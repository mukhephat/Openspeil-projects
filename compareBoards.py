import numpy as np


'''___________TIC TAC TOE SPECIFC____________'''

def unconvertBoard(board):
    #print('shape board unconvert',len(board))
    bList0 = board[0:9]
    #print(bList0)
    bListO=  board[9:18]
    #print(bListO)
    bListX = board[18:27]
    #print(bListX)
    bGrid = np.zeros((3,3),str)
    counter = -1
    for i in range(3):
        for j in range(3):
            counter +=1
            #print(counter)
            if bListO[counter] == '1':
                bGrid[i,j] = "O"
            elif bListX[counter] == '1':
                bGrid[i,j] = "X"
            #print(bGrid)
            #print(bListX)
            #print(bListO)
    return bGrid


def convertBoard(board):    
    board = np.array(board)
    #print('Type',type(board))
    bList0 = np.zeros(9)
    bListO= np.zeros(9)
    bListX = np.zeros(9)
    newList = []
    counter = -1

    for i in range(3):
        for j in range(3):
            counter +=1
            #print(counter)
            if board[i,j] == "":
                bList0[counter] = 1
            elif board[i,j] == "X":
                bListX[counter] = 1
            elif board[i,j] == "O":
                bListO[counter] = 1
            #print(bList0)
            #print(bListX)
            #print(bListO)
        new =  np.append(bList0,(bListO))
        #print(new)
        new =  np.append(new,(bListX))        
    #print('New appended list 0OX',new)
    #print('New convert',new)
    return new


def dictTTTstr():
    dictObj = {}
    dictObj['']  = 0
    dictObj['O'] = 1
    dictObj['X'] = 2    
    return dictObj  
    
def objectTTT():
    dictObj = {}
    dictObj[0] = [1,0,0]
    dictObj[1] = [0,1,0]
    dictObj[2] = [0,0,1]      
    return dictObj

def initTTT():
    dictObj = {}
    dictObj[''] = 0
    dictObj['X'] = 0
    dictObj['O'] = 0      
    return dictObj

def relationTTT():
    relations = {}
    relations[1] = [0,1,2]
    relations[2] = [3,4,5]
    relations[3] = [6,7,8]
    relations[4] = [0,3,6]
    relations[5] = [1,4,7]
    relations[6] = [2,5,8]
    relations[7] = [0,4,8]
    relations[8] = [2,4,6]
    return relations

def strTonum(boardStr):
    #takes the 3x3 string matrix and turns it into a 1x9 numeric list
    boardNum = []
    roww,coll = np.shape(boardStr)
    #print(roww,coll)
    dictT = dictTTTstr() 
    
    for i in range(roww):
        #print(i)
        pass
        for j in range(coll):
            #print(i,j)
            strObject = boardStr[i,j]
            item = dictT[strObject]
            boardNum.append(item)    
    return boardNum

def strToturp(boardStr):
    #takes the 3x3 string matrix and turns it into a 1x9 numeric list
    boardTurp = []
    roww,coll = np.shape(boardStr)
    #print(roww,coll)
    dictStr  = dictTTTstr()
    dictTurp = objectTTT()    
    for i in range(roww):
        #print(i)
        for j in range(coll):
            #print(i,j)
            strObject = boardStr[i,j]
            items = dictStr[strObject]
            item = dictTurp[items]
            boardTurp.append(item)
    boardTurpL = turntoLonglist(boardTurp)
    return boardTurp,boardTurpL

def turntoLonglist (boardTurp):
    n,m = np.shape(boardTurp)
    longList = []
    for o in range(n):
        roww = boardTurp[o]
        for p in range(m):
            item = roww[p]
            longList.append(item)
    return longList
    
def intprTTT(gameBoard):
    boardMatrix,boardList = strToturp(gameBoard)
    return boardMatrix #boardList


    
'''________________END TIC TAC TOE___________________'''    

def mapRel(board):
    boardNew = list(np.zeros(8))
    relations = relationTTT()
    boardN = strTonum(board)
    
    for i in relations:
        #print(i)
        hold = []
        for j in relations[i]:            
            hold.append(boardN[j])            
        boardNew[i-1] = hold
    return boardNew
        
def compareRel(mapped1,mapped2):
    count = 0
    for item1 in mapped1:
        for item2 in mapped2:
            if item1 == item2:
                count +=1
            #print (item1==item2,count)
    return count


def countObj(board):     
    n,m = np.shape(board)
    countObjs = initTTT()
    for o in range(n):
        for p in range (m):
            item = board[o,p]                    
            #print('item1',item)            
            countObjs[item] = countObjs.get(item,0)+1
    return  countObjs


def compareRots(board1,board2):
    origBoard = board1
    scores = []
    dictScore = {}  
    
    score1 = sum((compareBoards(board1,board2)))
    lBoard = hashBoard(board1)          
    dictScore[lBoard] = score1
    scores.append(score1) 
    
    board1T = np.transpose(board1)    
    score1 = sum(compareBoards(board1T,board2))    
    lBoard = hashBoard(board1T)
    dictScore[lBoard] = score1    
    scores.append(score1) 
    
    for i in range(3):  
        
        board1 = matrixRot(board1)
        score1 = sum(compareBoards(board1,board2))       
        lBoard = hashBoard(board1)
        dictScore[lBoard] = score1       
        scores.append(score1) 
        
        board1T = np.transpose(board1)
        score1 = sum(compareBoards(board1T,board2))        
        lBoard = hashBoard(board1T)
        dictScore[lBoard] = score1       
        scores.append(score1)
        moveList = rotateMove()
        #print('CB - dictScore',dictScore)
        #print('CB - scores',scores)
        #print('CB - moveList',moveList)
    return dictScore,scores,moveList


def hashBoard(boardList):
    board = convertBoard(boardList) #coverts from 3x3 to 1x27
    s = ''
    #print('Len',len(board))
    for i in board:
        string = str(int(i))
        s=s+string
    #print(s)
    return s

def compareBoards(board11,board22):
    board1 =  intprTTT(board11)
    board2 = intprTTT(board22)   
    dirVal,sameObj,sameRelat = directSim(board11,board22)    
    maxO = 9
    maxSObj = 9
    maxRel = 32
    w1 = 0.2
    w2 = 0.3
    w3 = 0.5
    return [w1*dirVal/maxO,w2*sameObj/maxSObj,w3*sameRelat/maxRel]

def transposeMat(board):
    boardTr = np.matrix(board)
    boardTr = board.transpose()    
    return boardTr


def matrixRot(board):  
    matTest = np.array(list(list(x)[::-1] for x in zip(*board)))
    return matTest


def directSim(board11,board22):
    board1 =  intprTTT(board11)
    board2 = intprTTT(board22)
    count = 0
    #count similarity of objects in the same physical space i.e. direct similarity
    for i in range(len(board1)):
        #print(board1[i], board2[i])
        if (board1[i] == board2[i]):
            count+=1
    countOB1 = countObj(board11)
    countOB2 = countObj(board22)
    #print('OB1',countOB1)
    #print('OB2',countOB2)
    summer = 0    
    #count number of all objects of the same type 
    for item in countOB1:
        #print(item)
        summer += min(countOB1[item],countOB2[item])
        #print('similar objects',summer)
    boardRel1 = mapRel(board11)
    boardRel2 = mapRel(board22)
    value = compareRel(boardRel1,boardRel2)    
    
    return count,summer,value

def rotateMove():
    B0 = np.array(([[0,1,2],[3,4,5],[6,7,8]]))
    #print('Matrix\n',B0)
    moveList = []
    
    BT = transposeMat(B0)
    moveList.append(B0)
    moveList.append(BT)
    #print('\nMatrixBT\n',BT)
    for i in range(3):
        #print('I',i)
        B0 =  matrixRot(B0)
        holder = (B0)
        moveList.append(holder)
        #print('\nMatrixB0\n',B0)
        
        BT = transposeMat(B0)
        holder = (BT)
        moveList.append(holder)
        #print('\nMatrixBT\n',BT)
    dictionary = {}
    counter = 0
    for i in moveList:
        dictionary[counter] = i
        counter+=1
    return dictionary
    
#print('MoveList\n',rotateMove())

print('The End - Compare Board')   

'''
boardList = [['','',''],['','O','X'],['' ,'' ,'' ]]
#boardList = [['O','X','O'],['','O',''],['X' ,'' ,'' ]]
#boardList = [['X','O','O'],['X','X','O'],['O' ,'X' ,'O' ]]
#boardList = [['X','O','X'],['O','X','O'],['X' ,'O' ,'X' ]]
#boardList = [['X','',''],['O','O',''],['X' ,'' ,'X' ]]

#print(boardList)
board1 = np.array(boardList)
print(board1)
#boardList = [['X','X','O'],['X','O',''],['' ,'' ,'' ]]
#boardList = [['X','O','O'],['X','X','O'],['O' ,'X' ,'O' ]]
#boardList = [['X','O','X'],['O','X','O'],['X' ,'O' ,'X' ]]
#boardList = [['X','','X'],['O','O',''],['X' ,'' ,'' ]]
boardList = [['','',''],['X','O',''],['' ,'' ,'' ]]
#boardList = [[1,2,3],[4,5,6],[7,8,9]]
board2 = np.array(boardList)
print(board2)
#print(boardList)
#print(sum(intprTTT(board)))

#compare = compareBoards(board1, board2)
#print(compare)

#print('\nOriginal\n',board2)
transp,score,moves = compareRots(board1,board2)
print('\nBoards\n',transp)
print(score)
#conve = convertBoard(board2)
#print(conve)

for i in transp:
    #print('i',len(i),'\n',i)
    print('The Value',transp[i])
    indeX  = []
    for j in i:
        indeX.append(j)
    print(indeX)
    
    a =unconvertBoard(indeX)
    #print('iList\n',i)
    
    
    print('unconverted\n',a)
    
print(transp['[0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]'])
'''