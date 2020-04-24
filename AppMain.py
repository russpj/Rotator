from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock


# BoardLayout encapsulates the playing board
class BoardLayout(BoxLayout):
	def __init__(self, numCells):
		super().__init__()
		self.numCells = numCells
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def InterpolateColor(self, beginColor, endColor, ratio):
		betweenColor = []
		for colorIndex in range(len(beginColor)):
			betweenColor.append(beginColor[colorIndex]*ratio + endColor[colorIndex]*(1-ratio))
		return betweenColor

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.1, .3, 0.1, 1)  # green; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
		
		self.rectangles = []
		pos = [0,0]
		posNext = [self.rect.size[0]/self.numCells, 0]
		beginColor = [0.0, .75, .25, 1]
		endColor = [0.0, .25, .75, 1]
		with self.canvas:
			for cell in range(self.numCells):
				betweenColor = self.InterpolateColor(beginColor, endColor, float(cell)/self.numCells)
				Color(betweenColor[0], betweenColor[1], betweenColor[2], betweenColor[3])
				size = [posNext[0]-pos[0], self.rect.size[1]]
				rect= Rectangle(size=size, pos=pos)
				self.rectangles.append(rect)
				pos = posNext.copy()
				posNext = [self.rect.size[0]*cell/self.numCells, 0]
			

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size

		numCells = len(instance.rectangles)
		for cell in range(numCells):
			rect = instance.rectangles[cell]
			pos = [instance.pos[0]+instance.size[0]*cell/numCells, instance.pos[1]]
			size = [instance.pos[0]+instance.size[0]*(cell+1)/numCells-pos[0], instance.size[1]]
			rect.pos = pos
			rect.size = size


class HeaderLayout(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(orientation='horizontal', **kwargs)
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.6, .6, 0.1, 1)  # yellow; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
		self.statusLabel = Label(text='Ready', color = [0.7,0.05, 0.7, 1])
		self.add_widget(self.statusLabel)
		self.fpsLabel = Label(text='0 fps', color=[0.7, 0.05, 0.7, 1])
		self.add_widget(self.fpsLabel)
		
	def UpdateText(self, fps=0, statusText='Ready'):
		self.fpsLabel.text = '{fps:.0f} fps'.format(fps=fps)
		self.statusLabel.text = statusText

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size


class FooterLayout(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(orientation='horizontal', padding=10, **kwargs)
		self.running = False
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.4, .1, 0.4, 1)  # purple; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
		
		self.startButton = Button(text='')
		self.add_widget(self.startButton)
		self.UpdateStartButtonText()
		self.startButton.bind(on_press=self.HandleStartButton)

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size

	def HandleStartButton(self, instance):
		self.running = not self.running
		self.UpdateStartButtonText()

	def UpdateStartButtonText(self):
		if self.running:
			self.startButton.text = 'Pause'
		else:
			self.startButton.text = 'Start'

	def IsPaused(self):
		return not self.running

	def SetButtonsState(self, start_button_text):
		if start_button_text == 'Pause':
			self.running = True;
		if start_button_text == 'Start':
			self.running = False
		self.UpdateStartButtonText()


class Rotator(App):
	def build(self):
		self.root = layout = BoxLayout(orientation = 'vertical')

		# header
		self.header = HeaderLayout(size_hint=(1, .1))
		layout.add_widget(self.header)

		# board
		self.boardLayout = boardLayout = BoardLayout(10)
		layout.add_widget(boardLayout)

		# footer
		self.footer = FooterLayout(size_hint=(1, .2))
		layout.add_widget(self.footer)

		# self.solver = SudokuSolver(easyBoard, yieldLevel=0)
		# board = self.solver.board
		# self.boardLayout.InitBoard(board)

		# self.generator = self.solver.Generate()
		Clock.schedule_interval(self.FrameN, 0.0)

		return layout

	def FrameN(self, dt):
		if dt != 0:
			fpsValue = 1/dt
		else:
			fpsValue = 0
		if self.footer.IsPaused():
			return

		try:
			# result = next(self.generator)
			self.UpdateText(fps=fpsValue)
		except StopIteration:
			# kill the timer
			self.UpdateText(fps=fpsValue, updatePositions = self.footer.IsPaused)
			self.footer.SetButtonsState(start_button_text = 'Start')
			

	def UpdateText(self, fps, updatePositions = True):
		self.header.UpdateText(fps = fps)

def Main():
	Rotator().run()

if __name__ == '__main__':
	Main()

