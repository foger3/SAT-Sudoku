import sys, time, random, numpy as np

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
        backtracks.count = 0
        self.solution = backtracks(self.clauses, [], self.heuristic)
        self.backtracking = backtracks.count
        print("# of Backtracks: {}".format(self.backtracking))
        if self.solution:  # rearrange solution in a 9x9 Sudoku grid
            Sol = [x for x in sorted(self.solution) if x > 0]
            print(np.array([int(str(i)[-1]) for i in Sol]).reshape(9, 9))
        else:
            print("Unsatisfiable!")

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
    print("TEST")
    return random.choice(list(check.keys()))

if __name__ == "__main__":
    #  Check file parameters
    if len(sys.argv) != 3:
        sys.exit("Input parameters as followed: python SAT.py -Sn Sudoku_name.cnf")

    heuristic = sys.argv[1]  # check heuristic
    if heuristic == "-S1" or "-s1":
        h = dpll
        print("Running default DPLL (random splitting) \n")
    elif heuristic == "-S2" or "-s2":
        pass
    elif heuristic == "-S3" or "-s3":
        pass
    else:
        sys.exit("Input parameters as followed: python SAT.py -Sn Sudoku_name.cnf")

    if sys.argv[2].endswith('.txt'):
        pass
    elif sys.argv[2].endswith('.cnf'):
        sudoku = sys.argv[2]  # check sudoku filename

        txtwrap = open(sudoku, "r")
        dimacs = txtwrap.readlines()
        time_start = time.process_time()
        run = SolvSAT(dimacs, h)
        run.start()
        run.results()
        time_end = time.process_time()
        duration = time_end - time_start
        print("\n Duration: {:.8f}".format(duration))
    else:
        sys.exit("Sudoku has to be in either .cnf or .txt format")