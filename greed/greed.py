from tkinter import *
from random import *
import tkinter.messagebox



class ScoreBoard():
    
    def __init__(self,parent):
        self.parent = parent       
        self.initGUI()        
        self.reset()
        
    def initGUI(self):
        # Score
        self.scoreVar = IntVar()
        Label(self.parent, text="Score:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=25, pady=50, sticky=N+W)
        Label(self.parent, textvariable=self.scoreVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=40, pady=100, sticky=N+W)        
        
    def reset(self):
        self.score = 0
        self.scoreVar.set(self.score)     
   
    def updateBoard(self, scoreStatus):
        self.score += scoreStatus
        self.scoreVar.set(self.score)


class ItemsFallingFromSky():
    
    def __init__(self,parent,canvas,player,board):
        self.parent = parent                    # root form
        self.canvas = canvas                    # canvas to display
        self.player = player                    # to check touching
        self.board = board                      # score board statistics
        
        self.fallSpeed = 70                     # falling speed        
        self.xPosition = randint(50, 750)       # random position
        self.isgood = randint(0,1)             # random goodness

        self.goodItems = ["zafir.png","emerald.png","diamond.png"] #Instead of creating a class for each element a group of gems or good items was created
        self.badItems = ["rock1.png","rock2.png","rock3.png"] #Instead of creating a class for each element a group of rocks or bad items was created
        
        # create falling items
        if self.isgood:   
            self.itemPhoto = tkinter.PhotoImage(file = "c:/Users/ASUS/Desktop/greed/images/{}" .format(choice(self.goodItems) ) )
            self.fallItem = self.canvas.create_image( (self.xPosition, 50) , image=self.itemPhoto , tag="good" )
        
        else:
            self.itemPhoto = tkinter.PhotoImage(file = "c:/Users/ASUS/Desktop/greed/images/{}" . format(choice(self.badItems) ) )
            self.fallItem = self.canvas.create_image( (self.xPosition, 50) , image=self.itemPhoto , tag="bad" )
            
        # trigger falling item movement
        self.move_object()
        
        
    def move_object(self):
        # dont move x, move y
        self.canvas.move(self.fallItem, 0, 20)
        
        if (self.check_touching()) or (self.canvas.coords(self.fallItem)[1] > 650):     # [ x0, y0, x1, y1 ]
            self.canvas.delete(self.fallItem)                                           # delete if out of canvas
        else:
            self.parent.after(self.fallSpeed, self.move_object)                         # after some time move object
            
        
    def check_touching(self):
        # find current coordinates
        x0, y0 = self.canvas.coords(self.fallItem)
        x1, y1 = x0 + 50, y0 + 50
        
        # get overlapps
        overlaps = self.canvas.find_overlapping(x0, y0, x1, y1)
        
        if (self.canvas.gettags(self.fallItem)[0] == "good") and (len(overlaps) > 1):
            self.board.updateBoard(1)                                              # (score)
            return True                                                                 # touching yes
        elif (self.canvas.gettags(self.fallItem)[0] == "bad") and (len(overlaps) > 1):
            self.board.updateBoard(-1)                                               # (score)
            return True                                                                 # touching yes
        return False                                                                    # touching not
    


class TheGame(ItemsFallingFromSky,ScoreBoard):
    
    def __init__(self,parent):
        self.parent = parent
        
        # windows form
        self.parent.geometry("1024x650")
        self.parent.title("GREED")

        # canvas window
        self.canvas = Canvas(self.parent, width=800, height=600)
        self.canvas.config(background="#000000")
        self.canvas.bind("<Key>", self.keyMoving)       # take keyboard input as movement
        self.canvas.focus_set()
        self.canvas.grid(row=1, column=1, padx=25, pady=25, sticky=W+N)

        # player character
        self.playerPhoto = tkinter.PhotoImage(file = "c:/Users/ASUS/Desktop/greed/images/{}" .format( "ship2.png" ) )
        self.playerChar = self.canvas.create_image( (475, 560) , image=self.playerPhoto , tag="player" )

        # define score board
        self.personalboard = ScoreBoard(self.parent)

        # start poping falling items
        self.createEnemies()
        
        
    def keyMoving(self, event):        
        if (event.char == "z") and (self.canvas.coords(self.playerChar)[0] > 50):
            self.canvas.move(self.playerChar, -50, 0)            
        if (event.char == "x") and (self.canvas.coords(self.playerChar)[0] < 750):
            self.canvas.move(self.playerChar, 50, 0)


    def createEnemies(self):
        ItemsFallingFromSky(self.parent, self.canvas, self.playerChar, self.personalboard)
        self.parent.after(1000, self.createEnemies)
        

        
if __name__ == "__main__":
    root = Tk()
    TheGame(root)
    root.mainloop()