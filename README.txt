Run in CMD with the following parameters:
python SAT.py -Sn Sudoku_name.cnf

Or input a whole folder with .cnf files: 
python SAT.py -Sn -Folder=<foldername>

S1 = DPLL (Random)
S2 = JW-OS
S3 = JW-TS
S4 = Random + JW-OS
S5 = Random + JW-TS
S6 = MLV (minimum legal values)
S7 = Random + MLV
S8 = JW-OS + MLV
S9 = JW-TS + MLV