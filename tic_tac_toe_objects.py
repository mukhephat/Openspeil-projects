import numpy as np

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
        
def intprTTT(gameBoard):
    boardMatrix,boardList = strToturp(gameBoard)
    return boardMatrix #boardList

def countObj(board):
     
    n,m = np.shape(board)
    countObjs = initTTT()
    for o in range(n):
        for p in range (m):
            item = board[o,p]                    
            #print('item1',item)            
            countObjs[item] = countObjs.get(item,0)+1
    return  countObjs

def weighVal(val,weights):
    counter=0
    summer = 0
    for i in val:
        print(i)
        summer += i*weights[counter]
        print('Summer',summer)
        counter+=1
    return summer
    
def compareBoards(board11,board22):
    board1 =  intprTTT(board11)
    board2 = intprTTT(board22)
    count = 0
    #count similarity of objects in the same physical space i.e. direct similarity
    for i in range(len(board1)):
        if board1[i] == board2[i]:
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
    num = count/9,summer/9,value/8
    weigh=(0.3,0.2,0.5)
    
    returnVal = weighVal(num,weigh)
    print(count,summer,value)
    
    return returnVal
    



boardList = [['','',''],['','',''],['' ,'' ,'X' ]]
boardList = [['O','X','O'],['','O',''],['X' ,'' ,'' ]]
boardList = [['X','O','O'],['X','X','O'],['O' ,'O' ,'O' ]]
boardList = [['X','O','X'],['O','X','O'],['X' ,'O' ,'X' ]]
boardList = [['X','',''],['O','O',''],['X' ,'' ,'X' ]]
#print(boardList)
board1 = np.array(boardList)
print(board1)
#boardList = [['X','X','O'],['X','O',''],['' ,'' ,'' ]]
boardList = [['X','O','O'],['X','X','O'],['O' ,'O' ,'O' ]]
boardList = [['X','O','X'],['O','X','O'],['X' ,'O' ,'X' ]]
boardList = [['X','','X'],['O','O',''],['X' ,'' ,'' ]]
board2 = np.array(boardList)
print(board2)
#print(boardList)
#print(sum(intprTTT(board)))

compare = compareBoards(board1, board2)
print(compare)

