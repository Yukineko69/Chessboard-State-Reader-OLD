import tkinter as tk
from Game import Game

LARGE_FONT = ('system', 20)
MED_FONT = ('system', 16)
SMALL_FONT = ('system', 12)

EASY_SKILL_LEVEL = 1
INTERMEDIATE_SKILL_LEVEL = 5
HARD_SKILL_LEVEL = 10
EXTREME_SKILL_LEVEL = 15
MASTER_SKILL_LEVEL = 20

class Application(tk.Tk):
    def __init__(self, url):
        '''
        GUI Controller
        '''
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.game = Game(url)

        # Holds CPU move information
        self.move = tk.StringVar()
        self.move.set('e2')
        # Holds winner information
        self.winner = tk.StringVar()
        self.winner.set('CPU Win')

        # Give page objects to Application
        for object in (StartGamePage, InitializeBoardPage,SetBoardPage, ChooseSidePage,
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

        easyButton = tk.Button(self, text='Easy', font=MED_FONT,
                               command = lambda: [self.setDifficulty(controller, EASY_SKILL_LEVEL),
                                                  controller.show_frame(ChooseSidePage)])
        intermediateButton = tk.Button(self, text='Intermediate', font=MED_FONT,
                               command = lambda: [self.setDifficulty(controller, INTERMEDIATE_SKILL_LEVEL),
                                                  controller.show_frame(ChooseSidePage)])
        hardButton = tk.Button(self, text='Hard', font=MED_FONT,
                               command = lambda: [self.setDifficulty(controller, HARD_SKILL_LEVEL),
                                                  controller.show_frame(ChooseSidePage)])
        extremeButton = tk.Button(self, text='Extreme', font=MED_FONT,
                               command = lambda: [self.setDifficulty(controller, EXTREME_SKILL_LEVEL),
                                                  controller.show_frame(ChooseSidePage)])
        masterButton = tk.Button(self, text='Master', font=MED_FONT,
                               command = lambda: [self.setDifficulty(controller, MASTER_SKILL_LEVEL),
                                                  controller.show_frame(ChooseSidePage)])

        label.pack(padx=10, pady=10)
        easyButton.pack()
        intermediateButton.pack()
        hardButton.pack()
        extremeButton.pack()
        masterButton.pack()

    def setDifficulty(self, controller, skill_level=1):
        controller.game.chessEngine.engine.setoption({'Skill Level' : skill_level})

class ChooseSidePage(tk.Frame):
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
                                                 self.checkValid(controller)])

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
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Your are in CHECK!!!', font=LARGE_FONT)

        continueButton = tk.Button(self, text='Continue', font=MED_FONT,
                                   command = lambda: [controller.show_frame(PlayerMovePage)])

        label.pack(padx=10, pady=10)
        continueButton.pack()

class ChoosePromotionPage(tk.Frame):
    '''
    Ask user to choose which piece they would like to promote their pawn
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Choose your promotion', font=LARGE_FONT)

        queenButton = tk.Button(self, text='Queen', font=MED_FONT,
                                command = lambda: [self.setPromotion(controller, 'q')])
        rookButton = tk.Button(self, text='Rook', font=MED_FONT,
                               command = lambda: [self.setPromotion(controller, 'r')])
        bishopButton = tk.Button(self, text='Bishop', font=MED_FONT,
                                 command = lambda: [self.setPromotion(controller, 'b')])
        knightButton = tk.Button(self, text='Knight', font=MED_FONT,
                                 command = lambda: [self.setPromotion(controller, 'n')])

        label.pack(padx=10, pady=10)
        queenButton.pack()
        rookButton.pack()
        bishopButton.pack()
        knightButton.pack()

    def setPromotion(self, controller, promotion='q'):
        '''
        Updates the move to UCI
        Check validity and update board
        '''
        controller.game.board.promotion = promotion
        controller.game.board.move += promotion
        controller.game.playerPromotion(controller.game.board.move)

        if controller.game.PlayerMoveError:
            controller.game.current = controller.game.previous
            controller.show_frame(PlayerMoveErrorPage)

        else:
            controller.move.set(controller.game.CPUMove())
            controller.show_frame(CPUMovePage)

class GameOverPage(tk.Frame):
    '''
    Shows the winner of the game
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Game Over', font=LARGE_FONT)

        self.winnerLabel = tk.Label(self, textvariable=controller.winner, font=LARGE_FONT)

        label.pack(padx=10, pady=10)
        self.winnerLabel.pack(padx=10, pady=10)
