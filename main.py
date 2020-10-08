# -*- coding: UTF-8 -*-
import methods
import logging
import os

logging.basicConfig(level=logging.INFO)

logging.info('Starting conversion of file from assembly to machine language')

logging.debug('Setting paths')
# Execution variables
project = 'Pong'
dirname = os.path.dirname(__file__)
tmp_path = os.path.join(dirname, 'tmp')
tmp_file = os.path.join(dirname, 'tmp', project + '_tmp.asm')
original_file = os.path.join(dirname, 'assembly_language_files', project + '.asm')
label_cv_file = os.path.join(dirname, 'tmp', project + '_label_cv.asm')
variable_cv_file = os.path.join(dirname, 'tmp', project + '_variable_cv.asm')
machine_file = os.path.join(dirname, 'machine_language_files', project + '-mine.hack')


logging.debug('Deleting blank lines, initial white spaces and commented lines')
# Delete commented lines
with open(original_file, 'r') as fp:
    lines = fp.readlines()
    methods.delete_lines(lines, tmp_file)


logging.debug('Creating symbol table with pre-defined symbols')
# Create symbol table with PRE-DEFINED symbols
symbols = methods.s_tables()

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
            instruction_type = methods.instruction_type(line)
            if instruction_type == 'label':
                label = line[line.find("(") + 1:line.find(")")]
                symbols.update({label: cnt-cnt2})
                cnt2 += 1
            # drop lines that start by whitespace or are commented
            if not line.startswith('('):
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
            instruction_type = methods.instruction_type(line.lstrip())
            if instruction_type == 'A_Var':
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
                instruction_type = methods.instruction_type(line.lstrip())
                # parse instruction to binary
                result = methods.parser(line.strip(), instruction_type)
                res.write(result)
                res.write("\n")
            line = fp.readline()
            cnt += 1
    res.close()

logging.debug('Deleting temporary files')
methods.delete_files(tmp_path)

logging.info('Files successfully converted into machine language')
