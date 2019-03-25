import random

class ChessBoard():
    def __init__(self):
        self.board=[[None for i in range(8)] for j in range(8)]
        self.VALUES={'PAWN':1,'ROOK':3,'KNIGHT':2,'BISHOP':2,'QUEEN':5,'KING':10}
        #PIJUNI
        for i,color in zip([1,6],['BLACK','WHITE']):
            for j in range(8):
                self.board[i][j]=Pawn((i,j),color,self)

        #OSTALI
        thisModule = __import__('chess')
        for i,color in zip([0,7],['BLACK','WHITE']):
            for j,piece in zip(range(8),['Rook','Knight','Bishop','Queen','King','Bishop','Knight','Rook']):
                ClassPiece = getattr(thisModule, piece)
                self.board[i][j]=ClassPiece((i,j),color,self)


    def isEmpty(self,position):
        if position[0]<0 or position[1]<0:
            return False
        try:
            if self.board[position[0]][position[1]]==None:
                return True
        except:
            return False
        return False
    def getPiece(self,position):
        if position[0]<0 or position[1]<0:
            return None
        return self.board[position[0]][position[1]]

    def move(self,fromPos,toPos):
        if self.getPiece(fromPos) == None:
            raise ValueError("No chesspiece on that position")
        if toPos in self.getPiece(fromPos).getMoves():
            self.board[toPos[0]][toPos[1]]=self.board[fromPos[0]][fromPos[1]]
            self.board[toPos[0]][toPos[1]].position=toPos
            self.board[fromPos[0]][fromPos[1]]=None
        else:
            raise ValueError("Illegal move")
    def getAllMoves(self,color):
        # VRACA (FROM,TO,VALUE)
        moves=[]
        for i in range(8):
            for j in range(8):
                try:
                    if self.board[i][j].color==color:
                        pieceMoves=self.board[i][j].getMoves()
                        for move in pieceMoves:

                            eaten=self.getPiece(move)
                            if eaten!=None:
                                moves.append(((i, j), move, self.VALUES[eaten.LABEL]))
                            else:
                                moves.append(((i, j), move, 0))

                except:
                    pass
        return moves
    def getBestMove(self,depth,color,upperBest=None):
        if depth==1:
            myMoves = self.getAllMoves(color)
            myMoves=sorted(myMoves,key=lambda x:x[2])

            return myMoves[0]
        currentBestMoves=[]
        currentBestValue=-10000
        currentBestMiniValue=None
        myMoves = self.getAllMoves(color)
        for myMove in myMoves:
            copyBoard=self.copy()
            copyBoard.move(myMove[0],myMove[1])
            if color == 'WHITE':
                opponentMove = copyBoard.getBestMove(depth-1,'BLACK',currentBestMiniValue)
            else:
                opponentMove = copyBoard.getBestMove(depth-1,'WHITE',currentBestMiniValue)
            if myMove[2]-opponentMove[2]>currentBestValue:
                currentBestValue=myMove[2]-opponentMove[2]
                currentBestMoves=[]
                currentBestMoves.append(myMove)
                currentBestMiniValue=myMove[2]
                #PRUNING

                if upperBest!=None:
                    if depth%2==0 and opponentMove[2]>upperBest:
                        break
                    if depth % 2 == 1 and opponentMove[2] < upperBest:
                        break

            elif myMove[2]-opponentMove[2]==currentBestValue:
                currentBestMoves.append(myMove)

        if len(currentBestMoves)>1:
            currentBestMove=currentBestMoves[random.randint(0,len(currentBestMoves)-1)]
        else:
            currentBestMove=currentBestMoves[0]
        currentBestMove=(currentBestMove[0],currentBestMove[1],currentBestValue)
        return currentBestMove
    def checkCheck(self):
        whiteMoves=self.getAllMoves('WHITE')
        blackMoves=self.getAllMoves('BLACK')

        whiteKing=None
        blackKing=None
        for i in range(8):
            for j in range(8):
                piece=self.getPiece((i,j))
                if piece!=None:
                    if piece.LABEL=='KING':
                        if piece.color=='WHITE':
                            whiteKing=piece
                        else:
                            blackKing=piece
        checks=[]
        mates=[]
        for whiteMove,blackMove in zip(whiteMoves,blackMoves):
            if whiteKing.position==blackMove[1]:
                checks.append(whiteKing.position)
            if blackKing.position==whiteMove[1]:
                checks.append(blackKing.position)

        for check in checks:
            checkedKing=self.getPiece(check)
            kingsMoves=checkedKing.getMoves()

            if checkedKing.color=='WHITE':
                for blackMove in blackMoves:
                    for kingsMove in kingsMoves:
                        if blackMove[1]==kingsMove:
                            kingsMoves.remove(kingsMove)
                for kingsMove in kingsMoves:
                    pieceOnMove=self.getPiece(kingsMove)
                    if pieceOnMove!=None:
                        if pieceOnMove.color=='WHITE':
                            kingsMoves.remove(kingsMove)
            else:
                for whiteMove in whiteMoves:
                    for kingsMove in kingsMoves:
                        if whiteMove[1]==kingsMove:
                            kingsMoves.remove(kingsMove)

                for kingsMove in kingsMoves:
                    pieceOnMove = self.getPiece(kingsMove)
                    if pieceOnMove != None:
                        if pieceOnMove.color == 'BLACK':
                            kingsMoves.remove(kingsMove)

            if len(kingsMoves) == 0:
                mates.append(check)

        return checks,mates
    def copy(self):
        retCopy=ChessBoard()
        for i in range(8):
            for j in range(8):
                if self.board[i][j]!=None:
                    retCopy.board[i][j]=self.board[i][j].copy(retCopy)
                else:
                    retCopy.board[i][j]=None
        return retCopy
    def __str__(self):
        retVal='    a   b   c   d   e   f   g   h  \n'
        for i in range(8):
            retVal+=str(8-i)+"  "
            for j in range(8):
                if self.isEmpty((i,j)):
                    retVal+="    "
                else:
                    retVal+=str(self.board[i][j])
            retVal+='\n'

        return retVal
    def numberToLetter(position):
        numberToLetter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return str(numberToLetter[position[1]]) + str(8 - position[0])
    def letterToNumber(position):
        letterToNumber = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - int(position[1]), letterToNumber[position[0]])

class ChessPiece():
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
    def getMoves(self):
        pass
    def forward(self,amount,position):
        if self.color=='BLACK':
            return (position[0]+amount,position[1])
        return (position[0]-amount,position[1])
    def back(self,amount,position):
        if self.color=='BLACK':
            return (position[0]-amount,position[1])
        return (position[0]+amount,position[1])
    def left(self,amount,position):
        if self.color=='BLACK':
            return (position[0],position[1]+amount)
        return (position[0],position[1]-amount)
    def right(self,amount,position):
        if self.color=='BLACK':
            return (position[0],position[1]-amount)
        return (position[0],position[1]+amount)

class Pawn(ChessPiece):
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
        self.LABEL = 'PAWN'
    def copy(self,newBoard):
        retCopy=Pawn(self.position,self.color,newBoard)
        return retCopy
    def getMoves(self):
        moves=[]
        #OBICAN SKOK ZA JEDAN
        newPosition=self.forward(1,self.position)
        if self.board.isEmpty(newPosition):
            moves.append(newPosition)
            # SKOK ZA DVA UNAPRIJED
            if self.color == 'BLACK':
                if self.position[0] == 1:
                    newPosition = self.forward(2, self.position)
                    if self.board.isEmpty(newPosition):
                        moves.append(newPosition)
            elif self.color == 'WHITE':
                if self.position[0] == 6:
                    newPosition = self.forward(2, self.position)
                    if self.board.isEmpty(newPosition):
                        moves.append(newPosition)
        #JEDENJE U DIJAGONALI
        newPosition=self.right(1,self.forward(1,self.position))
        if self.board.isEmpty(newPosition)!=True:
            try:
                if self.board.getPiece(newPosition).color!=self.color:
                            moves.append(newPosition)
            except:
                pass
        newPosition = self.left(1, self.forward(1, self.position))
        if self.board.isEmpty(newPosition) != True:
            try:
                if self.board.getPiece(newPosition).color != self.color:
                    moves.append(newPosition)
            except:
                pass

        return moves
    def __str__(self):
        if self.color=='WHITE':
            return 'P[ ]'
        return 'P[#]'

class Rook(ChessPiece):
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
        self.LABEL = 'ROOK'
    def copy(self,newBoard):
        retCopy=Rook(self.position,self.color,newBoard)
        return retCopy
    def getMoves(self):
        moves=[]
        for f in [self.forward, self.back, self.left, self.right]:
            for i in range(1,8):
                newPosition=f(i,self.position)
                if self.board.isEmpty(newPosition):
                    moves.append(newPosition)
                elif self.board.isEmpty(newPosition)!=True:
                    try:
                        if self.board.getPiece(newPosition).color!=self.color:
                            moves.append(newPosition)
                        break
                    except:
                        pass
                else:
                    break


        return moves
    def __str__(self):
        if self.color=='WHITE':
            return 'R[ ]'
        return 'R[#]'

class Knight(ChessPiece):
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
        self.LABEL = 'KNIGHT'
    def copy(self,newBoard):
        retCopy=Knight(self.position,self.color,newBoard)
        return retCopy
    def getMoves(self):
        moves = []
        for f1 in [self.forward, self.back]:
            for f2 in [self.left, self.right]:
                newPosition=f2(1,f1(2,self.position))
                if self.board.isEmpty(newPosition):
                    moves.append(newPosition)
                elif self.board.isEmpty(newPosition)!=True:
                    try:
                        if self.board.getPiece(newPosition).color!=self.color:
                            moves.append(newPosition)
                    except:
                        pass

        for f1 in [self.left, self.right]:
            for f2 in [self.forward, self.back]:
                newPosition = f2(1, f1(2, self.position))
                if self.board.isEmpty(newPosition):
                    moves.append(newPosition)
                elif self.board.isEmpty(newPosition)!=True:
                    try:
                        if self.board.getPiece(newPosition).color!=self.color:
                            moves.append(newPosition)
                    except:
                        pass

        return moves
    def __str__(self):
        if self.color=='WHITE':
            return 'K[ ]'
        return 'K[#]'

class Bishop(ChessPiece):
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
        self.LABEL = 'BISHOP'

    def copy(self, newBoard):
        retCopy = Bishop(self.position, self.color, newBoard)
        return retCopy
    def getMoves(self):
        moves=[]
        for f1 in [self.forward,self.back]:
            for f2 in [self.left,self.right]:
                for i in range(1,8):
                    newPosition=f2(i,f1(i,self.position))
                    if self.board.isEmpty(newPosition):
                        moves.append(newPosition)
                    elif self.board.isEmpty(newPosition) != True:
                        try:
                            if self.board.getPiece(newPosition).color != self.color:
                                moves.append(newPosition)
                            break
                        except:
                            pass
                    else:
                        break
        return moves

    def __str__(self):
        if self.color=='WHITE':
            return 'B[ ]'
        return 'B[#]'

class Queen(ChessPiece):
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
        self.LABEL = 'QUEEN'
    def copy(self,newBoard):
        retCopy=Queen(self.position,self.color,newBoard)
        return retCopy
    def getMoves(self):
        moves = []
        for f in [self.forward, self.back, self.left, self.right]:
            for i in range(1, 8):
                newPosition = f(i, self.position)
                if self.board.isEmpty(newPosition):
                    moves.append(newPosition)
                elif self.board.isEmpty(newPosition) != True:
                    try:
                        if self.board.getPiece(newPosition).color != self.color:
                            moves.append(newPosition)
                        break
                    except:
                        pass
                else:
                    break

        for f1 in [self.forward,self.back]:
            for f2 in [self.left,self.right]:
                for i in range(1,8):
                    newPosition=f2(i,f1(i,self.position))
                    if self.board.isEmpty(newPosition):
                        moves.append(newPosition)
                    elif self.board.isEmpty(newPosition) != True:
                        try:
                            if self.board.getPiece(newPosition).color != self.color:
                                moves.append(newPosition)
                            break
                        except:
                            pass
                    else:
                        break

        return moves
    def __str__(self):
        if self.color=='WHITE':
            return 'Q[ ]'
        return 'Q[#]'

class King(ChessPiece):
    def __init__(self,position,color,board):
        self.position=position
        self.color = color
        self.board=board
        self.LABEL='KING'
    def copy(self,newBoard):
        retCopy=King(self.position,self.color,newBoard)
        return retCopy
    def getMoves(self):
        moves = []
        for f in [self.forward, self.back, self.left, self.right]:
            newPosition = f(1, self.position)
            if self.board.isEmpty(newPosition):
                moves.append(newPosition)
            elif self.board.isEmpty(newPosition) != True:
                try:
                    if self.board.getPiece(newPosition).color != self.color:
                        moves.append(newPosition)
                except:
                    pass

        for f1 in [self.forward, self.back]:
            for f2 in [self.left, self.right]:
                newPosition = f2(1, f1(1, self.position))
                if self.board.isEmpty(newPosition):
                    moves.append(newPosition)
                elif self.board.isEmpty(newPosition) != True:
                    try:
                        if self.board.getPiece(newPosition).color != self.color:
                            moves.append(newPosition)
                    except:
                        pass

        return moves
    def __str__(self):
        if self.color=='WHITE':
            return 'K[ ]'
        return 'K[#]'

if __name__=='__main__':
    chessboard=ChessBoard()
    #chessboard.board[2][1]=chessboard.board[6][1]
    #chessboard.board[4][2]=chessboard.board[6][2]
    #chessboard.board[6][2]=None
    #chessboard.board[1][3] = None
    print(chessboard)
    #print(chessboard.getPiece((0,4)).getMoves())
    letterToNumber={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    numberToLetter = {0:'a', 1:'b', 2:'c',3: 'd', 4:'e',5: 'f', 6:'g', 7:'h'}

    while(True):
        #print("Moj najbolji potez je:")
        #print(chessboard.getBestMove(4, 'WHITE'))
        bestMove=chessboard.getBestMove(5, 'WHITE')

        print("%s s %s na %s"%(chessboard.getPiece(bestMove[0]),ChessBoard.numberToLetter(bestMove[0]),ChessBoard.numberToLetter(bestMove[1])))
        print("Value mog poteza je: %d"%(bestMove[2]))
        chessboard.move(bestMove[0],bestMove[1])
        print(chessboard)

        while(True):
            try:
                line = input()
                positions = line.split(" ")
                fromPos = ChessBoard.letterToNumber(positions[0])
                toPos = ChessBoard.letterToNumber(positions[1])

                chessboard.move(fromPos, toPos)
                break
            except Exception as e:
                print(e)
        print(chessboard)

