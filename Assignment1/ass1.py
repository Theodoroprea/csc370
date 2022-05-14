import sys
import re

global solution
solution = []
global solutionFinal
solutionFinal = []
global expectedRelation
expectedRelation = []

def checkBCNF(relation, FDs):
    global solution

    #print()
    #print(f"Relation: {relation}")

    for index, value in enumerate(FDs):
        violationCounter = 0

        closure = getClosure(value, FDs)

        if all(elem in closure for elem in relation):
            continue
        else:
            violationCounter = violationCounter + 1

            R1 = closure
            R1FDs = []
            for i in FDs:
                elements = re.split('/|,',i)
                if all(elem in R1 for elem in elements):
                    R1FDs.append(i)
            if R1FDs == []:
                solution.append(R1)
            else:
                checkBCNF(R1, R1FDs)
                #print(solution)

            LHS = getClosureLHS(value)
            R2 = list(set(relation) - set(closure)) + LHS
            R2 = sorted(R2)
            #print(f"I am R2: {R2}")
            R2FDs = []
            for i in FDs:
                elements = re.split('/|,',i)
                if all(elem in R2 for elem in elements):
                    R2FDs.append(i)
            if R2FDs == []:
                solution.append(R2)
            else:
                checkBCNF(R2, R2FDs)
                #print(solution)

        if violationCounter != 0:
            for i in solution:
                for j in solution:
                    difference = list(set(i) - set(j))
                    if all(elem in i for elem in j) and difference != []:
                        solution.remove(j)
            print(solution)
            if all(elem in expectedRelation for elem in solution):
                return
            #else:
            #    print("we made it here")
                #print(localTracker)
                #del solution[-1:localTracker]
                #print(solution)

    if violationCounter == 0:
        solution.append(relation)

def getClosureLHS(FD):
    originalLeftSide = (FD.split("/")[0]).split(",")
    return originalLeftSide

def getClosure(FD, FDs):
    originalLeftSide = (FD.split("/")[0]).split(",")
    covered = (FD.split("/")[1]).split(",")
    covered.extend(originalLeftSide)
    for i in FDs:
        leftSide = (i.split("/")[0]).split(",")
        rightSide = (i.split("/")[1]).split(",")
        if all(elem in covered for elem in leftSide):
            setDifference = set(rightSide) - set(covered)
            if len(setDifference) != 0:
                covered.extend(setDifference)
    covered = sorted(covered)
    #print(f"{originalLeftSide} --> {covered}")
    return covered

def main():

    relation = sys.argv[1].split(",")
    FDs = sys.argv[2].split(";")
    mode = sys.argv[3]

    global expectedRelation
    roughExpectedRelation = sys.argv[4].split(";")
    for i in roughExpectedRelation:
        expectedRelation.append(i.split(","))

    if mode == "B":
        checkBCNF(relation, FDs)
        print(f"solution -> {sorted(solution)}")
        print(f"expected solution -> {sorted(expectedRelation)}")
        if sorted(solution) != sorted(expectedRelation):
            print("False")
        else:
            print("True")
    elif mode == "3":
        print("Not implemented yet")
    else:
        raise ValueError("This is not supported.")

if __name__ == "__main__":
    main()
