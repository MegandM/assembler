# Assembler
This project is the final assignment of [From Nand to Tetris](https://www.nand2tetris.org/) course.
An assembler is created to translate files in Hack assembly language to Hack machine language (binary code). Hack is a language created by the professors of this course.
The syntax rules are explained in this [file](https://b1391bd6-da3d-477d-8c01-38cdf774495a.filesusr.com/ugd/56440f_65a2d8eef0ed4e0ea2471030206269b5.pdf). Rules must be applied to handle:
* white spaces
* instructions (A and C)
* symbols (pre-defined, label and variables)

## Pre requisites
### Environment setup
```bash
pip install -r requirements.txt
```

# Run
Check `main.py` usage by executing:
```bash
$ python main.py -h
usage: main.py [-h] -i FILENAME [--verbose]

Convert file in assembly language into machine language

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v

required arguments:
  -i FILENAME, --input FILENAME
                        File in assembly language to be converted
```


