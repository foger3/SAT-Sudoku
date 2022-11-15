import math
import os

import numpy as np

path_tests = 'top91.sdk.txt'
rules = 'sudoku-rules-{}x{}.txt'

def to_dimacs(input_file):
    
    sudoku_tests = open(input_file, "r").readlines()
    print(f'File contains {len(sudoku_tests)} sudokus')
    n = 1
    
    # parse - sudokus
    for sudoku in sudoku_tests:
        
        size = round(math.sqrt(len(sudoku)-1))
        print(f'Sudoku {n} of size {size}*{size} \n', sudoku)
        
        # initialize empty sudoku grid n*n
        sudoku_mat = np.zeros((size * size))
        
        # fill sudoku grid
        for i, ch in enumerate(sudoku[:-1]):
            if ch =='.':
                ch = 0

            sudoku_mat[i]= int(ch)
            i+=1
        
        mat = sudoku_mat.reshape((size, size))
        print('Sudoku grid \n', mat)
        
        # get row, col if not == 0
        givens_cnf = np.transpose((mat!=0).nonzero())
        
        # first line Dimacs - get sudoku nvars and nclauses
        if size == 4:
            nclauses = 448
            nvars = 444
            
        if size == 9:
            nclauses = 12016
            nvars = 999
            
        if size == 16:
            nclauses = 123904
            nvars = 5832
            
        nclauses = nclauses + len(givens_cnf) # total clauses with givens
        file_dimacs = f'p cnf {nvars} {nclauses}\n'
         
        for i, clause in enumerate(givens_cnf):
            row = clause[0]
            col = clause[1]
            val = int(mat[row][col])
            file_dimacs += f'{row+1}{col+1}{val} 0\n'
        
        #givens_dimacs.write(f'puzzle_{i}_{size}*{size}')
        print(file_dimacs)  
        
        # add rules to file 
        file_rules = rules.format(size, size)
        
        with open(file_rules, 'r') as file:
            rules_dimacs = file.read()
            
        file_dimacs+=rules_dimacs.split('\n', 1)[1]
            
        #print(file_dimacs)
        # save each sudoku as dimacs txt files 
        with open(f'sudoku_{size}_{size}_{n}.txt', "w+") as dimacs:
            dimacs.write(file_dimacs)
            
        n+=1
 
        #close file
        dimacs.close()
                
    return

to_dimacs(path_tests)

