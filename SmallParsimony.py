

def parsingData(data,N):
    leafID = 0
    nodeSequence = {}
    nodeChildren = {}
    for i in range(N):
        entry = data[i].strip("\n")
        parent = int(entry.split("->")[0])
        sequence = entry.split("->")[1]
        roundOfParsimony = len(sequence)

        if parent in nodeChildren:
            nodeChildren[parent].append(leafID)
        else:
            nodeChildren[parent] = [leafID]
        
        nodeSequence[leafID] = sequence

        leafID += 1

    for i in range(N,len(data)):
        entry = data[i].strip("\n")
        
        parent = int(entry.split("->")[0])

        if parent in nodeChildren:
            nodeChildren[parent].append(leafID)
        else:
            nodeChildren[parent] = [leafID]
        leafID += 1
    print(nodeChildren, nodeSequence, leafID ,roundOfParsimony)
    return nodeChildren, nodeSequence, leafID ,roundOfParsimony
    

def SmallParsimony(nodeChildren,nodeSequence,root,N,round, finalScore):


    alphabetic = {}
    for i in range(root+1):
        alphabetic[i] = {'A':float('inf'),'C':float('inf'),'G':float('inf'),'T':float('inf')}
    
    # initiate the alphabetic for the leaves
    for i in range(N):
        alphabetic[i][nodeSequence[i][round]] = 0
    

    #calculate score
    for node in range(N,root+1):   
        for k in ['A','C','G','T']:
            # find minDaughter    
            minDaughter = float('inf')
            for i in ['A','C','G','T']:
                if k == i:
                    score = 0
                else:
                    score = 1 
                
                if minDaughter > alphabetic[nodeChildren[node][0]][i] + score:
                    minDaughter = alphabetic[nodeChildren[node][0]][i] + score
            
            # find minSon    
            minSon = float('inf')
            for i in ['A','C','G','T']:
                if k == i:
                    score = 0
                else:
                    score = 1 
                
                if minSon > alphabetic[nodeChildren[node][1]][i] + score:
                    minSon = alphabetic[nodeChildren[node][1]][i] + score
            
            #asign new score to alphabetic
            alphabetic[node][k] = minDaughter + minSon
        
     
    print(alphabetic)
    #calculate final score and the letter in the root
    rootletter = ""
    minLetter = float('inf')
    for i in ['A','C','G','T']:
        if minLetter > alphabetic[root][i]:
            minLetter = alphabetic[root][i]
            rootletter = i
    
    finalScore = finalScore + minLetter

    if root in nodeSequence:
        nodeSequence[root] = nodeSequence[root] + rootletter
    else:
        nodeSequence[root] =  rootletter

    print(nodeSequence)
    #find letter for other node:
    for node in range(root-1,N-1,-1):
        #Find the smallest value in node
        minLetter = float('inf')
        for letter in ['A','C','G','T']:
            if minLetter > alphabetic[node][letter]:
                minLetter = alphabetic[node][letter]
        letterToChoose = []
        for letter in ['A','C','G','T']:
            if alphabetic[node][letter] == minLetter:
                letterToChoose.append(letter)
        print(letterToChoose)
        #Find the letter of mother node
        for key in nodeChildren: 
            if node in nodeChildren[key]:
                motherLetter = nodeSequence[key][round]
        if motherLetter in letterToChoose:
            if node in nodeSequence:
                nodeSequence[node] = nodeSequence[node] + motherLetter
            else:
                nodeSequence[node] =  motherLetter
        else:
            if node in nodeSequence:
                nodeSequence[node] = nodeSequence[node] + letterToChoose[0]
            else:
                nodeSequence[node] =  letterToChoose[0]
    print(nodeSequence)
    print()
    return nodeSequence, finalScore
    
    

        
def EditDistance(sequence1,sequence2):
    distance = 0
    for i in range(len(sequence1)):
        if sequence1[i] != sequence2[i]:
            distance = distance + 1
    return distance




if __name__ == '__main__':
    with open("dataset_10335_10.txt",'r') as f:
        N = int(f.readline())
        data = f.readlines()
    
    nodeChildren, nodeSequence, root, roundOfParsimony = parsingData(data,N)

    
    finalScore = 0
    for round in range(roundOfParsimony): 
        nodeSequence, finalScore = SmallParsimony(nodeChildren,nodeSequence,root,N,round, finalScore)


    with open("results_dataset_10335_10.txt",'w') as f:
        f.write(str(finalScore) + "\n")

        for key in nodeChildren:
            for node in nodeChildren[key]:
                
                sequence1 = nodeSequence[key]
                sequence2 = nodeSequence[node]
                distance = EditDistance(sequence1,sequence2)
                f.write("{}->{}:{}\n".format(sequence1,sequence2,distance))
                f.write("{}->{}:{}\n".format(sequence2,sequence1,distance))

        

