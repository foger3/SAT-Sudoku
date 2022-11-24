Run in CMD with the following parameters:
\python SAT.py -Sn Sudoku_name

For instance, if you want to run heuristic 3 on "sudoku1.cnf", put the following in CMD:
"python SAT.py -S3 Sudoku1.cnf"

Or input a whole folder with .cnf files: 
\python SAT.py -Sn -Folder=foldername

For instance, if you want to run heuristic 4 on all files in folder "sudokus", put the following in CMD:
"python SAT.py -S4 -Folder=sudokus"

S1 = DPLL (Random)
S2 = JW-OS
S3 = JW-TS
S4 = cJW-OS (Random + JW-OS)
S5 = cJW-TS (Random + JW-TS)
S6 = MLV (Minimum Legal Values)
S7 = cMLV (Random + MLV)
S8 = JW-OS+MLV
S9 = JW-TS+MLV
