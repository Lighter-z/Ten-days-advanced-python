from random import randint

def generateSequenceArray(n):
    result = []
    for i in range(n):
        result.append(i)
    return result


def generateRandomArray(n):
    result = generateSequenceArray(n)
    for i in range(n):
        r = randint(i,n-1)
        t = result[r]
        result[r] = result[i]
        result[i] = t
    return result

def printList(list):
    print(list)
