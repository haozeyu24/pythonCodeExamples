
#https://en.wikipedia.org/wiki/UPGMA#Working_example


def findMinValue(matrix):
    min = float('inf')
    node1 = 0
    node2 = 0
    n = len(matrix)
    for i in range(n-1):
        for j in range(i+1,n):
            if min > matrix[i][j]:
                min = matrix[i][j]
                node1 = i 
                node2 = j

    return min, node1, node2

def UPGMA(matrix,n):
    #initiation
    originalMatrix = matrix[:]
    clusters = []
    nodeAges = {}
    for i in range(n):
        clusters.append((0,[i]))
        nodeAges[i] = 0
    clusterNodeIDs = [i for i in range(n)]

    nextNodeID = n
    edges = set()
    
    while len(matrix) > 1:
        print("The current matrix is")
        print(matrix)

        min, node1, node2 = findMinValue(matrix)
        print("current nodes to eliminate")
        print(node1,node2)

        nextNodeAge = min/2
        nodeAges[nextNodeID] = nextNodeAge
        print("current Age")
        print(nodeAges)

        #updateEdges
        edges.add((clusterNodeIDs[node1],nextNodeID))
        edges.add((clusterNodeIDs[node2],nextNodeID))
        print("the current edges are")
        print(edges)

        #update clusterNodeID
        print("clusterID before update")
        print(clusterNodeIDs)
        remove1 = clusterNodeIDs[node1]
        remove2 = clusterNodeIDs[node2]
        clusterNodeIDs.remove(remove1)
        clusterNodeIDs.remove(remove2)
        clusterNodeIDs.append(nextNodeID)
        print("current cluster node ID")
        print(clusterNodeIDs)

        #update clusters
        newCluster = (nextNodeAge,clusters[node1][1] + clusters[node2][1])
        remove1 = clusters[node1]
        remove2 = clusters[node2]
        clusters.remove(remove1)
        clusters.remove(remove2)
        clusters.append(newCluster)
        print("current cluster is")
        print(clusters)

        #create a list of node to visit (remove the identified nodes)
        nodesCurrentMatrix = [i for i in range(len(matrix))]
        nodesCurrentMatrix.remove(node1)
        nodesCurrentMatrix.remove(node2)
        print("nodes to visit")
        print(nodesCurrentMatrix)

        #initiate new matrix
        newMatrix = [[0]*(len(nodesCurrentMatrix)+1) for i in range(len(nodesCurrentMatrix)+1)]
        
        #update the next matrix
        for i in range(len(newMatrix)-2):
            for j in range(i+1,len(newMatrix)-1):
                index1 = nodesCurrentMatrix[i]
                index2 = nodesCurrentMatrix[j]
                newMatrix[i][j] = matrix[index1][index2]
                newMatrix[j][i] = newMatrix[i][j]
        #update the next matrix: recalculate the distance to the new cluster
        for i in range(len(newMatrix)-1):
            j = len(newMatrix) -1
            cluster1tomerge = clusters[i][1]
            cluster2tomerge = clusters[j][1]
            sum = 0
            for node1 in cluster1tomerge:
                for node2 in cluster2tomerge:
                    sum = sum + originalMatrix[node1][node2]
            average = sum / (len(cluster1tomerge)*len(cluster2tomerge))
            newMatrix[i][j] = average
            newMatrix[j][i] = newMatrix[i][j]
            

        #     matrix[i][len(matrix)-1] = 
        
        matrix = newMatrix[:]
        nextNodeID += 1
        print()
    return  edges,nodeAges






if __name__ == '__main__':
    with open("dataset_10332_8.txt","r") as f:
        n = int(f.readline().strip())
        matrixInput = f.readlines()

    #generate initial Matrix
    matrix = []
    for i in matrixInput:
        rowList = []
        for j in i.strip().split("\t"):
            rowList.append(int(j))
        matrix.append(rowList)

    edges, nodeAges = UPGMA(matrix,n)

    newedges = set()
    for edge in edges:
        newedges.add(edge)
        newedges.add((edge[1],edge[0]))
    newedges= sorted(newedges, key = lambda x:(x[0],x[1]))
    print(newedges)

    with open("results_UPGMA.txt",'w') as f:
        for edge in newedges:
            f.write("{}->{}:{:.3f}\n".format(edge[0],edge[1],abs(nodeAges[edge[0]]-nodeAges[edge[1]])))



    
    