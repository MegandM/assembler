# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import methods
import logging
import os
import argparse

logging.basicConfig(level=logging.INFO)


def args():
    parser = argparse.ArgumentParser(description='Convert file in assembly language into machine language')
    required_arg = parser.add_argument_group('required arguments')
    required_arg.add_argument('-i', '--input', dest='filename', action='store', required=True,
                              type=str, help='File in assembly language to be converted')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    return parser.parse_args()


def instruction_type(instruction):
    """
    Defines instruction type according to a list of rules
    :param instruction: assembly instruction
    :return:
    """
    # check symbols starting with @
    # if symbol is already in symbols table -> A
    # else it is variable
    # if instruction starts with ( -> label
    # else C
    starts_with = instruction[0]
    if starts_with == '@':
        symbol = instruction.split('@')[1]
        if symbol[0].isdigit():
            i_type = 'A'
        else:
            i_type = 'A_Var'
    elif starts_with == "(":
        i_type = 'label'
    else:
        i_type = 'C'
    return i_type


def parser(instruction, i_type):
    """
    Parses assembly instruction to binary code.
    :param instruction:
    :param i_type:
    :return:
    """
    # A instruction
    if i_type == 'A':
        binary = f"0{int(instruction[1:]):015b}"
    # C instruction
    else:
        # init binary instruction
        binary = '111'
        # check JUMP expression
        if ";" in instruction:
            # jump expression
            code_j = instruction.split(';')[1][0:3].rstrip()
            instruction = instruction.split(';')[0]
        else:
            code_j = 'null'

        # dest & comp expression
        if "=" in instruction:
            code_d = instruction.split('=')[0]
            code_c = instruction.split('=')[1][0:3].rstrip()
        else:
            code_c = instruction
            code_d = 'null'

        # check COMP and/or DEST
        tabs = ['comp','dest','jump']
        for i in tabs:
            # destination information
            if i == 'comp':
                code = code_c
                if "M" in code:
                    a_param = '1'
                else:
                    a_param = '0'
                binary = binary + a_param
            elif i == 'dest':
                code = code_d
            elif i == 'jump':
                code = code_j
            # check table
            table = c_tables(i, a_param)
            # check value for a given key
            trans = list(table.values())[list(table.keys()).index(code)]
            binary = binary + trans
    return binary


def c_tables(type, a_param):
    """
    Contains C instructions conversion
    :param type: comp/dest/jump table
    :param a_param: a parameter
    :return:
    """
    try:
        if type == "comp":
            if a_param == '0':
                table = {"0": "101010",
                         "1": "111111",
                         "-1": "111010",
                         "D": "001100",
                         "A": "110000",
                         "!D": "001101",
                         "!A": "110001",
                         "-D": "001111",
                         "-A": "110011",
                         "D+1": "011111",
                         "A+1": "110111",
                         "D-1": "001110",
                         "A-1": "110010",
                         "D+A": "000010",
                         "D-A": "010011",
                         "A-D": "000111",
                         "D&A": "000000",
                         "D|A": "010101"
                        }
            elif a_param == "1":
                table = {"M": "110000",
                         "!M": "110001",
                         "-M": "110011",
                         "M+1": "110111",
                         "M-1": "110010",
                         "D+M": "000010",
                         "D-M": "010011",
                         "M-D": "000111",
                         "D&M": "000000",
                         "D|M": "010101"
                        }
            else:
                raise ValueError

        elif type == 'dest':
            table = {"null": "000",
                     "M": "001",
                     "D": "010",
                     "MD": "011",
                     "A": "100",
                     "AM": "101",
                     "AD": "110",
                     "AMD": "111"}

        elif type == "jump":
            table = {"null": "000",
                     "JGT": "001",
                     "JEQ": "010",
                     "JGE": "011",
                     "JLT": "100",
                     "JNE": "101",
                     "JLE": "110",
                     "JMP": "111"}
        else:
            raise ValueError

    except ValueError:
        print("Unknown table or incorrect 'a' argument")

    return table


def s_tables():
    """
    Create symbol tables. Fill it with pre-defined symbols.
    :return: symbols table
    """
    values = list(map(str, list(range(0, 16))))
    keys = ['R' + s for s in values]
    table = dict(zip(keys, values))
    table.update({'SCREEN': 16384, 'KBD': 24576, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4})
    return table


def delete_lines(lines, newfile):
    """
    Deletes blank lines, commented lines and lines starting by white spaces
    :param lines: lines read from .asm file
    :param newfile: output file
    :return:
    """
    with open(newfile, 'w') as fw:
        for l in lines:
            # drop blank lines
            l_strip = l.lstrip()
            # drop lines that are commented or start by white space
            if not (l_strip.startswith('//') or l_strip.startswith(' ')):
                fw.write(l_strip)
    return


def delete_files(directory):
    """
    Deletes all files of a certain directory
    :param directory: directory where files to be removed are located
    :return:
    """

    try:
        files_list = os.listdir(directory)
        for f in [directory + '/' + s for s in files_list]:
            os.remove(f)
    except FileNotFoundError:
        logging.error(f'File to delete in path {directory} is not found or {directory} does not exist')

    return


if __name__ == "__main__":
    # Project variables
    filename = args().filename
    project = filename.split(".", 1)[0]
    output = project + '.hack'
    logging.info(f'Starting conversion of file {filename} from assembly to machine language {output}')

    logging.debug('Setting paths')
    # Execution variables
    dir_name = os.path.dirname(__file__)
    tmp_path = os.path.join(dir_name, 'tmp')
    tmp_file = os.path.join(dir_name, 'tmp', project + '_tmp.asm')
    original_file = os.path.join(dir_name, 'assembly_language_files', filename)
    label_cv_file = os.path.join(dir_name, 'tmp', project + '_label_cv.asm')
    variable_cv_file = os.path.join(dir_name, 'tmp', project + '_variable_cv.asm')
    machine_file = os.path.join(dir_name, 'machine_language_files', project + '-mine.hack')

    logging.debug('Deleting blank lines, initial white spaces and commented lines')
    # Delete commented lines
    with open(original_file, 'r') as fp:
        lines = fp.readlines()
        delete_lines(lines, tmp_file)

    logging.debug('Creating symbol table with pre-defined symbols')
    # Create symbol table with PRE-DEFINED symbols
    symbols = s_tables()

    logging.debug('Translating label symbols')
    # Scan LABEL symbols in code
    with open(tmp_file, 'r+') as fp:
        with open(label_cv_file, 'w') as fw:
            # read line
            line = fp.readline()
            cnt = 1
            cnt2 = 1
            # for each line
            while line:
                # define instruction type (A, C)
                i_type = instruction_type(line)
                if i_type == 'label':
                    label = line[line.find("(") + 1:line.find(")")]
                    symbols.update({label: cnt-cnt2})
                    cnt2 += 1
                # drop lines that start by whitespace or are commented
                else:
                    fw.write(line)
                line = fp.readline()
                cnt += 1

    logging.debug('Translating variable symbols')
    # Third, scan VARIABLE symbols in code
    with open(label_cv_file, 'r') as fp:
        with open(variable_cv_file, 'w') as tf:
            # read line
            line = fp.readline()
            cnt = 1
            n = 16
            # for each line
            while line:
                # define instruction type (A, C)
                i_type = instruction_type(line.lstrip())
                if i_type == 'A_Var':
                    # translate variable to equivalent register
                    symb = line.split('@')[1].rstrip("\n").rstrip()
                    if symb not in symbols.keys():
                        symbols.update({symb: n})
                        n += 1
                    # check variable value in symbols table
                    variable = str(list(symbols.values())[list(symbols.keys()).index(symb)])
                    # overwrite line where variable appears
                    line = '@' + variable + "\n"
                # write into file
                tf.write(line)
                line = fp.readline()
                cnt += 1

    # Third, translate instruction into binary
    logging.debug('Translating instructions')
    with open(variable_cv_file, 'r') as fp:
        with open(machine_file, 'w') as res:
            # read line
            line = fp.readline()
            cnt = 1
            # for each line
            while line:
                # if line is not empty or commented
                if line.strip() and (line[0] is not '/'):
                    # define instruction type (A, C)
                    i_type = instruction_type(line.lstrip())
                    # parse instruction to binary
                    result = parser(line.strip(), i_type)
                    res.write(result)
                    res.write("\n")
                line = fp.readline()
                cnt += 1
        res.close()

    logging.debug('Deleting temporary files')
    delete_files(tmp_path)

    logging.info(f'File {filename} successfully converted into machine language file {output}')
