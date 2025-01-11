import random

SUDOKU_SIZE = 16
GRID_SIZE = 4
MAX_BT_CALL = 20000
MAX_CONSIDERED_SOLUTION = 30
ACCEPTED_SAME_SOLUTION = 20
sudokuCharSet = "G123456789ABCDEF"
english_words_file = "english_words.txt"
input_file = "input.txt"
output_file = "output.txt"
question2Solve = [""] * SUDOKU_SIZE
solvedSudoku = [""] * SUDOKU_SIZE
maxScoredSolvedSudoku = [""] * SUDOKU_SIZE
maxScore = 0
solutionNumber = 0
backtrack_call_trace = 0
collectionOfSolvedPuzzle = [""] * MAX_CONSIDERED_SOLUTION
collectionOfScoresOfSolvedPuzzle = [""] * MAX_CONSIDERED_SOLUTION
english_words = []
task_description = ""
sameSolutionConter = 0

# Function to check if a word can be formed from a sequence
def can_form_word(sequence, word):
    return sequence.count(word)

def isValid(num, row, col):
    for x in range(SUDOKU_SIZE):
        if solvedSudoku[row][x] == num:
            return False
        if solvedSudoku[x][col] == num:
            return False
        if solvedSudoku[row // GRID_SIZE * GRID_SIZE + x // GRID_SIZE][col // GRID_SIZE * GRID_SIZE + x % GRID_SIZE] == num:
            return False
    return True

def checkRow(newItem, row):
    return newItem in solvedSudoku[row]

def checkCol(newItem, col):
    return any(solvedSudoku[r][col] == newItem for r in range(SUDOKU_SIZE))

def printSudoku():
    with open(output_file, 'a') as f:
        for row in maxScoredSolvedSudoku:
            f.write("".join(row) + "\n")

def printOtherPossibilities():
    with open(output_file, 'a') as f:
        for i in range(MAX_CONSIDERED_SOLUTION):
            for row in collectionOfSolvedPuzzle[i]:
                f.write("".join(row) + "\n")
            f.write(f"Score: {collectionOfScoresOfSolvedPuzzle[i]}\n----------------\n")

#Backtrack Solution
def solveSudoku(type):
    global backtrack_call_trace
    global solvedSudoku
    global sudokuCharSet
    if backtrack_call_trace > MAX_BT_CALL:
        return True
    backtrack_call_trace += 1

    for row in range(SUDOKU_SIZE):
        for col in range(SUDOKU_SIZE):
            if solvedSudoku[row][col] == '.':
                allCharSet = sudokuCharSet
                for k in range(SUDOKU_SIZE):
                    if (type == -1):
                        #random simulation
                        num = random.choice(allCharSet)
                        allCharSet = allCharSet.replace(num, "")
                    else:
                        #serial simulation
                        num = sudokuCharSet[(k + type)%SUDOKU_SIZE]
                    
                    if isValid(num, row, col):
                        solvedSudoku[row][col] = num
                        if solveSudoku(type):
                            return True
                        solvedSudoku[row][col] = '.'
                return False
    return True

#Brute-force Solution
def placeI(sudokuChar):
    possibleRows2Place = [i for i in range(SUDOKU_SIZE) if not checkRow(sudokuChar, i)]
    possibleCols2Place = [i for i in range(SUDOKU_SIZE) if not checkCol(sudokuChar, i)]

    for i in possibleRows2Place:
        while possibleCols2Place:
            j = possibleCols2Place.pop(0)
            if solvedSudoku[i][j] == '.' and isValid(sudokuChar, i, j):
                solvedSudoku[i][j] = sudokuChar
                break

def match_words(words):
    matched_count = 0
    # Check rows
    for row in solvedSudoku:
        row_str = "".join(row)
        for word in words:
            if len(word) >= 3:
                matched_count += can_form_word(row_str, word)
    
    return matched_count

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def isGridSolved():
    global solvedSudoku
    for row in solvedSudoku:
        row_str = "".join(row)
        if (row_str.count(".") > 0):
            return False
    return True

def hex2Dec(hexChar):
    global sudokuCharSet
    return sudokuCharSet.find(hexChar)

# 0 for Serial Selection of Characters
# 1 for Random Selection of Characters
def runSimulation(simulationType):
    global maxScore
    global solvedSudoku
    global question2Solve
    global sameSolutionConter
    global backtrack_call_trace
    global maxScoredSolvedSudoku
    global collectionOfSolvedPuzzle
    global collectionOfScoresOfSolvedPuzzle

    if (sameSolutionConter == ACCEPTED_SAME_SOLUTION):
        return

    if (simulationType == 0):
        collectionOfSolvedPuzzleIndex = 0
        maxSimulationCount = SUDOKU_SIZE
    else:
        collectionOfSolvedPuzzleIndex = SUDOKU_SIZE
        maxSimulationCount = MAX_CONSIDERED_SOLUTION

    for alternateSolution in range (collectionOfSolvedPuzzleIndex, maxSimulationCount):
        backtrack_call_trace = 0
        solvedSudoku = [list(row) for row in question2Solve]

        if (simulationType == 0):
            booom = solveSudoku(alternateSolution)
        else:
            booom = solveSudoku(-1)
        
        if backtrack_call_trace >= MAX_BT_CALL:
            charPlaced = [0] * SUDOKU_SIZE
            for i in range(SUDOKU_SIZE):
                for j in range(SUDOKU_SIZE):
                    if solvedSudoku[i][j] != '.':
                        charPlaced[hex2Dec(solvedSudoku[i][j])] += 1
 
            highestPossibilities = 16
            while highestPossibilities:
                highestPossibilities -= 1
                for i in range(SUDOKU_SIZE):
                    if charPlaced[i] == highestPossibilities:
                        placeI(sudokuCharSet[i])

        # Match words and calculate score
        score = match_words(english_words)
        if (score >= maxScore and isGridSolved()):
            maxScoredSolvedSudoku = [list(row) for row in solvedSudoku]
            maxScore = score

        if (maxScoredSolvedSudoku == solvedSudoku):
            sameSolutionConter += 1
        
        collectionOfSolvedPuzzle[alternateSolution] = solvedSudoku
        collectionOfScoresOfSolvedPuzzle[alternateSolution] = score

        if (sameSolutionConter == ACCEPTED_SAME_SOLUTION):
            return

if __name__ == "__main__":
    # Read English words list
    with open(english_words_file, 'r') as f:
        english_words = [word.strip().upper() for word in f.readlines()]

    # Read input Sudoku task
    with open(input_file, 'r') as f:
        task_description = f.readlines()

    question2Solve = [list(row.strip()) for row in task_description]
    
    runSimulation(0) # Serial placement of character
    runSimulation(1) # Random placement of character

    # Clear output file
    open(output_file, 'w').close()

    # Print solved Sudoku with max count to output file
    printSudoku()
    # Append score information to output file
    with open(output_file, 'a') as f:
        f.write(f"Maximum Score: {maxScore}\n")
        f.write(f"================\n")

    # Print all other possibilities
    printOtherPossibilities()        

