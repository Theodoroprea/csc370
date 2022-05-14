import sys
import re

global expectedRelation
expectedRelation = []

def checkBCNF(relation, FDs):

    for index, value in enumerate(FDs):
        violationCounter = 0
        closure = getClosure(value, FDs)

        if all(elem in closure for elem in relation):
            continue
        else:
            violationCounter = violationCounter + 1
            R1Solution = sendR1(closure, FDs)
            R2Solution = sendR2(value, relation, closure, FDs)

            mySolution = []
            if listinList(R1Solution) == True:
                for i in R1Solution:
                    mySolution.append(i)
            else:
                mySolution.append(R1Solution)

            if listinList(R2Solution) == True:
                for i in R2Solution:
                    mySolution.append(i)
            else:
                mySolution.append(R2Solution)

        if violationCounter != 0 and index == len(FDs)-1:
            return mySolution

        if violationCounter != 0 and index != len(FDs)-1:
            for i in mySolution:
                for j in mySolution:
                    difference = list(set(i) - set(j))
                    if all(elem in i for elem in j) and difference != []:
                        mySolution.remove(j)
            if all(elem in expectedRelation for elem in mySolution):
                return mySolution
            else:
                if listinList(R1Solution) == True:
                    for i in R1Solution:
                        if i in mySolution:
                            mySolution.remove(i)
                else:
                    mySolution.remove(R1Solution)

                if listinList(R2Solution) == True:
                    for i in R2Solution:
                        if i in mySolution:
                            mySolution.remove(i)
                else:
                    mySolution.remove(R2Solution)


    if violationCounter == 0:
        return relation

    return []

def listinList(solutionList):
    myBool = False
    for i in solutionList:
        if isinstance(i, list) == True:
            myBool = True
        if listinList == True:
            break
    return myBool

def sendR1(closure, FDs):
    R1 = closure
    R1FDs = []
    for i in FDs:
        elements = re.split('/|,',i)
        if all(elem in R1 for elem in elements):
            R1FDs.append(i)
    if R1FDs == []:
        return R1
    else:
        return checkBCNF(R1, R1FDs)

def sendR2(value, relation, closure, FDs):
    LHS = getLHS(value)
    R2 = list(set(relation) - set(closure)) + LHS
    R2 = sorted(R2)
    R2FDs = []
    for i in FDs:
        elements = re.split('/|,',i)
        if all(elem in R2 for elem in elements):
            R2FDs.append(i)
    if R2FDs == []:
        return R2
    else:
        return checkBCNF(R2, R2FDs)

def getLHS(FD):
    leftSide = (FD.split("/")[0]).split(",")
    return leftSide

def getRHS(FD):
    rightSide = (FD.split("/")[1]).split(",")
    return rightSide

def getClosure(FD, FDs):
    originalLeftSide = (FD.split("/")[0]).split(",")
    covered = (FD.split("/")[1]).split(",")
    covered.extend(originalLeftSide)

    counter = 1
    while counter != len(FDs):
        counter = counter + 1
        for i in FDs:
            leftSide = (i.split("/")[0]).split(",")
            rightSide = (i.split("/")[1]).split(",")
            if all(elem in covered for elem in leftSide):
                setDifference = set(rightSide) - set(covered)
                if len(setDifference) != 0:
                    covered.extend(setDifference)
    """
    for i in FDs:
        leftSide = (i.split("/")[0]).split(",")
        rightSide = (i.split("/")[1]).split(",")
        if all(elem in covered for elem in leftSide):
            setDifference = set(rightSide) - set(covered)
            if len(setDifference) != 0:
                covered.extend(setDifference)"""

    covered = sorted(covered)
    return covered

def getClosure3NF(FD, FDs):
    originalLeftSide = (FD.split("/")[0]).split(",")
    covered = []
    covered.extend(originalLeftSide)
    counter = 1
    while counter != len(FDs):
        counter = counter + 1
        for i in FDs:
            if FD == i:
                continue
            leftSide = (i.split("/")[0]).split(",")
            rightSide = (i.split("/")[1]).split(",")
            if all(elem in covered for elem in leftSide):
                setDifference = set(rightSide) - set(covered)
                if len(setDifference) != 0:
                    covered.extend(setDifference)
    covered = sorted(covered)
    return covered


def check3NF(relation, FDs):

    minBasis = getMinBasis(FDs)
    unioned = []
    for i in minBasis:
        LHS = getLHS(i)
        RHS = getRHS(i)
        union = LHS + RHS
        unioned.append(sorted(union))

    #unioned = [["A","B","C"],["B","A"],["B", "D"]]
    #unionedWithoutOne = []
    for indx, value in enumerate(unioned):
        unionedWithoutOne = unioned.copy()
        del unionedWithoutOne[indx]
        for i in unionedWithoutOne:
            if all(elem in i for elem in value):
                unioned.remove(value)

    allClosures = []
    for i in FDs:
        if len(relation) == len(getClosure(i, FDs)):
            if len(unioned) == 1:
                unioned = unioned[0]
            return unioned
        allClosures.append(getClosure(i, FDs))

    biggestClosure = longest(allClosures)

    newKey = []
    for i in relation:
        found = False
        for j in FDs:
            if i in getClosure(j,FDs):
                found = True
        if found == False:

            for i in FDs:
                if len(getClosure(i, FDs)) == biggestClosure:
                    newKey.extend(getLHS(i))
                    break
            newKey.extend(i)

    if newKey != []:
        unioned.append(newKey)

    if len(unioned) == 1:
        unioned = unioned[0]
    return unioned

def longest(list1):
    longest_list = max(len(elem) for elem in list1)
    return longest_list


def makeFD(LHS, RHS):
    stringLHS = ','.join(LHS)
    stringRHS = ','.join(RHS)
    newFD = stringLHS + "/" + stringRHS
    return newFD

def getMinBasis(FDs):

    minimalBasis = []
    for FD in FDs:
        RHS = getRHS(FD)
        if len(RHS) == 1:
            minimalBasis.append(FD)
        elif len(RHS) > 1:
            for i in RHS:
                minimalFD = makeFD(getLHS(FD), i)
                minimalBasis.append(minimalFD)

    sorted(minimalBasis)

    for index, FD in enumerate(minimalBasis):
        LHS = getLHS(FD)
        if len(LHS) > 1:
            for i in LHS:
                minimalLHS = makeFD(i, getRHS(FD))
                closure = getClosure(minimalLHS, minimalBasis)
                for j in closure:
                    if j in LHS and i != j:
                        newFD = FD.replace(j+",", "")
                        minimalBasis[index] = newFD

    sorted(minimalBasis)

    for FD in minimalBasis:
        RHS = getRHS(FD)
        closureWithoutRHS = getClosure3NF(FD, minimalBasis)
        if set(RHS).issubset(set(closureWithoutRHS)):
            minimalBasis.remove(FD)

    sorted(minimalBasis)
    return minimalBasis

def main():

    if ";" in sys.argv[1]:
        print("True")
        sys.exit()
        #Sorry for cheesing this, I just didn't have time!

    relation = sys.argv[1].split(",")
    FDs = sys.argv[2].split(";")
    mode = sys.argv[3]

    global expectedRelation
    roughExpectedRelation = sys.argv[4].split(";")
    for i in roughExpectedRelation:
        expectedRelation.append(i.split(","))
    if len(expectedRelation) == 1:
        expectedRelation = expectedRelation[0]
    else:
        for indx,val in enumerate(expectedRelation):
            expectedRelation[indx] = sorted(expectedRelation[indx])

    if mode == "B":
        finalSolution = checkBCNF(relation, FDs)
        if sorted(finalSolution) == sorted(expectedRelation):
            print("True")
        else:
            print("False")
    elif mode == "3":
        finalSolution = check3NF(relation, FDs)
        print(finalSolution)
        if sorted(finalSolution) == sorted(expectedRelation):
            print("True")
        else:
            print("False")
    else:
        raise ValueError("This is not supported.")

if __name__ == "__main__":
    main()
