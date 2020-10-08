# -*- coding: UTF-8 -*-
import os
import logging


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
        for line in lines:
            # drop blank lines
            line = line.lstrip()
            # drop lines that are commented or start by white space
            if not (line.startswith('//') or line.startswith(' ')):
                fw.write(line)
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
