import tkinter as tk
from tkinter import *
from Game import Game

LARGE_FONT = ('system', 20)
MED_FONT = ('system', 16)
SMALL_FONT = ('system', 12)

EASY_SKILL_LEVEL = 1
INTERMEDIATE_SKILL_LEVEL = 5
HARD_SKILL_LEVEL = 10
EXTREME_SKILL_LEVEL = 15
MASTER_SKILL_LEVEL = 20

url = 'http://192.168.1.7:8080/shot.jpg'

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        '''
        GUI Controller
        '''
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.game = Game()

        # Holds CPU move information
        self.move = StringVar()
        self.move.set('e2')
        # Holds winner information
        self.winner = StringVar()
        self.winner.set('CPU Win')

        # Give page objects to Application
        for object in (StartGamePage, InitializeBoardPage,SetBoardPage, ChooseColorPage,
                       ChooseDifficultyPage, CPUMovePage, PlayerMovePage, CheckPage,
                       CPUMoveErrorPage, GameOverPage, PlayerMoveErrorPage, ChoosePromotionPage):
            frame = object(container, self)
            self.frames[object] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartGamePage)

    def show_frame(self, object):
        frame = self.frames[object]
        frame.tkraise()

class StartGamePage(tk.Frame):
    '''
    Ask user start new game
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Chessboard State Reader', font=LARGE_FONT)

        startGameButton = tk.Button(self, text='Start New Game', font=MED_FONT,
                                    command = lambda: [controller.show_frame(InitializeBoardPage),
                                                       controller.game.setUp()])

        label.pack(pady=20, padx=20)
        startGameButton.pack()

class InitializeBoardPage(tk.Frame):
    '''
    Ask user clear board for initialization
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Please clear your board for game set up', font=LARGE_FONT)
        initBoardButton = tk.Button(self, text='Done', font=MED_FONT,
                                    command = lambda: [controller.show_frame(SetBoardPage),
                                                       controller.game.analyzeBoard()])

        label.pack(padx=10, pady=10)
        initBoardButton.pack()

class SetBoardPage(tk.Frame):
    '''
    Ask user setup board after initialization
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Game initialization done. Please setup your board', font=LARGE_FONT)
        initBoardButton = tk.Button(self, text='Done', font=MED_FONT,
                                    command = lambda: [controller.show_frame(ChooseDifficultyPage),
                                                       controller.game.checkBoardIsSet()])

        label.pack(padx=10, pady=10)
        initBoardButton.pack()

class ChooseDifficultyPage(tk.Frame):
    '''
    Ask user choose difficulty of chess engine
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Please choose the difficulty', font=LARGE_FONT)

        easyButton = tk.Button(self, text='Easy',
                               command = lambda: [self.setDifficulty(controller, EASY_SKILL_LEVEL),
                                                  controller.show_frame(ChooseColorPage)])
        intermediateButton = tk.Button(self, text='Intermediate',
                               command = lambda: [self.setDifficulty(controller, INTERMEDIATE_SKILL_LEVEL),
                                                  controller.show_frame(ChooseColorPage)])
        hardButton = tk.Button(self, text='Hard',
                               command = lambda: [self.setDifficulty(controller, HARD_SKILL_LEVEL),
                                                  controller.show_frame(ChooseColorPage)])
        extremeButton = tk.Button(self, text='Extreme',
                               command = lambda: [self.setDifficulty(controller, EXTREME_SKILL_LEVEL),
                                                  controller.show_frame(ChooseColorPage)])
        masterButton = tk.Button(self, text='Master',
                               command = lambda: [self.setDifficulty(controller, MASTER_SKILL_LEVEL),
                                                  controller.show_frame(ChooseColorPage)])

        label.pack(padx=10, pady=10)
        easyButton.pack()
        intermediateButton.pack()
        hardButton.pack()
        extremeButton.pack()
        masterButton.pack()

    def setDifficulty(self, controller, skill_level=1):
        controller.game.chessEngine.engine.setoption({'Skill Level' : skill_level})

class ChooseColorPage(tk.Frame):
    '''
    Ask user choose to move first or not (choose side)
    '''
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Which side would you like to play?', font=LARGE_FONT)

        blackButton = tk.Button(self, text='Black', font=MED_FONT,
                                command = lambda: [controller.show_frame(CPUMovePage),
                                                   controller.move.set(controller.game.CPUMove())])
        whiteButton = tk.Button(self, text='White', font=MED_FONT,
                                command = lambda: [controller.show_frame(PlayerMovePage)])

        label.pack(padx=10, pady=10)
        blackButton.pack()
        whiteButton.pack()

class CPUMovePage(tk.Frame):
    '''
    Displays chess engine move and ask user to move piece
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='CPU Move:', font=LARGE_FONT)

        self.moveLabel = tk.Label(self, textvariable=controller.move, font=MED_FONT)

        CPUButton = tk.Button(self, text='Done', font=MED_FONT,
                              command = lambda: [controller.game.updateCurrent(),
                                                 sef.checkValid(controller)])

        label.pack(padx=10, pady=10)
        self.moveLabel.pack(padx=10, pady=10)
        CPUButton.pack()

    def checkValid(self, controller):
        '''
        Check move validity
        '''
        if controller.game.over:
            controller.winner.set(controller.game.winner)
            controller.show_frame(GameOverPage)

        elif controller.game.isCheck:
            controller.show_frame(CheckPage)

        elif controller.game.CPUMoveError:
            controller.game.current = controller.game.previous
            controller.show_frame(CPUMoveErrorPage)

        else:
            controller.show_frame(PlayerMovePage)

class PlayerMovePage(tk.Frame):
    '''
    Ask user to move
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Your move:', font=LARGE_FONT)

        playerButton = tk.Button(self, text='Done', font=MED_FONT,
                                 command = lambda: [controller.game.playerMove(),
                                                    self.checkValid(controller)])
        resignButton = tk.Button(self, text='Resign', font=MED_FONT,
                                 command = lambda: [controller.show_frame(GameOverPage)])

        label.pack(padx=10, pady=10)
        playerButton.pack()
        resignButton.pack()

    def checkValid(self, controller):
        '''
        Check move validity
        '''
        if controller.game.over:
            controller.winner.set(controller.game.winner)
            controller.show_frame(GameOverPage)

        elif controller.game.board.promo:
            controller.show_frame(ChoosePromotionPage)

        elif controller.game.PlayerMoveError:
            controller.game.current = controller.game.previous
            controller.show_frame(PlayerMoveErrorPage)

        else:
            controller.move.set(controller.game.CPUMove())
            controller.show_frame(CPUMovePage)

class CPUMoveErrorPage(tk.Frame):
    '''
    Alert user that the move they made is not correct (not the same as the move CPU requested)
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='That wasn\'t the correct CPU move', font=LARGE_FONT)

        showCPUMoveButton = tk.Button(self, text='Show CPU move', font=MED_FONT,
                                      command = lambda: [controller.show_frame(CPUMovePage)])

        label.pack(padx=10, pady=10)
        showCPUMoveButton.pack()

class PlayerMoveErrorPage(tk.Frame):
    '''
    Alert user that they made an invalid move
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Error, invalid move', font=LARGE_FONT)

        tryAgainButton = tk.Button(self, text='Try again', font=MED_FONT,
                                   command = lambda: [controller.show_frame(PlayerMovePage)])

        label.pack(padx=10, pady=10)
        tryAgainButton.pack()

class CheckPage(tk.Frame):
    '''
    Alert user they are in check
    '''
    def __init__(self, parent, controller):
        
