
"""
Simple fishing game with GUI using tkinter.

Controls:
 - Click 'Cast' to drop the bait.
 - Click 'Reel' to reel in. If a fish is on the hook you catch it.
 - Fish swim horizontally; hooking happens when bait overlaps a fish.
"""
from tkinter import Tk, Canvas, Button, Label
import random


class Fish:
	def __init__(self, canvas, x, y, speed, color):
		self.canvas = canvas
		self.x = x
		self.y = y
		self.speed = speed
		self.color = color
		self.id = canvas.create_oval(x-20, y-10, x+20, y+10, fill=color, outline='')

	def move(self):
		self.x += self.speed
		if self.x > self.canvas.winfo_width() + 30:
			self.x = -30
		if self.x < -30:
			self.x = self.canvas.winfo_width() + 30
		self.canvas.coords(self.id, self.x-20, self.y-10, self.x+20, self.y+10)


class FishingGame:
	def __init__(self, root):
		self.root = root
		root.title('Fishing Game')
		self.canvas = Canvas(root, width=600, height=400, bg='#87CEEB')
		self.canvas.pack()

		# water
		self.canvas.create_rectangle(0, 200, 600, 400, fill='#1E90FF', outline='')

		self.score = 0
		self.score_label = Label(root, text=f'Score: {self.score}')
		self.score_label.pack()

		self.cast_btn = Button(root, text='Cast', command=self.cast)
		self.cast_btn.pack(side='left', padx=10, pady=5)
		self.reel_btn = Button(root, text='Reel', command=self.reel)
		self.reel_btn.pack(side='left', padx=10, pady=5)

		# bait state
		self.bait_x = 300
		self.bait_y = 190
		self.bait_id = None
		self.bait_dropped = False
		self.hooked_fish = None

		# create fishes
		colors = ['orange', 'yellow', 'red', 'green', 'purple']
		self.fishes = []
		for i in range(5):
			x = random.randint(0, 600)
			y = random.randint(230, 370)
			speed = random.choice([1, 2, -1, -2])
			f = Fish(self.canvas, x, y, speed, random.choice(colors))
			self.fishes.append(f)

		# draw rod top
		self.canvas.create_line(300, 0, 300, 190, fill='sienna', width=4)
		self.root.after(50, self.update)

	def cast(self):
		if self.bait_dropped:
			return
		self.bait_dropped = True
		self.bait_y = 190
		if self.bait_id:
			self.canvas.delete(self.bait_id)
		self.bait_id = self.canvas.create_oval(self.bait_x-6, self.bait_y-6, self.bait_x+6, self.bait_y+6, fill='brown')

	def reel(self):
		if not self.bait_dropped:
			return
		# check hooked fish
		if self.hooked_fish:
			# catch fish
			try:
				self.canvas.delete(self.hooked_fish.id)
			except Exception:
				pass
			self.fishes.remove(self.hooked_fish)
			self.hooked_fish = None
			self.score += 1
			self.score_label.config(text=f'Score: {self.score}')
		# remove bait
		if self.bait_id:
			self.canvas.delete(self.bait_id)
			self.bait_id = None
		self.bait_dropped = False

	def update(self):
		# move fishes
		for f in list(self.fishes):
			f.move()

		# update bait if dropped
		if self.bait_dropped:
			# lower bait until depth
			if self.bait_y < 360 and not self.hooked_fish:
				self.bait_y += 6
			# if hooked, bait follows fish
			if self.hooked_fish:
				self.bait_x = self.hooked_fish.x
				self.bait_y = self.hooked_fish.y - 12
			self.canvas.coords(self.bait_id, self.bait_x-6, self.bait_y-6, self.bait_x+6, self.bait_y+6)

			# check collision with fishes
			if not self.hooked_fish:
				for f in self.fishes:
					if abs(f.x - self.bait_x) < 24 and abs(f.y - self.bait_y) < 16:
						self.hooked_fish = f
						break

		# if no fish left spawn one occasionally
		if len(self.fishes) < 5 and random.random() < 0.01:
			x = -30
			y = random.randint(230, 370)
			speed = random.choice([1, 2])
			self.fishes.append(Fish(self.canvas, x, y, speed, random.choice(['orange','yellow','red','green','purple'])))

		self.root.after(50, self.update)


def main():
	root = Tk()
	game = FishingGame(root)
	root.mainloop()


if __name__ == '__main__':
	main()
