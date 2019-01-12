#Memory Game (Python Mini Project)

#Developed by Akash Rajpurohit,Ronak Jain,Ronak Mali
#In Beta-2 Version
#START DATE : 15/02/2018
#END DATE : 

import random, pygame, sys, os
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1' #Position the Window to Center

pygame.mixer.pre_init(44100,16,2,4096)

pygame.init()

#Set Icon
icon = pygame.image.load('icon/icon.png')

pygame.display.set_icon(icon)

qm = pygame.image.load('imgs/qstnmark.jpg')

bg1 = pygame.image.load('imgs/final.png')

bg = pygame.image.load('imgs/bg.jpg')

PIKACHU = pygame.image.load('models/pikachu.png')

CHARMANDER = pygame.image.load('models/charmander.png')

DRATINI = pygame.image.load('models/dratini.png')

EEVEE =pygame.image.load('models/eevee.png')

JIGGLYPUFF=pygame.image.load('models/jigglypuff.png')

MEOWTH=pygame.image.load('models/meowth.png')

MEW=pygame.image.load('models/mew.png')

PIDGEY=pygame.image.load('models/pidgey.png')

RATTATA=pygame.image.load('models/rattata.png')

SNORLAX=pygame.image.load('models/snorlax.png')

SQUIRTLE=pygame.image.load('models/squirtle.png')

ZUBAT=pygame.image.load('models/zubat.png')

#Set Caption
pygame.display.set_caption('Brain V/S Box')

#Initialize Sound
win_sound = pygame.mixer.Sound('sound/win.wav')

pygame.mixer.music.load('sound/background.wav')

click_sound = pygame.mixer.Sound('sound/cardflip.wav')

intro_sound = pygame.mixer.Sound('sound/intro.wav')

lose_sound = pygame.mixer.Sound('sound/lose.wav')


FPS = 60 # frames per second, the general speed of the program

WINDOWWIDTH = 640 # size of window's width in pixels

WINDOWHEIGHT = 480 # size of windows' height in pixels

REVEALSPEED = 5 # speed boxes' sliding reveals and covers

BOXSIZE = 64 # size of box height & width in pixels

GAPSIZE = 10 # size of gap between boxes in pixels

BOARDWIDTH = 3 # number of columns of icons

BOARDHEIGHT = 2 # number of rows of icons


assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'


XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)

YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)


#                       R    G    B
FLIRTATIOUS        = ( 254, 211,  48 )

NAVYBLUE           = (  64,  64, 122 )

WHITE              = ( 255, 255, 255 )

RED                = ( 255,  77,  77 )

BRIGHT_RED         = ( 255,  56,  56)

DARK_RED           = (214, 48, 49)

GREEN              = (  88, 177, 159)

BRIGHT_GREEN       = (16, 172, 132)

BLUE               = (75, 123, 236)

BRIGHT_BLUE        = (56, 103, 214)

BROWN              = (179, 55, 113)

BRIGHT_BROWN       = (109, 33, 79)

ORANGE             = (243, 156, 18)

BRIGHT_ORANGE      = (225, 112, 85)

PURPLE             = (205, 132, 241)

BRIGHT_PURPLE      = (197, 108, 240)

CYAN               = (24, 220, 255)

BLACK              = (0, 0, 0)

BGCOLOR = NAVYBLUE

WINCOLOR = FLIRTATIOUS

LOSECOLOR = DARK_RED

BOXCOLOR = WHITE

HIGHLIGHTCOLOR = BLUE

pikachu = 'pikachu'

charmander = 'charmander'

dratini='dratini'

eevee='eevee'

jigglypuff='jigglypuff'

meowth='meowth'

mew='mew'

pidgey='pidgey'

rattata='rattata'

snorlax='snorlax'

squirtle='squirtle'

zubat='zubat'


ALLSHAPES = (dratini,eevee,jigglypuff,meowth,mew,pidgey,pikachu,rattata,snorlax,squirtle,zubat,charmander)

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

Click = 2 # Count the Number of Clicks
    
def main():

    game_intro()

def game_loop():

    global FPSCLOCK, DISPLAYSURF, Click, color

    color = WHITE

    FPSCLOCK = pygame.time.Clock()

    mousex = 0 # used to store x coordinate of mouse event

    mousey = 0 # used to store y coordinate of mouse event

    mainBoard = getRandomizedBoard()

    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    DISPLAYSURF.blit(bg,[0,0])

    startGameAnimation(mainBoard)

    while True: # main game loop

        mouseClicked = False

        if Click <= 3:

            color = RED

        DISPLAYSURF.blit(bg,[0,0]) # drawing the window

        drawBoard(mainBoard, revealedBoxes)
        


        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):

                pygame.quit()

                sys.exit()

            elif event.type == MOUSEMOTION:

                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP:

                mousex, mousey = event.pos

                mouseClicked = True



        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None:

            # The mouse is currently over a box.

            if not revealedBoxes[boxx][boxy]:

                drawHighlightBox(boxx, boxy)

            if not revealedBoxes[boxx][boxy] and mouseClicked:

                pygame.mixer.Sound.play(click_sound)

                revealBoxesAnimation(mainBoard, [(boxx, boxy)])

                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                
                if firstSelection == None: # the current box was the first box clicked
                    
                    firstSelection = (boxx, boxy)
                    clicks(Click,color)
                else: # the current box was the second box clicked
                    
                    # Check if there is a match between the two icons.

                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])

                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    
                    if icon1shape != icon2shape or icon1color != icon2color:
                                
                        Click -= 1
                        clicks(Click,color)            
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])

                        revealedBoxes[firstSelection[0]][firstSelection [1]] = False

                        revealedBoxes[boxx][boxy] = False
                        
                        


                    elif hasWon(revealedBoxes) and Click >= 0: # check if all pairs found
                            
                        gameWonAnimation(mainBoard)

                        win(Click)

                        pygame.time.wait(2500)
                        
                        #Reset the board
                            
                        mainBoard = getRandomizedBoard()

                        revealedBoxes = generateRevealedBoxesData(False)


                        # Show the fully unrevealed board for a second.

                        drawBoard(mainBoard, revealedBoxes)

                        pygame.display.update()

                        pygame.time.wait(1000)


                        # Replay the start game animation.

                        startGameAnimation(mainBoard)

                    firstSelection = None # reset firstSelection variable
                    
                      

        # Redraw the screen.
        

        if Click <= 0 :

            gameLostAnimation(mainBoard)

            lose()

        clicks(Click,color)

        pygame.display.update()

        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):

    revealedBoxes = []

    for i in range(BOARDWIDTH):

        revealedBoxes.append([val] * BOARDHEIGHT)

    return revealedBoxes



def getRandomizedBoard():

    # Get a list of every possible shape in every possible color.

    icons = []

    for shape in ALLSHAPES:

        icons.append( (shape,color) )


    random.shuffle(icons) # randomize the order of the icons list

    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed

    icons = icons[:numIconsUsed] * 2 # make two of each

    random.shuffle(icons)


    # Create the board data structure, with randomly placed icons.

    board = []

    for x in range(BOARDWIDTH):

        column = []

        for y in range(BOARDHEIGHT):

            column.append(icons[0])

            del icons[0] # remove the icons as we assign them

        board.append(column)

    return board




def splitIntoGroupsOf(groupSize, theList):

    # splits a list into a list of lists, where the inner lists have at

    # most groupSize number of items.

    result = []

    for i in range(0, len(theList), groupSize):

        result.append(theList[i:i + groupSize])

    return result



def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN

    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN + 30

    return (left, top)





def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):

        for boxy in range(BOARDHEIGHT):
            
            left, top = leftTopCoordsOfBox(boxx, boxy)

            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)

            if boxRect.collidepoint(x, y):

                return (boxx, boxy)

    return (None, None)





def drawIcon(shape, color, boxx, boxy):

    quarter = int(BOXSIZE * 0.25) # syntactic sugar

    half =    int(BOXSIZE * 0.5)  # syntactic sugar



    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords

    # Draw the shapes

    if shape == pikachu :

        DISPLAYSURF.blit(PIKACHU,[left + half - 32 , top + half - 32 ])

    elif shape == charmander :

        DISPLAYSURF.blit(CHARMANDER,[left + half - 32 , top + half - 32 ])
        
    elif shape == dratini :

        DISPLAYSURF.blit(DRATINI,[left + half - 32 , top + half - 32])
        
    elif shape == eevee :

        DISPLAYSURF.blit(EEVEE,[left + half - 32 , top + half - 32 ])
        
    elif shape == jigglypuff :

        DISPLAYSURF.blit(JIGGLYPUFF,[left + half - 32 , top + half - 32 ])
        
    elif shape == meowth :

        DISPLAYSURF.blit(MEOWTH,[left + half - 32 , top + half - 32 ])
        
    elif shape == mew :

        DISPLAYSURF.blit(MEW,[left + half - 32 , top + half - 32 ])
        
    elif shape == pidgey :

        DISPLAYSURF.blit(PIDGEY,[left + half - 32 , top + half - 32 ])
        
    elif shape == rattata :

        DISPLAYSURF.blit(RATTATA,[left + half - 32 , top + half - 32 ])
        
    elif shape == snorlax :

        DISPLAYSURF.blit(SNORLAX,[left + half - 32, top + half - 32 ])
        
    elif shape == squirtle :

        DISPLAYSURF.blit(SQUIRTLE,[left + half - 32 , top + half - 32 ])
        
    elif shape == zubat :

        DISPLAYSURF.blit(ZUBAT,[left + half - 32 , top + half - 32 ])





def getShapeAndColor(board, boxx, boxy):

    # shape value for x, y spot is stored in board[x][y][0]

    # color value for x, y spot is stored in board[x][y][1]

    return board[boxx][boxy][0], board[boxx][boxy][1]





def drawBoxCovers(board, boxes, coverage):

    # Draws boxes being covered/revealed"boxes" is a list

    # of two-item lists, which have the x & y spot of the box.

    for box in boxes:

        left, top = leftTopCoordsOfBox(box[0], box[1])

        pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))

        shape, color = getShapeAndColor(board, box[0], box[1])

        drawIcon(shape, color, box[0], box[1])
        
        if coverage > 0: # only draw the cover if there is an coverage

            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    
    pygame.display.update()

    FPSCLOCK.tick(FPS)




def revealBoxesAnimation(board, boxesToReveal):

    # Do the "box reveal" animation.

    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):

        drawBoxCovers(board, boxesToReveal, coverage)
        

    pygame.display.update()





def coverBoxesAnimation(board, boxesToCover):

    # Do the "box cover" animation.

    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):

        drawBoxCovers(board, boxesToCover, coverage)




def drawBoard(board, revealed):

    # Draws all of the boxes in their covered or revealed state.

    for boxx in range(BOARDWIDTH):

        for boxy in range(BOARDHEIGHT):

            left, top = leftTopCoordsOfBox(boxx, boxy)

            if not revealed[boxx][boxy]:

                # Draw a covered box.

                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

                button("<",20,40,30,30,BLUE,BRIGHT_BLUE,level)

                DISPLAYSURF.blit(qm, (left+4, top+8))

            else:

                # Draw the (revealed) icon.

                shape, color = getShapeAndColor(board, boxx, boxy)

                drawIcon(shape, color, boxx, boxy)





def drawHighlightBox(boxx, boxy):

    left, top = leftTopCoordsOfBox(boxx, boxy)

    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)



def startGameAnimation(board):

    # Randomly reveal the boxes 8 at a time.

    coveredBoxes = generateRevealedBoxesData(False)

    boxes = []

    for x in range(BOARDWIDTH):

        for y in range(BOARDHEIGHT):

            boxes.append( (x, y) )

    random.shuffle(boxes)

    boxGroups = splitIntoGroupsOf(20, boxes)



    drawBoard(board, coveredBoxes)

    for boxGroup in boxGroups:

        revealBoxesAnimation(board, boxGroup)

        coverBoxesAnimation(board, boxGroup)




def gameWonAnimation(board):

    pygame.mixer.music.stop()

    pygame.mixer.Sound.play(win_sound)

    pygame.mixer.Sound.stop(click_sound)

    # flash the background color when the player has won

    coveredBoxes = generateRevealedBoxesData(True)

    color1 = WINCOLOR

    color2 = BGCOLOR


    for i in range(9):

        color1, color2 = color2, color1 # swap colors

        DISPLAYSURF.fill(color1)

        drawBoard(board, coveredBoxes)

        pygame.display.update()

        pygame.time.wait(250)


def gameLostAnimation(board):

    pygame.mixer.music.stop()

    pygame.mixer.Sound.play(lose_sound)

    pygame.mixer.Sound.stop(click_sound)

    # flash the background color when the player has won

    coveredBoxes = generateRevealedBoxesData(True)

    color1 = LOSECOLOR

    color2 = BGCOLOR


    for i in range(9):

        color1, color2 = color2, color1 # swap colors

        DISPLAYSURF.fill(color1)

        drawBoard(board, coveredBoxes)

        pygame.display.update()

        pygame.time.wait(250)


def clicks(click,color) :
    
    font = pygame.font.Font('fonts/neuropol x rg.ttf', 40)
    text = font.render("MOVES LEFT : " + str(click), True, color)
    
    DISPLAYSURF.blit(text,(100,35))


def win(click):
    
    win = True

    quotes = ["Awesome!","Perfect!!!!","Bravo!","Spectacular!","Eagle Eye!!!"]

    quote = random.choice(quotes)

    while win :
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()

                sys.exit()
                
                quit()

        DISPLAYSURF.blit(bg,[0,0])
        
        message_display(quote,WINDOWWIDTH/2,100,WHITE,75,'fonts/Hanged Letters.ttf')

        message_display("Try Next Level",WINDOWWIDTH/2,300,WHITE,60,'fonts/Hanged Letters.ttf')

        message_display("Your Score  : " + str(click),WINDOWWIDTH/2,200,BLACK,60,"fonts/Electro Shackle.otf")

        button("Levels",130,380,130,50,GREEN,BRIGHT_GREEN,level)
        
        button("BYE :(",420,380,130,50,RED,BRIGHT_RED,quitgame)

        pygame.display.update()


def lose():

    quotes = ["Game Over","Oops!","Hard Luck","Never Back Down","Don't Give Up"]

    quote = random.choice(quotes)
    

    lose = True

    while lose :
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()

                sys.exit()
                
                quit()

        DISPLAYSURF.blit(bg,[0,0])
        
        message_display(quote,WINDOWWIDTH/2,WINDOWHEIGHT/3,WHITE,80,'fonts/Hanged Letters.ttf')

        message_display("Try Again!!",WINDOWWIDTH/2,WINDOWHEIGHT/2 + 40,WHITE,80,'fonts/Hanged Letters.ttf')
        
        button("Again?",130,350,130,50,GREEN,BRIGHT_GREEN,level)

        button("BYE :(",420,350,130,50,RED,BRIGHT_RED,quitgame)

        pygame.display.update()
    


def text_objects(text, font, color):
    
    textSurface = font.render(text, True, color)

    return textSurface,textSurface.get_rect()


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False

    for i in revealedBoxes:

        if False in i:

            return False # return False if any boxes are covered.

    return True


def button(msg,x,y,w,h,ic,ac,action = None):
    
    mouse = pygame.mouse.get_pos()

    #print(mouse)

    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        
        pygame.draw.rect(DISPLAYSURF,ac,(x,y,w,h))

        if click[0] == 1 and action != None :

            action()

    else :

        pygame.draw.rect(DISPLAYSURF,ic,(x,y,w,h))

    smallText = pygame.font.Font('fonts/HVD_Comic_Serif_Pro.otf', 30)
    
    textSurf, textRect = text_objects(msg, smallText, WHITE)
    
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    
    DISPLAYSURF.blit(textSurf,textRect)
    


def game_intro():

    pygame.mixer.Sound.stop(intro_sound)

    pygame.mixer.Sound.play(intro_sound)

    intro = True

    while intro :
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()

                sys.exit()
                
                quit()

        DISPLAYSURF.blit(bg1,[0,0])

        button("Go!!!!",WINDOWWIDTH/2 - 80,400,100,50,GREEN,BRIGHT_GREEN,level)

        button("About",500,20,100,50,BLUE,BRIGHT_BLUE,about)

        pygame.display.update()
        

def level():

    pygame.mixer.music.play(-1)

    pygame.mixer.Sound.stop(win_sound)

    pygame.mixer.Sound.stop(lose_sound)

    pygame.mixer.Sound.stop(click_sound)

    pygame.mixer.Sound.stop(intro_sound)

    level = True

    while level :
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit()
                
                quit()

        DISPLAYSURF.blit(bg,[0,0])
        
        largeText = pygame.font.Font('fonts/HVD_Comic_Serif_Pro.otf', 40)

        TextSurf , TextRect = text_objects("Choose a Level", largeText , WHITE)

        TextRect.center = ((WINDOWWIDTH/2),(WINDOWHEIGHT/9))

        DISPLAYSURF.blit(TextSurf,TextRect)

        button("Noob",400,110,220,40,GREEN,BRIGHT_GREEN,lambda : levels(5,4,16))

        message_display('16 Move Puzzle',150,130,GREEN,25,'fonts/ka1.ttf')

        message_display('<----',330,130,GREEN,40,'fonts/Roboto-Black.ttf')

        button("Beginner",40,180,220,40,ORANGE,BRIGHT_ORANGE,lambda : levels(5,4,14))

        message_display('14 Move  Puzzle',510,200,ORANGE,25,'fonts/ka1.ttf')

        message_display('---->',330,200,ORANGE,40,'fonts/Roboto-Black.ttf')

        button("Intermediate",400,250,220,40,BROWN,BRIGHT_BROWN,lambda : levels(5,4,12))

        message_display('12 Move Puzzle',150,270,BROWN,25,'fonts/ka1.ttf')

        message_display('<----',330,270,BROWN,40,'fonts/Roboto-Black.ttf')

        button("Professional",40,320,220,40,PURPLE,BRIGHT_PURPLE,lambda : levels(5,4,10))

        message_display('10 Move Puzzle',510,340,PURPLE,25,'fonts/ka1.ttf')

        message_display('---->',330,340,PURPLE,40,'fonts/Roboto-Black.ttf')

        button("Insane",400,390,220,40,BLUE,BRIGHT_BLUE,lambda : levels(5,4,8))

        message_display('8 Move Puzzle',150,410,BLUE,25,'fonts/ka1.ttf')

        message_display('<----',330,410,BLUE,40,'fonts/Roboto-Black.ttf')

        pygame.display.update()
        

def message_display(text,x,y,color,fontSize,font):

    largeText = pygame.font.Font(font,fontSize)

    TextSurf , TextRect = text_objects(text, largeText , color)

    TextRect.center = (x,y)

    DISPLAYSURF.blit(TextSurf,TextRect)


def levels(width,height,click):

    global BOARDWIDTH,BOARDHEIGHT,XMARGIN,YMARGIN,Click

    BOARDWIDTH = width

    BOARDHEIGHT = height

    Click = click

    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)

    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
    
    game_loop()


def about():

    about = True

    while about :
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()

                sys.exit()
                
                quit()

        DISPLAYSURF.blit(bg,[0,0])

        message_display("About The Developers",WINDOWWIDTH/2,50,RED,35,'fonts/hemi head bd it.ttf')

        message_display("-----------------------------------",320,100,WHITE,35,'fonts/hemi head bd it.ttf')

        message_display("This Game is Developed by the Team 'RAR-Ed'",320,150,FLIRTATIOUS,25,'fonts/hemi head bd it.ttf')

        message_display("The Members of the Team are : ",230,200,CYAN,25,'fonts/hemi head bd it.ttf')

        message_display("Akash Rajpurohit",190,250,ORANGE,35,'fonts/hemi head bd it.ttf')

        message_display("Ronak Jain",140,300,WHITE,35,'fonts/hemi head bd it.ttf')

        message_display("Ronak Mali",140,350,GREEN,35,'fonts/hemi head bd it.ttf')

        message_display("Contact Developers :",500,300,BROWN,25,'fonts/hemi head bd it.ttf')

        message_display("raredinc@gmail.com",500,350,BROWN,25,'fonts/hemi head bd it.ttf')

        button("Back",100,420,120,45,BLUE,BRIGHT_BLUE,game_intro)

        button("Start",450,420,120,45,GREEN,BRIGHT_GREEN,level)

        pygame.display.update()
    


def quitgame() :

    pygame.quit()

    sys.exit()
    
    quit()



if __name__ == '__main__':

    main()
