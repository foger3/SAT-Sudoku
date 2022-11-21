import os, sys, time, random, csv, numpy as np

class SolvSAT:
    def __init__(self, dimacs, heuristic):
        self.dimacs = dimacs
        self.heuristic = heuristic
        self.clauses = []
        self.literals = []
        self.solution = []
        self.backtracking = 0

    def start(self):
        for string in self.dimacs:
            if string.startswith("p"):
                continue
            clauses = [int(x) for x in string[:-2].split()]
            for i in clauses:
                if abs(i) not in self.literals:
                    self.literals.append(abs(i))
            self.clauses.append(clauses)

    def results(self):
        self.clauses = taut_check(self.clauses)
        backtracks.count = 0
        self.solution = backtracks(self.clauses, [], self.heuristic)
        self.backtracking = backtracks.count
        print("# of Backtracks: {}".format(self.backtracking))
        if self.solution:  # rearrange solution in a 9x9 Sudoku grid
            sol = [x for x in sorted(self.solution) if x > 0]
            print(np.array([int(str(i)[-1]) for i in sol]).reshape(9, 9))
        else:
            print("Unsatisfiable!")

    def colab_res(self, heuristic):
        self.clauses = taut_check(self.clauses)
        colab_backs.count = 0
        colab_backs.cocount = 0
        colab_backs.heur = dpll
        colab_backsTS.count = 0
        colab_backsTS.cocount = 0
        colab_backsTS.heur = dpll

        if heuristic == "-S4":
            self.solution = colab_backs(self.clauses, [], self.heuristic)
            self.backtracking = colab_backs.count
            print("# of Backtracks: {}".format(self.backtracking))
            if self.solution:  # rearrange solution in a 9x9 Sudoku grid
                sol = [x for x in sorted(self.solution) if x > 0]
                print(np.array([int(str(i)[-1]) for i in sol]).reshape(9, 9))
            else:
                print("Unsatisfiable!")

        if heuristic == "-S5":
            self.solution = colab_backsTS(self.clauses, [], self.heuristic)
            self.backtracking = colab_backsTS.count
            print("# of Backtracks: {}".format(self.backtracking))
            if self.solution:  # rearrange solution in a 9x9 Sudoku grid
                sol = [x for x in sorted(self.solution) if x > 0]
                print(np.array([int(str(i)[-1]) for i in sol]).reshape(9, 9))
            else:
                print("Unsatisfiable!")

    def outfile(self, name):  # creates the solution .out file
        if not len(self.solution):
            pass
        else:
            sol = self.solution
            filename = name[:-4] + ".out"
            vars_nums = len(sol)
            clause_nums = len(sol)
            write = "p cnf {} {}\n".format(vars_nums, clause_nums)
            for i in sol:
                write += "{} 0\n".format(i)
            exp_file = open(filename, "w")
            exp_file.write(write)
            exp_file.close()
            print("\n Solution written to {}".format(os.path.basename(filename)))

    def outcome(self, name, heurname):  # creates the .cvs results file
        if sys.argv[2].endswith('.cnf') or sys.argv[2].endswith('.txt'):
            rfile_name = (str(name) + "_" + "results" + ".csv")

        if sys.argv[2].startswith('-Folder='):
            rfile_name = (str(directory[1]) + "_" + "results" + ".csv")

        resdict = {
            'filename': name,
            'heuristic': heurname,
            'duration': duration,
            'backtracks': self.backtracking
        }

        if not os.path.exists(rfile_name):
            res_file = open(rfile_name, "w", newline="")
            csv_writer = csv.DictWriter(res_file, fieldnames=resdict.keys(), dialect='excel')
            csv_writer.writeheader()
            res_file.close()

        csv_handle = open(rfile_name, "a", newline="")
        csv_writer = csv.DictWriter(csv_handle, fieldnames=resdict.keys(), dialect='excel')
        csv_writer.writerow(resdict)
        print("\n Results written to {}".format(os.path.basename(rfile_name)))

def colab_backs(x, found, coheuristic):  # Random + JWOS
    coheuristic = colab_backs.heur
    colab_backs.count += 1
    colab_backs.cocount += 1
    if colab_backs.cocount % 200 == 0:
        colab_backs.heur = changeheur(coheuristic)

    x, pure_found = pure_l(x)
    x, unit_found = atom_propagation(x)
    found = found + unit_found + pure_found
    if x == - 1:
        return []
    if not x:
        return found
    var = coheuristic(x)

    if coheuristic == dpll:
        solution = colab_backs(bcp(x, var), found + [var], coheuristic)
        if not solution:
            coheuristic = dpll
            solution = colab_backs(bcp(x, -var), found + [-var], coheuristic)
        return solution

    if coheuristic == JW_OS:
        solution = colabJWOS(bcp(x, var), found + [var], coheuristic)
        if not solution:
            coheuristic = JW_OS
            solution = colabJWOS(bcp(x, -var), found + [-var], coheuristic)
        return solution

def changeheur(coheuristic):
    if coheuristic == dpll:
        coheuristic = JW_OS
        return coheuristic

    else:
        coheuristic = dpll
        return coheuristic

def colabJWOS(x, found, heuristic):
    x, pure_found = pure_l(x)
    x, unit_found = atom_propagation(x)
    found = found + unit_found + pure_found
    if x == - 1:
        return []
    if not x:
        return found

    var = heuristic(x)
    solution = colab_backs(bcp(x, var), found + [var], heuristic)
    if not solution:
        solution = colab_backs(bcp(x, -var), found + [-var], heuristic)

    return solution

def colab_backsTS(x, found, heuristic):  # Random + JWTS
    coheuristic = colab_backsTS.heur
    colab_backsTS.count += 1
    colab_backsTS.cocount += 1
    if colab_backsTS.cocount % 200 == 0:
        colab_backsTS.heur = changeheurTS(coheuristic)

    x, pure_found = pure_l(x)
    x, unit_found = atom_propagation(x)
    found = found + unit_found + pure_found
    if x == - 1:
        return []
    if not x:
        return found
    var = coheuristic(x)

    if coheuristic == dpll:
        solution = colab_backsTS(bcp(x, var), found + [var], coheuristic)
        if not solution:
            coheuristic = dpll
            solution = colab_backsTS(bcp(x, -var), found + [-var], coheuristic)
        return solution

    if coheuristic == JW_TS:
        solution = colabJWTS(bcp(x, var), found + [var], coheuristic)
        if not solution:
            coheuristic = JW_TS
            solution = colabJWTS(bcp(x, -var), found + [-var], coheuristic)
        return solution

def changeheurTS(coheuristic):
    if coheuristic == dpll:
        coheuristic = JW_TS
        return coheuristic

    else:
        coheuristic = dpll
        return coheuristic

def colabJWTS(x, found, heuristic):
    x, pure_found = pure_l(x)
    x, unit_found = atom_propagation(x)
    found = found + unit_found + pure_found
    if x == - 1:
        return []
    if not x:
        return found

    var = heuristic(x)
    solution = colab_backsTS(bcp(x, var), found + [var], heuristic)
    if not solution:
        solution = colab_backsTS(bcp(x, -var), found + [-var], heuristic)

    return solution

def backtracks(x, found, heuristic):
    backtracks.count += 1
    x, pure_found = pure_l(x)
    x, unit_found = atom_propagation(x)
    found = found + unit_found + pure_found
    if x == - 1:
        return []
    if not x:
        return found

    var = heuristic(x)
    solution = backtracks(bcp(x, var), found + [var], heuristic)
    if not solution:
        solution = backtracks(bcp(x, -var), found + [-var], heuristic)

    return solution

def check_literals(x):
    amount = {}
    for i in x:
        for literal in i:
            if literal in amount:
                amount[literal] += 1
            else:
                amount[literal] = 1
    return amount

def bcp(x, y):  # unit clauses
    modified = []
    for clause in x:
        if y in clause:
            continue
        if -y in clause:
            new_clause = [x for x in clause if x != -y]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified

def pure_l(x):
    amount = check_literals(x)
    plist = []
    found = []
    for literals, i in amount.items():
        if -literals not in amount:
            plist.append(literals)
    for pure in plist:
        x = bcp(x, pure)
    found += plist
    return x, found

def atom_propagation(x):
    found = []
    unit_clauses = [c for c in x if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        x = bcp(x, unit[0])
        found += [unit[0]]
        if x == -1:
            return -1, []
        if not x:
            return x, found
        unit_clauses = [c for c in x if len(c) == 1]
    return x, found

def dpll(x):
    check = check_literals(x)
    return random.choice(list(check.keys()))

def taut_check(clauselist):
    updatelist = []
    match = 0
    for clause in clauselist:
        for literal in clause:
            if -literal in clause:
                match = 1
                break
        if match == 0:
            updatelist.append(clause)
        else:
            match = 0
    return updatelist

def JW_OS(x):
    checkjw1 = lit_JW1(x)
    return max(checkjw1, key=checkjw1.get)

def lit_JW1(x, weight=2):
    amount = {}
    for clause in x:
        for literal in clause:
            if literal in amount:
                amount[literal] += weight ** -len(clause)
            else:
                amount[literal] = weight ** -len(clause)
    return amount

def JW_TS(x):
    checkjw2 = lit_JW2(x)
    return max(checkjw2, key=checkjw2.get)

def lit_JW2(x, weight=2):
    amount = {}
    for clause in x:
        for literal in clause:
            literal = abs(literal)
            if literal in amount:
                amount[literal] += weight ** -len(clause)
            else:
                amount[literal] = weight ** -len(clause)
    return amount

if __name__ == "__main__":
    #  Check file parameters
    heuristic = None
    h = None
    if len(sys.argv) != 3:
        sys.exit("Input parameters as follows: python SAT.py -Sn <sudokuname>.cnf/.txt \n"
                 "Or input a folder with .cnf/.txt files: python SAT.py -Sn -Folder=<foldername>")

    heuristic = str(sys.argv[1])  # check heuristic
    if heuristic == "-S1":
        h = dpll
        heurname = "DPLL-Default"
        print("Running default DPLL (random splitting) \n")
    elif heuristic == "-S2":
        h = JW_OS
        heurname = "JW-OS"
        print("Running One Sided Jeroslow-Wang \n")
    elif heuristic == "-S3":
        h = JW_TS
        heurname = "JW-TS"
        print("Running Two Sided Jeroslow-Wang \n")
    elif heuristic == "-S4":
        h = dpll
        heurname = "Random+JW-OS"
        print("Running Collaborative Random+JW-OS")
    elif heuristic == "-S5":
        h = dpll
        heurname = "Random+JW-TS"
        print("Running Collaborative Random+JW-TS")
    else:
        sys.exit("Input parameters as follows: python SAT.py -Sn <sudokuname>.cnf/.txt \n"
                 "Or input a folder with .cnf/.txt files: python SAT.py -Sn -Folder=<foldername>")

    if sys.argv[2].endswith('.cnf') or sys.argv[2].endswith('.txt'):  # for single files
        sudoku = sys.argv[2]  # check sudoku filename

        txtwrap = open(sudoku, "r")
        dimacs = txtwrap.readlines()
        time_start = time.process_time()

        if heuristic == "-S4" or heuristic == "-S5":
            run = SolvSAT(dimacs, h)
            run.start()
            run.colab_res(heuristic)
            time_end = time.process_time()
            duration = time_end - time_start
            print("\n Duration: {:.8f}".format(duration))
            run.outfile(sudoku)
            run.outcome(sudoku, heurname)

        else:
            run = SolvSAT(dimacs, h)
            run.start()
            run.results()
            time_end = time.process_time()
            duration = time_end - time_start
            print("\n Duration: {:.8f}".format(duration))
            run.outfile(sudoku)
            run.outcome(sudoku, heurname)

    elif sys.argv[2].startswith('-Folder='):  # for folders containing files
        directory = (sys.argv[2].split('='))
        os.chdir(directory[1])
        for ind_sudoku in os.listdir():
            if ind_sudoku.endswith(".cnf") or ind_sudoku.endswith(".txt"):
                sudoku = ind_sudoku
                txtwrap = open(sudoku, "r")
                dimacs = txtwrap.readlines()
                print("\n Running {}".format(heurname))
                time_start = time.process_time()
                if heuristic == "-S4" or heuristic == "-S5":
                    run = SolvSAT(dimacs, h)
                    run.start()
                    run.colab_res(heuristic)
                    time_end = time.process_time()
                    duration = time_end - time_start
                    print("\n Duration: {:.8f}".format(duration))
                    run.outfile(sudoku)
                    run.outcome(sudoku, heurname)

                else:
                    run = SolvSAT(dimacs, h)
                    run.start()
                    run.results()
                    time_end = time.process_time()
                    duration = time_end - time_start
                    print("\n Duration: {:.8f}".format(duration))
                    run.outfile(sudoku)
                    run.outcome(sudoku, heurname)
            else:
                continue
    else:
        sys.exit("Sudoku has to end with either .cnf or .txt, or add a folder")