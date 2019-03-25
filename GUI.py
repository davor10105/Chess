from chess import *
import pygame

WINDOW_SIZE=(720,720)
SCREEN_SIZE=(1080,720)
SQUARE_MARGIN=2

BLACK = (0, 0, 0)
WHITE = (255, 191, 128)
BROWN=(153, 51, 0)
GREEN = (0, 255, 0)
RED=(255,0,0)
ORANGE=(255,165,0)

pygame.init()
pygame.font.init()

font=pygame.font.SysFont('Arial',12)
#board=pygame.display.set_mode(WINDOW_SIZE)
screen=pygame.display.set_mode(SCREEN_SIZE)
board=pygame.Surface(WINDOW_SIZE)
textSurface=font.render('Drag and drop chesspieces to move',False,(255,255,255))
textBackground=pygame.Surface((SCREEN_SIZE[0]-WINDOW_SIZE[0],SCREEN_SIZE[1]))

pygame.display.set_caption("CHESSOLINO")
pygame.display.set_icon(pygame.image.load('./icons/pawn_icon.png'))

clock=pygame.time.Clock()
run=True

clicked=False
textForTextBox=[]
checks=[]
mates=[]

startMovePos=None
endMovePos=None

bestMove=(None,None)

myTurn=True

#chessboard=ChessBoard()

def square(offset):
    return [WINDOW_SIZE[0]/8*offset[0]+SQUARE_MARGIN,WINDOW_SIZE[1]/8*offset[1]+SQUARE_MARGIN,WINDOW_SIZE[0]/8-2*SQUARE_MARGIN,WINDOW_SIZE[1]/8-2*SQUARE_MARGIN]

def drawPiece(position):
    piece=chessboard.getPiece(position)
    if piece!=None:
        board.blit(image_storage[piece.color.lower()][piece.LABEL.lower()], (square((j, i))))

def resetVariables():
    global clicked,checks,mates,startMovePos,endMovePos,bestMove,myTurn

    clicked = False
    checks = []
    mates = []

    startMovePos = None
    endMovePos = None

    bestMove = (None, None)

    myTurn = True

image_storage={}
for color in ['white','black']:
    color_storage={}
    for piece in ['pawn','rook','knight','bishop','king','queen']:
        color_storage[piece]=pygame.transform.scale(pygame.image.load("./icons/"+color+'_'+piece+'.png'),(WINDOW_SIZE[0]//8,WINDOW_SIZE[1]//8))
    image_storage[color]=color_storage

retry=True
while(retry):
    chessboard=ChessBoard()
    resetVariables()
    run=True
    while(run):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                retry=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if clicked==False:
                    clicked=True
                    endMovePos=None
                    bestMove = (None, None)
                    clickPosition=pygame.mouse.get_pos()

                    startMovePos=(int(clickPosition[1]/WINDOW_SIZE[1]*8),int(clickPosition[0]/WINDOW_SIZE[0]*8))
            elif event.type == pygame.MOUSEBUTTONUP:
                if clicked==True:
                    clicked=False

                    clickPosition = pygame.mouse.get_pos()

                    endMovePos = (int(clickPosition[1] / WINDOW_SIZE[1] * 8), int(clickPosition[0] / WINDOW_SIZE[0] * 8))

                    try:
                        chessboard.move(startMovePos,endMovePos)

                        myTurn=False
                    except Exception as e:
                        print(e)
                        startMovePos=None
                        endMovePos=None

                    try:
                        checks, mates = chessboard.checkCheck()
                    except:
                        run = False

        board.fill(BLACK)

        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    pygame.draw.rect(board,WHITE,[WINDOW_SIZE[0]/8*j+SQUARE_MARGIN,WINDOW_SIZE[1]/8*i+SQUARE_MARGIN,WINDOW_SIZE[0]/8-2*SQUARE_MARGIN,WINDOW_SIZE[1]/8-2*SQUARE_MARGIN])
                else:
                    pygame.draw.rect(board, BROWN,
                                     [WINDOW_SIZE[0] / 8 * j + SQUARE_MARGIN, WINDOW_SIZE[1] / 8 * i + SQUARE_MARGIN,
                                      WINDOW_SIZE[0] / 8 - 2 * SQUARE_MARGIN, WINDOW_SIZE[1] / 8 - 2 * SQUARE_MARGIN])

                if (i,j)==startMovePos:
                    pygame.draw.rect(board, GREEN, square((startMovePos[1], startMovePos[0])))
                if (i,j)==endMovePos:
                    pygame.draw.rect(board, GREEN, square((endMovePos[1], endMovePos[0])))
                if (i, j) == bestMove[0]:
                    pygame.draw.rect(board, RED, square((bestMove[0][1], bestMove[0][0])))
                if (i, j) == bestMove[1]:
                    pygame.draw.rect(board, RED, square((bestMove[1][1], bestMove[1][0])))

                for k in range(len(checks)):
                    if checks[k]==(i,j):
                        pygame.draw.rect(board, ORANGE, square((checks[k][1], checks[k][0])))
                for k in range(len(mates)):
                    if mates[k]==(i,j):
                        pygame.draw.rect(board, BLACK, square((mates[k][1], mates[k][0])))

                drawPiece((i,j))

        #DODAVANJE SCREENOVA ZA GAME I TEXT
        screen.blit(board, (0, 0))
        textBackground.fill((64, 64, 64))
        textBackground.blit(textSurface,(0,0))
        screen.blit(textBackground,(WINDOW_SIZE[0],0))

        pygame.display.flip()

        if myTurn==False:
            bestMove=chessboard.getBestMove(4,'BLACK')
            eatenPiece = chessboard.getPiece(bestMove[1])
            chessboard.move(bestMove[0], bestMove[1])

            try:
                checks,mates = chessboard.checkCheck()
            except:
                run=False

            myTurn=True

        clock.tick(60)


    bigFont=pygame.font.SysFont('Arial',72)
    #textSurface=bigFont.render('GAME OVER click to restart',False,(255,255,255))
    run=True
    while(run):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                retry = False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                print("kita")
                run=False

            board.fill(BLACK)

            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 0:
                        pygame.draw.rect(board, WHITE,
                                         [WINDOW_SIZE[0] / 8 * j + SQUARE_MARGIN, WINDOW_SIZE[1] / 8 * i + SQUARE_MARGIN,
                                          WINDOW_SIZE[0] / 8 - 2 * SQUARE_MARGIN, WINDOW_SIZE[1] / 8 - 2 * SQUARE_MARGIN])
                    else:
                        pygame.draw.rect(board, BROWN,
                                         [WINDOW_SIZE[0] / 8 * j + SQUARE_MARGIN, WINDOW_SIZE[1] / 8 * i + SQUARE_MARGIN,
                                          WINDOW_SIZE[0] / 8 - 2 * SQUARE_MARGIN, WINDOW_SIZE[1] / 8 - 2 * SQUARE_MARGIN])

                    if (i, j) == startMovePos:
                        pygame.draw.rect(board, GREEN, square((startMovePos[1], startMovePos[0])))
                    if (i, j) == endMovePos:
                        pygame.draw.rect(board, GREEN, square((endMovePos[1], endMovePos[0])))
                    if (i, j) == bestMove[0]:
                        pygame.draw.rect(board, RED, square((bestMove[0][1], bestMove[0][0])))
                    if (i, j) == bestMove[1]:
                        pygame.draw.rect(board, RED, square((bestMove[1][1], bestMove[1][0])))

                    drawPiece((i, j))

            pygame.display.flip()
            clock.tick(60)

            screen.blit(textSurface, (WINDOW_SIZE[0], 0))

pygame.quit()


