
import time
import tkinter as tk
from PIL import  ImageTk as itk 
import random
from copy import copy
from math import sqrt, log



def playWithFriend(rootwin):
    
    clearAll(rootwin)
    # Creates a board
    my_board = Board(rootwin)


    # Creates pieces inside the board
    my_player = Human(my_board)  
    my_player.play()

        
def playWithComputer(rootwin):

    clearAll(rootwin)
    # Creates a board
    my_board = Board(rootwin)


    # Creates pieces inside the board
    my_player = Computer(my_board)  
    my_player.play()

        

#List functions
def mostFrequent(list1):
    highest = 0
    count =0
    for i in list1:
        c = list1.count(i)
        if c >= count :
            count = c
            highest = i

    return highest

def Intersection(list1, list2):
    list3 = []
    for i in list1:
        if i in list2:
            if i not in list3:
                list3.append(i)
    
    return list3
def Difference(list1,list2): # list1-list2
    "list1 - list2"
    
    for i in list2:
        if i in list1:
            count = list1.count(i)
            if count > 1:
                for _ in range(0,count):
                    list1.remove(i)
            else:  list1.remove(i)  

    return list1

def Union(list1,list2):
    list3 = []
    for i in list1:
        if i not in list3:
            list3.append(i)
    for i in list2:
        if i not in list3:
            list3.append(i)
    return list3        



def clearAll(window):
    "Used to clear everything on the window"
    
    #time.sleep(1) # Gives an interval between the function call and execution so that it doesn't appear abrupt
    def all_children (window) :
        _list = window.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list

    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()
    



class Memory:

    def __init__(self, board):

          
        self.board = board

        # Setting the winner string to empty 
        self.winner = 'N/A'

        # Tells memory whether the game started with player X
        self.start_with_playerx = None
        #Winner announced boolean 
        self.winner_announced = False
        # Counting the moves made my the players
        self.playerx_moves = 0
        self.playero_moves = 0
        self.total_moves = self.playerx_moves + self.playero_moves 

        # Slots that when a certain player occupies, he/she is decided a winner
        self.winning_slots = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]

        # This is the total number of slots, but here we use it to delete taken slots so that images are not overwritten
        self.slots = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9}
        self.slots_takenx = []
        self.slots_takeno = []

    @property
    def WinnerAnnounced(self):
        return self.winner_announced
    @WinnerAnnounced.setter
    def WinnerAnnounced(self, boolean):
        self.winner_announced = boolean





class Board:
        

    def __init__(self, rootwin, width = 400, height = 400, board_color = 'black', board_bg = 'white'):
            self.rootwin = rootwin  
            self.w = width
            self.h = height
            self.board_color = board_color
            self.board_bg = board_bg
            
            self.info_statement = "Player X, Start the Game By Choosing a Box. Good Luck!  :)"

            # Creating a label to show information
            self.info = tk.Label(self.rootwin, text = self.info_statement)

            # Creatubg label for showing coordinates 
            self.coordinates = tk.Label(self.rootwin,text = '')
            self.canvas = tk.Canvas(self.rootwin, width = self.w, height = self.h, bg = 'white',)

            # Creating a board memory for the board
            self.boardMemory = Memory(self)
            # Winner Announced boolean
            self.winner_announced = self.boardMemory.winner_announced
            # Sets up the board
            self.setupBoard()
            # Packing the  label to show information
            self.info.pack()

    # Checks if a winner is decided
   
    def checkWinner(self):
        x = self.boardMemory.slots_takenx
        o = self.boardMemory.slots_takeno 
        statement = 'No Winners Announced'
        print(x,o)
        if self.boardMemory.winner == 'Player X Won!' or self.boardMemory.winner == 'Player O Won!'  or  self.boardMemory.winner == 'This Game is a Draw!':
            clearAll(self.rootwin)
      
        try:
                
            for i in self.boardMemory.winning_slots:
                    
                if i[0] in x and i[1] in x and i[2] in x:
                    statement = 'Player X Won!'
                    self.info.config(text = statement)
                    self.winner_announced = True 
                    self.endWindow()
                    
                elif i[0] in o and i[1] in o and i[2] in o:
                    statement = 'Player O Won!' 
                    self.info.config(text = statement)
                    self.winner_announced = True
                    self.endWindow()
                    
                elif len(list(self.boardMemory.slots.keys())) == 0 and self.winner_announced == False:
                    statement = 'This Game is a Draw!'
                    self.info.config(text = statement)  
                    self.winner_announced = True
                    self.endWindow()
        except:
            print('Failed CheckWinner', 'Statement : ', statement)
            
        finally:
            print('checkWinner Function Statement : ', statement)  
            if self.winner_announced == False:
                return statement  
            

    def moveMouse(self,event):
        
        self.coordinates.config(text = 'Coordinates X: ' + str(event.x) + ' Y: ' + str(event.y))              
   
            

    def setupBoard(self):

            # Packing the canvas on the screem
            self.canvas.pack_configure(anchor ='center')
           
            # Create lines for the Board
            self.canvas.create_line(self.w/3, 0, self.w/3, self.h, fill = self.board_color)
            self.canvas.create_line(2*self.w/3, 0, 2*self.w/3, self.h, fill = self.board_color)

            self.canvas.create_line(0, self.h/3, self.w, self.h/3, fill = self.board_color)
            self.canvas.create_line(0, 2*self.h/3, self.w, 2*self.h/3, fill = self.board_color)

            # Creating Invisible rectangeles that act as buttons
            self.canvas.create_rectangle(0 , 0, self.w/3, self.h/3,  fill = self.board_bg, tags = 1) # Box 1
            self.canvas.create_rectangle(self.w/3 , 0, 2*self.w/3, self.h/3,  fill = self.board_bg, tags = 2) # Box 2
            self.canvas.create_rectangle(2*self.w/3 , 0, self.w, self.h/3,  fill = self.board_bg, tags =3) # Box 3
            self.canvas.create_rectangle(0 , self.h/3, self.w/3, 2*self.h/3,  fill = self.board_bg, tags = 4) # Box 4
            self.canvas.create_rectangle(self.w/3 , self.h/3, 2*self.w/3, 2*self.h/3,  fill = self.board_bg, tags = 5) # Box 5
            self.canvas.create_rectangle(2*self.w/3 , self.h/3, self.w, 2*self.h/3,  fill = self.board_bg, tags = 6) # Box 6
            self.canvas.create_rectangle(0 , 2*self.h/3, self.w/3, self.h,  fill = self.board_bg, tags = 7) # Box 7
            self.canvas.create_rectangle(self.w/3 , 2*self.h/3, 2*self.w/3, self.h,  fill = self.board_bg, tags = 8) # Box 8
            self.canvas.create_rectangle(2*self.w/3 , 2*self.h/3, self.w, self.h,  fill = self.board_bg, tags = 9) # Box 9

            
            # Displaying coordinates    
            self.coordinates.pack()

            # Binding mousebutton 1 to show the coordinated when clicked
            self.canvas.bind('<Button-1>', self.moveMouse)

    def endWindow(self):
        startHumanBtn = tk.Button( self.rootwin,height = 2, width = 20, text = 'Play Again With a Friend', command = lambda :playWithFriend(self.rootwin)) 
        startComputerBtn = tk.Button(self.rootwin,height = 2, width = 20, text = 'Play Again With Computer', command = lambda : playWithComputer(self.rootwin))
        quitBtn = tk.Button(self.rootwin, height = 2, width = 20, text = 'Quit Game', command = lambda: self.rootwin.destroy())

        
        startHumanBtn.pack(pady = 10)
        startComputerBtn.pack(pady = 10)
        quitBtn.pack(pady = 10)


            

class Player(Board):
    
   
    

    def __init__(self , board, playerx = True):
        
        self.board = board
        self.playerx = playerx

        self.canvas = self.getCanvas()
                     
          
        self.setUpBoardVariables()
        self.setImages()
        self.createBlankBoxes()
        #self.bindCanvas()

    def getCanvas(self) :
        return self.board.canvas
    

    def getBoard(self):
        return self.board    


    def setUpBoardVariables(self):
        self.board = self.getBoard()
        self.boardMemory = self.board.boardMemory
        self.winner_announced = self.boardMemory.winner_announced

        self.info = self.board.info
        
        
        self.rootwin = self.board.rootwin  
        self.w = self.board.w
        self.h = self.board.h
        

        # Access noard memory's variables
        self.slots_takenx = self.boardMemory.slots_takenx
        self.slots_takeno = self.boardMemory.slots_takeno
        self.slots = self.boardMemory.slots
                       
        # Telling  memory that started with player x
        self.board.boardMemory.start_with_playerx =  self.playerx

    def setImages(self):
        # Importing image and keepin a reference so that garbage collection does not delete it
        self.ximg = itk.PhotoImage(file = 'X.png')
        self.oimg = itk.PhotoImage(file = 'O.png')

        self.labelx = tk.Label(image = self.ximg)
        self.labelo = tk.Label(image = self.oimg)

        self.x = self.labelx['image']
        self.o = self.labelo['image']


    def createBlankBoxes(self):
        #Creating Blank boxes to put image
        self.box1 = self.canvas.create_image(self.w/6, self.h/6, image = None , tags = 1 )
        self.box2 = self.canvas.create_image(self.w/2, self.h/6, image = None , tags = 2 )
        self.box3 = self.canvas.create_image(5*self.w/6, self.h/6, image = None , tags = 3)
        self.box4 = self.canvas.create_image(self.w/6, self.h/2, image = None , tags = 4 )
        self.box5 = self.canvas.create_image(self.w/2, self.h/2, image = None , tags = 5 )
        self.box6 = self.canvas.create_image(5*self.w/6, self.h/2, image = None , tags = 6 )
        self.box7 = self.canvas.create_image(self.w/6, 5*self.h/6, image = None , tags = 7 )
        self.box8 = self.canvas.create_image(self.w/2, 5*self.h/6, image = None , tags = 8 ) 
        self.box9 = self.canvas.create_image(5*self.w/6, 5*self.h/6, image = None , tags = 9 )

    def bindCanvas(self, func):
        # Binding the Button one to get the tag of the widget when clicked         
        return self.getCanvas().bind('<Button-1>', func)   

    # Changing Player Label
    def playerOneLabel(self):
        self.board.info.config(text = "Player X's Game")
    
    # Changing Player Label
    def playerTwoLabel(self):
        self.board.info.config(text = "Player O's Game")
               

        
    # Functions that displays the image of X or O
    def one(self, tag):
        #(1,2)
        if self.playerx == True:
            self.canvas.itemconfig(self.box1, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
            
        elif self.playerx == False :
            self.canvas.itemconfig(self.box1, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box One Error')

    def two(self, tag):
        #(1,2)
        if self.playerx == True:
            self.canvas.itemconfig(self.box2, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box2, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Two Error')
            
    def three(self, tag):
        #(1,3)
        if self.playerx == True:
            self.canvas.itemconfig(self.box3, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box3, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Three Error')

    def four(self, tag):
        #(2,1)
        if self.playerx == True:
            self.canvas.itemconfig(self.box4, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box4, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Four Error')

    def five(self, tag):
        #(2,2)
        if self.playerx == True:
            self.canvas.itemconfig(self.box5, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box5, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Five Error')

    def six(self, tag):
        #(2,3)
        if self.playerx == True:
            self.canvas.itemconfig(self.box6, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box6, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Six Error')

    def seven(self, tag):
        #(3,1)
        if self.playerx == True:
            self.canvas.itemconfig(self.box7, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box7, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Seven Error')

    def eight(self, tag):
        #(3,2)
        if self.playerx == True:
            self.canvas.itemconfig(self.box8, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box8, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Eight Error')

    def nine(self, tag):
        #(3,3)
        if self.playerx == True:
            self.canvas.itemconfig(self.box9, image = self.x)
            self.playerx = False
            del self.slots[tag]
            self.slots_takenx.append(tag)
            self.playerTwoLabel()
        elif self.playerx == False :
            self.canvas.itemconfig(self.box9, image = self.o)
            self.playerx = True
            del self.slots[tag]
            self.slots_takeno.append(tag)
            self.playerOneLabel()
        else:
            print('Box Nine Error')
   
        
       
class Human(Player):
    def __init___(self , board, playerx = True):
        
        super().__init__(board, playerx)


    def play(self):
        self.bindCanvas(self.nearestWidget)
        
        
    # def bindCanvas(self):
    #     # Binding the Button one to get the tag of the widget when clicked         
    #     self.canvas.bind('<Button-1>', self.nearestWidget)   

    def nearestWidget(self,event):

    # Getting the nearest psudo widget
    
    
        def onObjectClick(event):  
            #print('Got object click at ', event.x, event.y)
            item = event.widget.find_closest(event.x, event.y)
            #print(self.canvas.gettags(item))
            tag = self.canvas.gettags(item)[0]
            #print(tag)
            return int(tag)

        if self.winner_announced == False:
            tag = onObjectClick(event)

            # Calling the corresponding funtions to display X or O images according to the clicked coordinated
            if tag not in self.slots_takenx and tag not in self.slots_takeno:
                if tag == 1:  self.one(tag)  
                elif tag == 2:  self.two(tag)
                elif tag == 3:  self.three(tag)
                elif tag == 4:  self.four(tag)
                elif tag == 5:  self.five(tag)
                elif tag == 6:  self.six(tag)
                elif tag == 7:  self.seven(tag)
                elif tag == 8:  self.eight(tag)
                elif tag == 9:  self.nine(tag)
                # Checking if the prevous move decided a winner
                self.boardMemory.winner = self.checkWinner()
                if self.winner_announced == True:
                    
                    self.canvas.unbind('<Button-1>', self.nearestWidget)
                
            else:
                print('Click Function not called')

             
class Computer(Player):
    def __init___(self , board, playerx = True):
        super().__init__(board, playerx)
        


    def play(self):
        self.bindCanvas(self.nearestWidgetC)

    def computerMove(self):
                    
                if self.playerx == False:
                    #computer_choice = self.computerRandom()
                    computer_choice = self.computerAI()
                    if computer_choice == 1:  self.one(computer_choice)  
                    elif computer_choice == 2:  self.two(computer_choice)
                    elif computer_choice == 3:  self.three(computer_choice)
                    elif computer_choice == 4:  self.four(computer_choice)
                    elif computer_choice == 5:  self.five(computer_choice)
                    elif computer_choice == 6:  self.six(computer_choice)
                    elif computer_choice == 7:  self.seven(computer_choice)
                    elif computer_choice == 8:  self.eight(computer_choice)
                    elif computer_choice == 9:  self.nine(computer_choice)
                    print('AI Choice', computer_choice)
                    print('Calling computer check winner')  

                    self.boardMemory.winner = self.checkWinner()
                    if self.winner_announced == True:
                        self.canvas.unbind('<Button-1>', self.bindCanvas(self.nearestWidgetC))
                        self.info.config(text = 'The Computer Has Won!')
                        
                    elif self.winner_announced == False:
                        self.playerx = True              
                   
                    


    def nearestWidgetC(self,event):

    # Getting the nearest psudo widget
    
    
        def onObjectClick(event):  
            #print('Got object click at ', event.x, event.y)
            item = event.widget.find_closest(event.x, event.y)
            #print(self.canvas.gettags(item))
            tag = self.canvas.gettags(item)[0]
            #print(tag)
            return int(tag)

        tag = onObjectClick(event)

        # Calling the corresponding funtions to display X or O images according to the clicked coordinated
        if tag not in self.slots_takenx and tag not in self.slots_takeno and tag in list(self.slots.keys()):
            if self.playerx == True:
                if tag == 1:  self.one(tag)  
                elif tag == 2:  self.two(tag)
                elif tag == 3:  self.three(tag)
                elif tag == 4:  self.four(tag)
                elif tag == 5:  self.five(tag)
                elif tag == 6:  self.six(tag)
                elif tag == 7:  self.seven(tag)
                elif tag == 8:  self.eight(tag)
                elif tag == 9:  self.nine(tag)
                                   
                # Checking if the prevous move decided a winner
                self.boardMemory.winner = self.checkWinner()
                
                if self.winner_announced == False:
                                    
                    self.computerMove()
                    
                elif self.winner_announced == True:
                    self.canvas.unbind('<Button-1>', self.bindCanvas(self.nearestWidgetC))
                    
                    
            else:
                print('OnObjectClick Function not called')
            
                
            
            
    def computerAI(self):
        print("I'm Here")
        mcts = MCTS(self.boardMemory,main_player_x=False)
        return mcts.Simulate(mcts.root,1000) 

class TreeNode():
    def __init__(self, value, bMemory=None,parent=None):
        self.value = value
        #setting the score to 0 at start
        self.score = 0
        #setting the number of visits the node to zero
        self.visits =0

        # To backPropogate we need a parant Node
        self.parent = parent

        # Getting the memory of the current board 
        #self.memory = copy(bMemory)

        # Creating a set for children of the node
        self.children = dict()

        
        self.is_terminal_node = False
        
        self.is_fully_expanded = False

    
        


class MCTS():
    def __init__(self, bMemory,value=None, main_player_x = True):
        
        self.best_moves = []
        self.memory = self.copyMemory(bMemory)
        self.root = TreeNode(value,self.memory)
        self.current = self.root
        self.my_slots = copy(self.memory.slots)
        # main player is the player want to win
        self.main_player_x = main_player_x
        self.player_x = self.main_player_x
        self.slots_takenx = copy(self.memory.slots_takenx)
        self.slots_takeno = copy(self.memory.slots_takeno)
        self.winning_slots = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]
        self.winner_announced = False
    def resetSlots(self):
        self.my_slots = copy(self.memory.slots)
        self.player_x = copy(self.main_player_x)
        self.slots_takenx = copy(self.memory.slots_takenx)
        self.slots_takeno = copy(self.memory.slots_takeno)
        self.winner_announced = False

    def copyMemory(self, bMemory):
        memory = Memory(None)
        

        # Setting the winner string to empty 
        memory.winner = bMemory.winner

        # Tells memory whether the game started with player X
        memory.start_with_playerx = bMemory.start_with_playerx
        #Winner announced boolean 
        memory.winner_announced = bMemory.winner_announced
        # Counting the moves made my the players
        memory.playerx_moves = bMemory.playerx_moves
        memory.playero_moves = bMemory.playero_moves
        memory.total_moves = bMemory.total_moves

        # Slots that when a certain player occupies, he/she is decided a winner
        memory.winning_slots = bMemory.winning_slots

        # This is the total number of slots, but here we use it to delete taken slots so that images are not overwritten
        memory.slots = bMemory.slots
        memory.slots_takenx  =bMemory.slots_takenx
        memory.slots_takeno = bMemory.slots_takeno
        return memory

    def Select(self, node):
        ptr = node
        # Make we are dealing with a non terminal node
        while not ptr.is_terminal_node:
            # if the node is fully expanded we can get the  best move
            if ( node.is_fully_expanded):
                pass


    def randomMoveGenerator(self, node):
        if len(self.my_slots) == 0:
            raise ArithmeticError("Moves Finished! No more random moves.")
        
        choice = random.choice(list(self.my_slots.keys()))
        
        return choice
    def deleteChoice(self, node, choice):
        if len(self.my_slots) == 0:
            raise ArithmeticError("Move deletion failed.")
        try:
            if self.player_x:
                self.slots_takenx.append(choice)
                self.player_x =False
            else:
                self.slots_takeno.append(choice)
                self.player_x =True 
            # deleteing from slots set
            del self.my_slots[choice]
        except:
            raise   ArithmeticError("Move deletion failed. 2")


    # Simulate a single game
    def Simulate(self,node ,iterations):
        root_node = node
        for iteration in range(iterations):
                score, end_node = self.Rollout(root_node)
                root_node = self.BackPropogate(end_node,score)
                

        try:
            return self.getBestMove(root_node,2).value
        except:
            ValueError("Best Move not returned ID : 3")

                


            
    def BackPropogate(self,node, score): # score is 1 is win -1 is lost or 0 if draw
        if( not node.is_terminal_node ):
            print("Warning ! Backpropogation is not from a terminal node.")
        else:
            return_node= node
            ptr = node
            while(ptr):
                ptr.visits +=1
                if(score ==1):
                    ptr.score +=score
                elif(score ==-1):
                    ptr.score -=score
                return_node = ptr
                ptr = ptr.parent
            return return_node
            
    def Expand(self, node, choice):
        # Getting all the possible states 
        free_slots = list(self.my_slots.values()) # it is a slot number list

        if(len(free_slots)==len(list(node.children.keys()))):
            node.is_fully_expanded = True
        #for free_slot in free_slots:
            # Make sure that the current state in states is not already present among child nodes
        elif choice not in list(node.children.keys()):
                #create a new node
                new_node = TreeNode(choice, parent =node)
                
                # add child node to parent's node children list (dict)
                node.children[choice] = new_node
    def isFullyExpanded(self,node): #returns a booloean       
        """
        When can a node become fully expanded?
        
        when the all of the free slots in memory is in children

        """
        ans = True
        for i in self.my_slots.values():
            if i not in node.children:
                ans = False
                break
        node.is_fully_expanded = ans             
                

        """       
        #warning
        if len(free_slots) != len(node.children.keys()) :
            print("Out of Bounds! Shouldn't be here. ID: 0")
        """

    def Rollout(self,node):
        # play randomly on both sides until winner is announced
        score = 0
        ptr = node 
        statement = None
        while(not self.winner_announced):

            try:    

                
                random_choice = self.randomMoveGenerator(ptr)
                # if the node has no child nodes then we make the child node 
                if len(ptr.children)< len(self.my_slots) :
                    self.Expand(ptr,random_choice)
                    self.isFullyExpanded(ptr)
                self.deleteChoice(ptr,random_choice)
                statement = self.checkWinner()
                #if(not self.winner_announced):
                ptr = ptr.children[random_choice]
            except:
                raise ValueError("Out of moves! Error ID 1")
        ptr.is_terminal_node = self.winner_announced  
        # Resetomg slots after reaching the end of a game
        self.resetSlots()
  
        # Now after we reach the end
        
        # if our main player is x we want to return a postive score if x wins
        
        if (self.main_player_x):
            if statement == 'Player X Won!':
                score = 1
            elif statement == 'Player O Won!':
                score = -1
                       
        # if our main player is o we want to return a postive score if x wins
        elif(not self.main_player_x):
            if statement == 'Player O Won!':
                 score = 1
            elif statement == 'Player X Won!':
                score = -1
        
        return (score, ptr)  
            
    # finally after Backpropogation we need to get the best move this returns a node
    def getBestMove(self, node ,exploration_constant, main_player=True):
        best_score = float('-inf')
        best_moves =  []
        if main_player:
            current_player = 1
        else :
            #if we want maximum score for the opponent then we'd have to multiply the move score by -1 to make it postive 
            current_player = -1

        # loop over all the child nodes
        for child_node in node.children.values():
            move_score = current_player *  (child_node.score / child_node.visits) + (exploration_constant) *  sqrt( log(node.visits/child_node.visits) )

            # Case where a better move has been found
            if move_score> best_score:
                best_score = move_score
                best_moves = [child_node]
            # Case where a move has been found that is as good as the one we have
            elif move_score == best_score:
                best_moves.append(child_node)
        
        # return one of the best moves randomly
        return random.choice(best_moves)

    def checkWinner(self):
        x = self.slots_takenx
        o = self.slots_takeno 
        statement = 'No Winners Announced'
        print(x,o)
        """
        if self.winner == 'Player X Won!' or self.winner == 'Player O Won!'  or  self.boardMemory.winner == 'This Game is a Draw!':
            clearAll(self.rootwin)
        """
        try:
            if(not self.winner_announced):    
                for i in self.winning_slots:
                        
                    if i[0] in x and i[1] in x and i[2] in x:
                        statement = 'Player X Won!'
                        
                        self.winner_announced = True 
                        
                        
                    elif i[0] in o and i[1] in o and i[2] in o:
                        statement = 'Player O Won!' 
                        
                        self.winner_announced = True
                        
                        
                    elif len(list(self.my_slots)) == 0 and self.winner_announced == False:
                        statement = 'This Game is a Draw!'
                        self.winner_announced = True
            else:
                raise ValueError("Winner Previouly Announced! This function should not be called again.")        
        except:
            print('Failed CheckWinner Inside MCTS', 'Statement : ', statement)
            
        finally:
            print('checkWinner Function Statement Inside MCTS : ', statement)  
            
            return statement


if __name__ =="__main__":
    # Creating and labeling the master window 
    master = tk.Tk()
    master.geometry('1000x1000')
    master.title('Tic Tac Toe Game')


    
    startHumanBtn = tk.Button( master, height = 5, width = 20, text = 'Play With a Friend', command = lambda :playWithFriend(master)) 
    startComputerBtn = tk.Button(master, height = 5, width = 20, text = 'Play With Computer', command = lambda : playWithComputer(master))
    quitBtn = tk.Button(master, height = 5, width = 20, text = 'Quit Game', command = lambda: master.destroy())



    startHumanBtn.pack(pady = 10)
    startComputerBtn.pack(pady = 10)
    quitBtn.pack(pady = 10)

    master.mainloop()

