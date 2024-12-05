import pygame
import math

pygame.init()
win = pygame.display.set_mode((720, 700))
pygame.font.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (250, 200, 0)
RED = (255, 0, 0)
PINK = (255, 0, 255)

FPS = 60

width = win.get_width()
height = win.get_height()

LIVES_FONT = pygame.font.SysFont("ArenaOutline", 40)
LOST_FONT = pygame.font.SysFont("Cartoonist", 60)

class Ball:
	VEL = 10
	def __init__(self, x, y, r, clr):
		self.x = x
		self.y = y
		self.r = r
		self.clr = clr
		
		self.vel_x = 0
		self.vel_y = -self.VEL
	
	def draw(self, win):
		pygame.draw.circle(win, self.clr, (self.x, self.y), self.r)
		
	def move(self):
		self.y += self.vel_y
		self.x += self.vel_x
	
	def reverseVel(self):
		self.vel_y = abs(self.vel_y)
		
	def bounceBar(self, bar):
		bar_centre = bar.x + (bar.len / 2)
		dst_to_centre = self.x - bar_centre
		percent = dst_to_centre  / (bar.len)
		
		angle = percent * 90
		rad_angle = math.radians(angle)
		
		self.vel_x = math.sin(rad_angle) * self.VEL
		self.vel_y = -math.cos(rad_angle) * self.VEL
				
								
	def bounceEdge(self, sc_w, sc_h):
		if self.x - self.r < 0 or self.x + self.r > sc_w:
			self.vel_x = -self.vel_x
			
		if self.y - self.r < 0:
			self.vel_y = -self.vel_y
		
	def isCollide(self, bar):
		if self.x > bar.x and self.x  < bar.x + bar.len:
			if abs((self.y + self.r) - bar.y) < 2:
				return True
	
	def isGoesDown(self, sc_h):
		if self.y - self.r > sc_h:
			self.vel_y = -self.vel_y
			return True
		
	
class Bar:
	def __init__(self, x, y, len, clr):
		self.x = x
		self.y = y
		self.len = len
		self.clr = clr
	
	def draw(self, win):
		pygame.draw.rect(win, self.clr, (self.x, self.y, self.len, 20))
		

class Brick:
	def __init__(self, x, y, width, height, clr):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.clr = clr
		
		self.health = 10
		
	def isCollide(self, ball):
		if ball.x  + ball.r> self.x and ball.x - ball.r < self.x + self.width:
			if ball.y + ball.r > self.y and ball.y - ball.r < self.y + self.height:
				return True
				
	def takeDamage(self, damage):
		self.health -= damage
	
	def changeClr(self, color):
		self.clr = color
	
	def draw(self, win):
		pygame.draw.rect(win, self.clr, (self.x , self.y, self.width, self.height))


def resetBallPos(ball, bar):
	ball.x = bar.x + (bar.len / 2)
	ball.y = bar.y - ball.r 

def move(ball, x, y):
	ball.x = x
	ball.y = y
	
	
def generateBrick(rows, cols, width):
	brick_lst = []
	gap = 10
	diff = (width / cols)
	y = 30
	for r in range(rows):
		for c in range(cols):
			x = diff * c
			new_brick = Brick(x, y, 65, 30,  RED)
			brick_lst.append(new_brick)
		y += new_brick.height + gap

	return brick_lst

	
def drawWin(win, ball, bar, bricks, lives):
	livesText = LIVES_FONT.render(f"LIVES: {lives}", True, BLACK)

	win.fill(WHITE)

	win.blit(livesText, (width - 120, height - 40))
	
	for brick in bricks:
		brick.draw(win)
		
	bar.draw(win)
	ball.draw(win)

	pygame.display.update()
		

def main():
	ball = Ball(200, 300, 10, BLUE)
	bar = Bar(400, height - 30, 150, YELLOW)

	resetBallPos(ball, bar)

	bricks = generateBrick(5, 10, width)

	lives = 3

	clock = pygame.time.Clock()

	stage_start = False

	run = True
	while run:  # Main Gameloop
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				pygame.quit()
			if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
				stage_start = True
			
		clock.tick(FPS)

		if not stage_start:
			x = bar.x + bar.len / 2
			y = ball.y
			move(ball, x, y)

		# move Bar according to mouse pos
		x, y = pygame.mouse.get_pos()
		bar.x = x - (bar.len / 2)

		ball.bounceEdge(width, height)
		# direction reversed on collision on bar
		if ball.isCollide(bar): 
			#ball.reverseVel()
			ball.bounceBar(bar)
	
		# reset ball position if ball goes out of screen
		if ball.isGoesDown(height):
			lives -= 1
			resetBallPos(ball, bar)

		# if nomore lives is remained then restart game
		if lives <= 0:
			run = False
		
		for brick in bricks:
			if brick.isCollide(ball):
				ball.reverseVel()
				brick.takeDamage(5)
				brick.changeClr(PINK)
				if brick.health <= 0:
					bricks.remove(brick)
			
		# generate brick again if nothing left
		if len(bricks) <= 0:
			resetBallPos(ball, bar)
			bricks = generateBrick(5, 10, width)
		
		if stage_start:
			ball.move()
		# move(ball, x, y)
		
		drawWin(win, ball, bar, bricks, lives)
		

def lostMenu(win):
	#TODO
	lostText = LOST_FONT.render("You Lost!\nPress any key to play again!", True, RED)
	lostTextRect = lostText.get_rect()
	lostTextRect.center = (width // 2, height // 2)

	clock = pygame.time.Clock()
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				print(event.type)
				main()

		clock.tick(FPS)

		win.blit(lostText, lostTextRect)
		pygame.display.update()



if __name__ == '__main__':
	main()
	lostMenu(win)
	