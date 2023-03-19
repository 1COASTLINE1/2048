import tkinter as tk
import tkinter.messagebox
# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark
from a3_support import *
# Write your classes here

class Model:
	def __init__(self) -> None:
		"""
		Constructs a new 2048 model instance. This includes setting up a new game (see new_game
		method below).	
		"""
		self.new_game()
	def new_game(self) -> None:
		"""
		Sets, or resets, the game state to an initial game state. Any information is set to its initial
		state, the tiles are all set to empty, and then two new starter tiles are randomly generated
		(see the add_tile method below).
		"""
		
		self._undos_remaining=1#number of undos remaining
		self._score=0#score
		self._previous_board=[]#previous board
		self._previous_score=0#previous score
		self._board = [[None for _ in range(4)] for _ in range(4)] #reset the board
		self.add_tile()
		self.add_tile()
	def get_tiles(self) -> list[list[Optional[int]]]:
		"""
		Return the current tiles matrix. Each internal list represents a row of the grid, ordered from
		top to LEFT. Each item in each row list is the integer value on the tile occupying that
		space, or None if no tile is occupying that space.
		"""
		return self._board
	def add_tile(self) -> None:
		"""
		Randomly generate a new tile at an empty location (you must use generate_tile for this)
		and add it to the current tiles matrix.
		"""
		tile=generate_tile(self._board)
		row=tile[0][0]
		col=tile[0][1]
		value=tile[1]
		self._board[row][col]=value		
	def move_left(self) -> None:	
		"""
		Moves all tiles to their left extreme, merging where necessary. This involves stacking all tiles
		to the left, merging to the left, and then restacking to the left to fill in any gaps created. If
		you are keeping track of a score (see Task 2), this method should also add any points gained
		from the move to the total score.
		"""	
		self._previous_score=self.get_score()
		self._previous_board=self.get_tiles()
		self._board=stack_left(self._previous_board)
		board,value=combine_left(self._board)
		self._board=board
		self._score+=value
		self._board=stack_left(self._board)			
	def move_right(self) -> None: 
		"""Moves all tiles to their right extreme, merging where necessary. This can be achieved by reversing the tiles matrix, moving left, and then reversing
		the matrix again. If you are keeping track of a score (see Task 2), this method should also
		result in gained points being added to the total score.
		"""
		self._previous_score=self.get_score()
		self._previous_board=self.get_tiles()
		self._board=reverse(self._board)
		self._board=stack_left(self._board)
		board,value=combine_left(self._board)
		self._board=board
		self._score+=value
		self._board=stack_left(self._board)
		self._board=reverse(self._board)
	def move_up(self) -> None:
		"""
		Moves all tiles to their top extreme, merging where necessary. This can be achieved by
		transposing the tiles matrix, moving left, and then transposing the matrix again. If you are
		keeping track of a score (see Task 2), this method should also result in gained points being
		added to the total score.
		"""
		self._previous_score=self.get_score()
		self._previous_board=self.get_tiles()
		self._board=transpose(self._board)
		self._board=stack_left(self._board)
		board,value=combine_left(self._board)
		self._board=board
		self._score+=value
		self._board=stack_left(self._board)
		self._board=transpose(self._board)		
	def move_down(self) -> None:
		"""
		Moves all tiles to their LEFT extreme, merging where necessary. This can be achieved by
		transposing the tiles matrix, moving right, and then transposing the matrix again. If you
		are keeping track of a score (see Task 2), this method should also result in gained points
		being added to the total score.
		"""
		self._previous_score=self.get_score()
		self._previous_board=self.get_tiles()
		self._board=transpose(self._board)
		self._board=reverse(self._board)
		self._board=stack_left(self._board)
		board,value=combine_left(self._board)
		self._board=board
		self._score+=value
		self._board=stack_left(self._board)
		self._board=reverse(self._board)
		self._board=transpose(self._board)		
	def attempt_move(self, move: str) -> bool:
		"""
		Makes the appropriate move according to the move string provided. Returns True if the
		move resulted in a change to the game state, else False. The move provided must be one
		of wasd (this is a pre-condition, not something that must be handled within this method).
		"""
		board1=self._board
		score1=self._score
		previous=self._previous_board
		if move=='w':
			self.move_up()
			if self._board!=board1:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return True
			else:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return False
		elif move=='a':
			self.move_left()
			if self._board!=board1:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return True
			else:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return False
		elif move=='s':
			self.move_down()
			if self._board!=board1:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return True
			else:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return False
		elif move=='d':
			self.move_right()
			if self._board!=board1:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return True
			else:
				self._board=board1
				self._score=score1
				self._previous_board=previous
				return False
	def has_won(self) -> bool:
		"""
		Returns True if the game has been won, else False. The game has been won if a 2048 tile
		exists on the grid.
		"""	
		for tuple in self._board:
			for tile in tuple:
				if tile==2048:
					return True
				else:
					return False
	def has_lost(self) -> bool:

		"""
		Returns True if the game has been lost, else False. The game has been lost if there are
		no remaining empty places in the grid, but no move would result in a change to the game
		state.
		"""
		if self.attempt_move('w')==False and self.attempt_move('a')==False and self.attempt_move('s')==False and self.attempt_move('d')==False:
			return True
		else:
			return False		
	def get_score(self) -> int:
		"""
		Returns the current score for the game. Each time a new tile is
		created by a merge, its new value should be added to the score. The total score to be added
		after a merge is calculated for you by the combine_left function in a3_support.py
		"""
		return self._score
	def get_undos_remaining(self) -> int:
		"""
		Get the number of undos the player has remaining.
		This should start at 3 at the beginning of a new game, and reduce each time an undo is
		used
		"""
		return self._undos_remaining
	def check_board(self)->bool:
		"""
		check whether the player has moved the board or not return true if the player has moved the board
		"""
		number=0
		for i in range(4):
			for j in range(4):
				if self._board[i][j]==None:
					number+=1
		if number==14:
			return False
		else:
			return True
	def use_undo(self) -> None:
		"""
		Attempts to undo the previous move, returning the current tiles
		to the previous tiles state before the last move that made changes to the tiles matrix. If the
		player does not have any undos remaining, or they are back at the initial state, this method
		should do nothing.
		"""
		if self._undos_remaining >0 and self.check_board():
			self._board=self._previous_board
			self._score=self._previous_score
			self._undos_remaining-=1
	def deep_copy(self,board:list[list[Optional[int]]],s)->list[list[Optional[int]]]:
		"""
		return a deep copy of the board and the score
		"""
		board=self._board
		score=self._score
		return board,score
class GameGrid(tk.Canvas):

	SIDE_LENGTH=95 #the size of a single box
	OUTTER_PADDING=10#padding between boxes and the edge of the canvas
	def __init__(self, master: tk.Tk, **kwargs) -> None:
		"""
		Sets up a new GameGrid in the master window. **kwargs is used to allow GameGrid to
		support any named arguments supported by tk.Canvas. The canvas should be 400 pixels
		wide and 400 pixels tall.
		"""
		self.colour="#ccc0b3"
		self.colour2=DARK
		super().__init__(
			master,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
			background=BACKGROUND_COLOUR,
            **kwargs

        )
	def get_Coordinate(self,row:int,col:int) -> tuple[tuple[int,int],tuple[int,int]]:
		"""
		Return the graphics which is used to draw the box in the grid.
		"""
		#return the graphics coordinates for the top left corner of the cell at the given (row, col) position.
		x_min=col*self.SIDE_LENGTH+self.OUTTER_PADDING
		y_min=row*self.SIDE_LENGTH+self.OUTTER_PADDING
		#return the graphics coordinates for the LEFT right corner of the cell at the given (row, col) position.
		x_max=x_min+self.SIDE_LENGTH
		y_max=y_min+self.SIDE_LENGTH
		return (x_min,y_min),(x_max,y_max)
	def choose_colour(self,row:int,col:int,tiles:list[list[Optional[int]]])->str:
		if tiles[row][col]==None:
			self.colour="#ccc0b3"
		if tiles[row][col]==2:
			self.colour="#fcefe6"
			self.colour2=DARK
		if tiles[row][col]==4:
			self.colour="#f2e8cb"
			self.colour2=DARK
		if tiles[row][col]==8:
			self.colour="#f5b682"
			self.colour2=LIGHT
		if tiles[row][col]==16:
			self.colour="#f29446"
			self.colour2=LIGHT
		if tiles[row][col]==32:
			self.colour="#ff775c"
			self.colour2=LIGHT
		if tiles[row][col]==64:
			self.colour="#e64c2e"
			self.colour2=LIGHT
		if tiles[row][col]==128:
			self.colour="#ede291"
			self.colour2=LIGHT
		if tiles[row][col]==256:
			self.colour="#fce130"
			self.colour2=LIGHT
		if tiles[row][col]==512:
			self.colour="#ffdb4a"
			self.colour2=LIGHT
		if tiles[row][col]==1024:
			self.colour="#f0b922"
			self.colour2=LIGHT
		if tiles[row][col]==2048:
			self.colour="#fad74d"
			self.colour2=LIGHT
		return self.colour,self.colour2
	def _draw_box(self,row:int,col:int,tiles:list[list[Optional[int]]]) -> None:
		"""
		Draws the given box in the grid.
		"""
		(x_min,y_min),(x_max,y_max)=self.get_Coordinate(row,col)
		self.create_rectangle(
			x_min+BUFFER/2,y_min+BUFFER/2,
			x_max,y_max,
			fill=self.choose_colour(row,col,tiles)[0],
			width=1
		)
		x_middle,y_middle=self._get_midpoint((row,col))
		if tiles[row][col]!=None:
			self.create_text(
					x_middle+5,y_middle+5,
					text = f"{tiles[row][col]}", 
					fill = self.choose_colour(row,col,tiles)[1], 
					font = TILE_FONT
				)
	
	def flash(self,tiles:list[list[Optional[int]]]) -> None: 
		"""
		generate 16 boxes in the grid randomly.
		"""
		for row in range(4):
			for col in range(4):
				self._draw_box(row,col,tiles)
	
	def _get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
		"""
		Return the bounding box for the (row, column) position, in the form
		(x_min, y_min, x_max, y_max).
		Here, (x_min, y_min) is the top left corner of the position with 10 pixels of padding
		added, and (x_max, y_max) is the LEFT right corner of the cell with 10 pixels of padding
		subtracted.
		"""
		(x_min,y_min),(x_max,y_max)=self.get_Coordinate(position)
		return (x_min,y_min,x_max,y_max)
	def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
		"""
		Return the graphics coordinates for the center of the cell at the given (row, col) position.
		"""
		(x_min,y_min),(x_max,y_max)=self.get_Coordinate(position[0],position[1])
		return ((x_min+x_max)//2,(y_min+y_max)//2)
	def clear(self) -> None:
		"""
		Clears all items.
		"""
		self.delete(tk.ALL)
	def redraw(self, tiles: list[list[Optional[int]]]) -> None:
		"""
		Clears and redraws the entire grid based on the given tiles.
		"""
		self.clear()
		self.flash(tiles)
class Game:
	def __init__(self, master: tk.Tk) -> None:
		"""
		Constructs a new 2048 game. This method should create a Model instance, set the window
		title, create the title label and create instances of any view classes packed into master. It
		should also bind key press events to an appropriate handler, and cause the initial GUI to
		be drawn.
		"""
		self.master=master
		self.master.title("CSSE1001/7030 2022 Semester 2 A3")
		title = tk.Label(text="2048", background="yellow", fg="white", font=TITLE_FONT)
		title.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.model=Model()

		self.grid=GameGrid(master)
		self.grid.pack()

		self.grid1=StatusBar(master)
		self.grid1.pack()

		self.master.bind("<Key>", self.attempt_move)
		self.grid1.set_callbacks(self.start_new_game,self.undo_previous_move)
		self.grid.redraw(self.model._board)
		self.master.mainloop()
	def draw(self) -> None:
		"""
		Redraws any view classes based on the current model state
		"""
		self.grid.redraw(self.model._board)
	def attempt_move(self, event: tk.Event) -> None:
		"""
		Attempt a move if the event represents a key press on character a, w, s, or d. Once
		a move has been made, this method should redraw the view, display the appropriate messagebox if the game has been won, or create a new tile after 150ms if the game has not been
		won
		"""	
		if event.keysym=="w":
			self.model.move_up()
			self.grid.redraw(self.model._board)
			self.grid1.redraw_infos(self.model.get_score(),self.model.get_undos_remaining())
		if event.keysym=="s":
			self.model.move_down()
			self.grid.redraw(self.model._board)
			self.grid1.redraw_infos(self.model.get_score(),self.model.get_undos_remaining())
		if event.keysym=="a":
			self.model.move_left()
			self.grid.redraw(self.model._board)
			self.grid1.redraw_infos(self.model.get_score(),self.model.get_undos_remaining())
		if event.keysym=="d":
			self.model.move_right()
			self.grid.redraw(self.model._board)
			self.grid1.redraw_infos(self.model.get_score(),self.model.get_undos_remaining())
		if self.model.has_won()==True:
			tkinter.messagebox.showinfo(WIN_MESSAGE)
		else:
			if event.keysym == 'w' or event.keysym == 's' or event.keysym == 'a' or event.keysym == 'd':
				self.master.after(150, self.new_tile)	
	def new_tile(self) -> None:
		"""
		Adds a new tile to the model and redraws. If the game has
		been lost with the addition of the new tile, then the player should be prompted with the
		appropriate messagebox displaying the LOSS_MESSAGE.
		"""
		self.model.add_tile()
		self.draw()
		if self.model.has_lost()==True:
			tkinter.messagebox.showinfo('2048',LOSS_MESSAGE)
	def undo_previous_move(self) -> None:
		"""
		 A handler for when the 'Undo' button is pressed in
		the status bar. This method should attempt to undo the last action, and then redraw the
		view classes with the updated model information.
		"""
		self.model.use_undo()
		self.grid1.redraw_infos(self.model.get_score(),self.model.get_undos_remaining())
		self.grid.redraw(self.model._board)
	def start_new_game(self) -> None:
		"""
		A handler for when the 'New Game' button is pressed
		in the status bar. This method should cause the model to set its state to that of a new
		game, and redraw the view classes to reflect these changes. Note: The new game should not
		replicate the initial state of the previous game. The new game state should be the result of
		calling the new_game method on the Model instance.
		"""
		self.model.new_game()
		self.grid1.redraw_infos(self.model.get_score(),self.model.get_undos_remaining())
		self.draw()
class StatusBar(tk.Frame):
	def __init__(self, master: tk.Tk,**kwargs):
		"""
		Sets up self to be an instance of tk.Frame
		and sets up inner frames, labels and buttons in this status bar.
		"""
		super().__init__(master, **kwargs)
		frame1=tk.Frame(self,bg="#bbada0")#one that contains score
		frame1.pack(side=tk.LEFT,anchor=tk.W,padx=10)
		frame2=tk.Frame(self,bg="#bbada0")#one that contains undo 
		frame2.pack(side=tk.LEFT,anchor=tk.W,expand=1)
		#construct the score label
		self._score_label = tk.Label(frame1, text="SCORE",bg=BACKGROUND_COLOUR, fg="#ccc0b3", font=('Arial bold', 25))
		self._score_label.pack(side=tk.TOP,anchor=tk.N,ipadx=5)
		self._score1_label=tk.Label(frame1,text="0",bg=BACKGROUND_COLOUR,fg="#f5ebe4",font=('Arial bold', 15))
		self._score1_label.pack(side=tk.TOP)

		#construct the undo button
		self._undos_label=tk.Label(frame2,text="UNDOS",bg=BACKGROUND_COLOUR, fg="#ccc0b3", font=('Arial bold', 25))
		self._undos_label.pack(side=tk.TOP,anchor=tk.N,ipadx=5)
		self._undos1_label=tk.Label(frame2,text="1",bg=BACKGROUND_COLOUR, fg="#f5ebe4", font=('Arial bold', 15))
		self._undos1_label.pack(side=tk.TOP)
		#construct the new game button
		self._new_game_button = tk.Button(self, text="New Game")
		self._new_game_button.pack(side=tk.TOP, anchor=tk.E,padx=10,pady=10)
		self._undo_button = tk.Button(self, text="Undo Move")
		self._undo_button.pack(side=tk.TOP,anchor=tk.E, padx=10,pady=10)
	def redraw_infos(self, score: int, undos: int) -> None:
		"""
		Updates the score and undos
		labels to reflect the information given
		"""
		self._score1_label.configure(text=score)
		self._undos1_label.configure(text=undos)
	def set_callbacks(self, new_game_command: callable, undo_command: callable):
		"""
		Sets the commands for the new game and undo buttons to the given commands. 
		The arguments here are references to functions to be called when the buttons are pressed.
		"""
		self._new_game_button.config(command=new_game_command)
		self._undo_button.config(command=undo_command)

def play_game(root):
	# Add a docstring and type hints to this function
	# Then write your code here
	game=Game(root)

	

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()
