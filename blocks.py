import sys; args = sys.argv[1:]
import math, time

def findPairs(listOfArgs):
    listOfPairs = []
    listOfArgs = [arg.lower() for arg in listOfArgs]
    for argIdx, arg in enumerate(listOfArgs):
        if "x" in arg:
            indexOfX = arg.index("x")
            listOfPairs.append((int(arg[:indexOfX]), int(arg[indexOfX+1:])))
        else:
            if(argIdx < len(listOfArgs)-1 and not "x" in listOfArgs[argIdx+1]):
                #print(argIdx, listOfPairs)
                #print(listOfArgs[indexOfArg], listOfArgs[indexOfArg+1])
                listOfPairs.append((int(listOfArgs[argIdx]), int(listOfArgs[argIdx+1])))
    return listOfPairs

def setGlobals(arguments):
    letters = [*"ABCDEFGHJIKLMNOPQRSTUVWXYZ"]
    height = int(findPairs(arguments)[0][0])
    width = int(findPairs(arguments)[0][1])
    return (height, width, {letters[idx]:(pair, (pair[1], pair[0])) for idx, pair in enumerate(findPairs(arguments)[1:])})

def printBoard(board):
    print("\n".join([board[i:i+width] for i in range(0, len(board), width)]))

def pzlPossible(BLOCKSET, height, width):
    areaSum = 0
    totalArea = height*width
    for blockSym in BLOCKSET:
        block = BLOCKSET[blockSym][0]
        areaSum += block[0]*block[1]
        if areaSum > totalArea:
            return False
    return True

def pzlIsDone(pzl):
    if "." in pzl:
        return False
    return True

def isPossibleInsertion(pzl, topLeftInd, blockW, blockH):
    for rowNum in range(blockH):
        startInd = topLeftInd + (rowNum*width)
        startIndRow = startInd // width
        for rowInd in range(startInd, startInd+blockW):
            rowIndRow = rowInd // width
            if rowInd >= len(pzl):
                return False
            if startIndRow != rowIndRow:
                return False

    return True

def insertBlock(pzl, topLeftInd, blockW, blockH, symbol):
    #print("func called", blockW, blockH)
    #printBoard(pzl)
    if isPossibleInsertion(pzl, topLeftInd, blockW, blockH):
        for rowNum in range(blockH):
            startInd = topLeftInd + (rowNum*width)
            for rowInd in range(startInd, startInd+blockW):
                #print(startInd, rowInd)
                replacedSym = pzl[rowInd]
                if replacedSym != ".":
                    #print("false triggerd", topLeftInd)
                    return False
                pzl = pzl[:rowInd] + symbol + pzl[rowInd+1:]
        #print("successful", symbol, topLeftInd)
        return pzl
    return False

def bruteForce(pzl, BLOCKSET):
    if len(BLOCKSET) == 0: return pzl

    idx = pzl.index(".") #find unfilled pos
    for blockSym in BLOCKSET: 
        for orientation in BLOCKSET[blockSym]:
            blockW = orientation[0]
            blockH = orientation[1]
            newPzl = insertBlock(pzl, idx, blockW, blockH, blockSym)
            if newPzl:
                newBLOCKSET = {key:BLOCKSET[key] for key in BLOCKSET}
                newBLOCKSET.pop(blockSym)#update blockset
                #print("blockset:", BLOCKSET, "newblockset:", newBLOCKSET)
                bF = bruteForce(newPzl, newBLOCKSET)
                if bF: return bF
    return False

def decomposePuzzle(pzl):
    symbolsEncountered = {}
    blockSizes = {}
    widthsAndHeights = {}
    finStr = ""
    for idx, chr in enumerate(pzl):
        if chr not in symbolsEncountered: #first time seeing each symbol
            symbolsEncountered[chr] = 1 
            rowNum = idx // width
            #print(rowNum, pzl[rowNum*width:rowNum*width+width])
            thisChrBlockW = 0
            for sym in pzl[rowNum*width:rowNum*width+width]:
                if sym == chr:
                    thisChrBlockW += 1
            blockSizes[chr] = thisChrBlockW
        else:
            symbolsEncountered[chr] += 1

    for sym in symbolsEncountered:
        widthsAndHeights[sym] = (blockSizes[sym], symbolsEncountered[sym] // blockSizes[sym])

    for sym in widthsAndHeights:
        finStr += str(widthsAndHeights[sym][1]) + "x" + str(widthsAndHeights[sym][0]) + " "
    
    return finStr

def main():
    if args:
        global BLOCKSET, height, width, pzl
        height, width, BLOCKSET = setGlobals(args)
        if not pzlPossible(BLOCKSET, height, width):
            print("No solution possible")
        else:
            #print(height, width)
            pzl = "."*width*height
            #print(BLOCKSET)
            solution = bruteForce(pzl, BLOCKSET)
            if solution:
                print("Decomposition:", decomposePuzzle(solution))
                printBoard(solution)
            else:
                print("No solution possible")
    else:
        newargs = ["16", "9", "9", "16"]
        height, width, BLOCKSET = setGlobals(newargs)
        print(BLOCKSET)
        #print(height, width)
        pzl = "."*width*height
        solution = bruteForce(pzl, BLOCKSET)
        #printBoard(bruteForce(pzl, BLOCKSET))
        print(decomposePuzzle(bruteForce(pzl, BLOCKSET)))

if __name__ == '__main__': main()
