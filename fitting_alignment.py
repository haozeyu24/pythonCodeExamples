
from cmath import inf
import sys
import pandas as pd
sys.setrecursionlimit(10000)

def LSCBackTrack(v,w,string1,string2,indelPenalty,dict_PAM):
    matrixS = [[0 for i in range(w+1)] for i in range(v+1)]
    backTrack = [[0 for i in range(w+1)] for i in range(v+1)]

    for i in range(1,w+1):
        backTrack[0][i] = 3 # horizontal
    for i in range(1,v+1):
        backTrack[i][0] = 2  # vertical

    for i in range(w+1):
        matrixS[0][i] = indelPenalty * i
    for i in range(v+1):
        matrixS[i][0] = 0 * i
    matrixS[0][0] = 0

    for i in range(1,v+1):
        for j in range(1,w+1):
            # if string1[i-1] == string2[j-1]:
            #     match = 1
            # else:
            #     match = -1
            match =  dict_PAM[string1[i-1] ,string2[j-1]]

            
            matrixS[i][j] = max(matrixS[i-1][j] -float(inf) , matrixS[i][j-1] + indelPenalty, matrixS[i-1][j-1] + match, 0)
            if matrixS[i][j] == matrixS[i-1][j-1] + match:
                backTrack[i][j] = 1
            elif matrixS[i][j] == matrixS[i-1][j] -float(inf):
                backTrack[i][j] = 2
            elif matrixS[i][j] == matrixS[i][j-1] + indelPenalty:
                backTrack[i][j] = 3
            else:
                backTrack[i][j] = 0
    # print(backTrack[0])
    # print(backTrack[1])
    # print(backTrack[2])

    # print()
    # print(matrixS[0])
    # print(matrixS[1])
    # print(matrixS[2])

    return backTrack, matrixS
    

def outPutLCString1(backTrack, string1, v, w):
    if w == 0 and v == 0:
        return ""
    elif backTrack[v][w] == 0:
        return outPutLCString1(backTrack, string1, v-1, w-1) + string1[v-1]
    elif backTrack[v][w] == 1:
        return outPutLCString1(backTrack, string1, v-1, w-1) + string1[v-1]
    elif backTrack[v][w] == 2:
        return outPutLCString1(backTrack, string1, v-1, w) + string1[v-1]
    elif backTrack[v][w] == 3:
        return outPutLCString1(backTrack, string1, v, w-1) + "-"

def outPutLCString2(backTrack, string2, v, w):
    if w == 0 and v ==0:
        return ""
    elif backTrack[v][w] == 0:
        return outPutLCString2(backTrack, string2, v-1, w-1) + string2[w-1]
    elif backTrack[v][w] == 1:
        return outPutLCString2(backTrack, string2, v-1, w-1) + string2[w-1]
    elif backTrack[v][w] == 2:
        return outPutLCString2(backTrack, string2, v-1, w) + "-"
    elif backTrack[v][w] == 3:
        return outPutLCString2(backTrack, string2, v, w-1) + string2[w-1]


def largestValue(matrixS,v,w):
    max = 0
    a = 0 
    for i in range(v+1):
            if matrixS[i][w] > max:
                max = matrixS[i][w]
                a = i 
    return a,w


if __name__ == '__main__':
    with open("dataset_248_5.txt","r") as f:
        string1 = f.readline().strip()
        string2 = f.readline().strip()

    df_PAM250 = pd.read_csv('BLOSUM62.txt', sep='\s+')
    with open("BLOSUM62.txt",'r') as f:
        letters = f.readline().strip().split()

    dict_PAM = {}
    for i in letters:
        for j in letters:
            dict_PAM[(i,j)] = df_PAM250[i][j]

    indelPenalty = -1
    v = len(string1)
    w = len(string2)

    backTrack,matrixS = LSCBackTrack(v,w,string1,string2,indelPenalty,dict_PAM)

    a, b = largestValue(matrixS,v,w)

    output1 = outPutLCString1(backTrack, string1, a, b)[-w:]
    output2 = outPutLCString2(backTrack, string2, a, b)[-w:]

   
    
    score = 0
    for i in range(len(output1)):
        if output1[i] != output2[i]:
            score -= 1
        else:
            score += 1
    print(score)
    print(output1)
    print(output2)

    with open("results_248_5.txt","w") as f:
        f.write(str(score)+ "\n")
        f.write(outPutLCString1(backTrack, string1, a, b)[-w:]+ "\n")
        f.write(outPutLCString2(backTrack, string2, a, b)[-w:])
    