from collections import defaultdict


# Create a graph to implement Djistra's shortest path algorithm
class Graph():
    def __init__(self):
        '''
        self.edges is a dict of all possible next nodes
        self.weight hass all the weights between two nodes.
        with the two nodes as a tuple as the key
        '''
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edges(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node,to_node)] = weight
        self.weights[(to_node,from_node)] = weight

def dijsktra(tree, initial, end):
    # shortest path is a dict of nodes 
    # whose value is a tuple of (previous node, weight)
    graph = Graph()
    for edge in tree:
        graph.add_edges(*edge)  #a single star means that the variable "edge" will be a tuple of extra parameters that were supplied to the funciton
    
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node,next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node,weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node,weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key = lambda k: next_destinations[k][1])

    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    # reverse path
    path = path[::-1]
    return path

def addEdge(tree,path,distanceFromStartNode,oldLeafToAddBack,currentLimbLength,newNodeLabel,):
    # print(path)
    # print(tree)
    # print(distanceFromStartNode,oldLeafToAddBack,currentLimbLength,newNodeLabel)
    dist = 0 
    for i in range(1,len(path)):
            for edge in tree:
                if (edge[0] == path[i-1]) & (edge[1] == path[i]):
                    dist = dist + edge[2]
            
            if distanceFromStartNode == dist: 
                # add the leaf back
                tree.append((int(path[i]),int(oldLeafToAddBack),int(currentLimbLength)))
                break
            elif dist > distanceFromStartNode: 
                # add the leaf back
                tree.append((int(newNodeLabel),int(oldLeafToAddBack),int(currentLimbLength)))
                # add edge from the new label to i 
                tree.append((int(newNodeLabel),int(path[i]),int(dist-distanceFromStartNode)))
            
                distance1 = tree[-1][2]
 
                for edge in tree:
                    if (edge[0] == path[i-1]) and (edge[1] == path[i]):
                        distance2 = edge[2]
      
                tree.append((path[i-1],newNodeLabel,abs(distance2-distance1)))
                
                nonDuplicateTree = list(set(tree))
                tree = nonDuplicateTree[:]
                tree.remove((path[i-1],path[i],distance2)) 
                break
    return tree



def limbLength(matrix):
    n = len(matrix)
    limb = float("inf")
    for i in range(n):
        for j in range(n):
            if (i != n-1) and (j != n-1) and (i!=j):
                dist = (matrix[i][n-1] + matrix[n-1][j] - matrix[i][j]) / 2
                if dist < limb:
                    limb = dist
    return limb


def additivePhylogenyStack(matrix,n):
    newNodeLabel = n
    # if only two nodes were left, return the matrix
    lengthOfCurrentMatrix = len(matrix) 
    
    if lengthOfCurrentMatrix == 2:
        # return consisting of a single edge of length
        tree = [(0,1,matrix[0][1])]
        return tree, newNodeLabel

    # creat the bold matrix
    currentLimbLength = limbLength(matrix)
    for j in range(lengthOfCurrentMatrix-1):
        matrix[j][lengthOfCurrentMatrix-1] = matrix[j][lengthOfCurrentMatrix-1] - currentLimbLength
        matrix[lengthOfCurrentMatrix-1][j] = matrix[j][lengthOfCurrentMatrix-1]

    
    # the new node is between i and k, distance to i is x, and the removed leaf is "lengthOfCurrentMatrix-1", and the limbLength
    startNode, endNode, distanceFromStartNode = findIK(matrix)

    # remove the last node of the matrix
    newMatrix = []
    for i in range(lengthOfCurrentMatrix -1):
        newMatrix.append(matrix[i][:-1])
    matrix = newMatrix[:]

    # start the recursion
    tree,newNodeLabel = additivePhylogenyStack(matrix,n)
    
    # # v <- the (potentially new) node in tree at distance x from i on the path between i and k
    # add leaf n back to tree by creating a limb (v,n) of length limbLength

    #   print(startNode, endNode, distanceFromStartNode,lengthOfCurrentMatrix-1, currentLimbLength)
    # use dijsktra's shorted path algorithm to find nodes on the path from i to k
    path = dijsktra(tree,startNode,endNode)
    
    tree = addEdge(tree,path, distanceFromStartNode,lengthOfCurrentMatrix-1, currentLimbLength,newNodeLabel)
    
    newNodeLabel = newNodeLabel + 1
    return tree, newNodeLabel


    
def findIK(matrix):
    lengthOfCurrentMatrix = len(matrix) 
    for i in range(lengthOfCurrentMatrix-1):
        for k in range(lengthOfCurrentMatrix-1):
            if matrix[i][k] == matrix[i][lengthOfCurrentMatrix-1] + matrix[lengthOfCurrentMatrix-1][k]:
                return i,k, matrix[i][lengthOfCurrentMatrix-1]
    
def generateOutput(tree):
    newTree = []
    for edge in tree:
        newTree.append(edge)
        newTree.append((edge[1],edge[0],edge[2]))
    sortedTree = sorted(newTree, key=lambda x: (x[0], x[1]))
    with open("results_coronavirus_distance_matrix_additive.txt","w") as f:
        for edge in sortedTree:
            f.write("{}->{}:{}\n".format(edge[0],edge[1],edge[2]))



# limb length Theorem: given an additive matrix D and a leaf j, LimbLength(j) is equal to the minimum value of (Di,j + Dj,k - Di,k)/2.
# over all leaves i and k
if __name__ == '__main__':
    with open("coronavirus_distance_matrix_additive.txt","r") as f:
        n = int(f.readline().strip())
        matrixInput = f.readlines()

    #generate initial Matrix
    matrix = []
    for i in matrixInput:
        rowList = []
        for j in i.strip().split("\t"):
            rowList.append(int(j))
        matrix.append(rowList)
  
    tree,newNodeLabel = additivePhylogenyStack(matrix,n)
    generateOutput(tree)


    


 
    
