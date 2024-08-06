# Here, modules such as pygame, random and math are imported
# Pygame is also initiated below
import pygame
from pygame import *
init()
import random
import math
from math import * 
 
# Here, the basics of the game, such as the width and height of the screen are declared 
width = 1000
height = 600
border = 25
screen = display.set_mode((width, height))
gameWidth = 975
gameHeight = 575
pygame.display.set_caption("8 Ball Pool") 
font = pygame.font.SysFont("Arial", 34)

friction = 0.005

# This class creates the elements needed for the Pool Table
# The elements include the borders and the pockets               
class PoolTable():
	# The function below will create rectangles with given sizes 
	# The function will then draw the created borders on the game screen
	def drawBorders(self,screen):
		# Border 1 has been drawn on the screen with the given colour and co-ordinates, in the form of a rectangle
		draw.rect(screen, (150,75,0), (0,0,1000,25))
		# Border 2 has been drawn on the screen with the given colour and co-ordinates, in the form of a rectangle
		draw.rect(screen, (150,75,0), (0,0,25,1000))
		# Border 3 has been drawn on the screen with the given colour and co-ordinates, in the form of a rectangle
		draw.rect(screen, (150,75,0), (0,580,1000,25))
		# Border 4 has been drawn on the screen with the given colour and co-ordinates, in the form of a rectangle
		draw.rect(screen, (150,75,0), (980,0,25,1000))

	# This function is used to create holes on the pool table 
	# They are known as pockets and are drawn in the form of circles
	def drawPockets(self,screen):
		# Pocket 1 has been drawn on the screen with the given colour and co-ordinates, in the form of a cirlce
		draw.circle(screen, (0,0,0), (30,30), 30)
		# Pocket 2 has been drawn on the screen with the given colour and co-ordinates, in the form of a cirlce
		draw.circle(screen, (0,0,0), (485,30), 30)
		# Pocket 3 has been drawn on the screen with the given colour and co-ordinates, in the form of a cirlce
		draw.circle(screen, (0,0,0), (970,30), 30)
		# Pocket 4 has been drawn on the screen with the given colour and co-ordinates, in the form of a cirlce
		draw.circle(screen, (0,0,0), (30,570), 30)
		# Pocket 5 has been drawn on the screen with the given colour and co-ordinates, in the form of a cirlce
		draw.circle(screen, (0,0,0), (485,570), 30)
		# Pocket 6 has been drawn on the screen with the given colour and co-ordinates, in the form of a cirlce
		draw.circle(screen, (0,0,0), (970,570), 30)    
		
	def checkPockets(self, allBalls): 
		for b in allBalls:
			pocket1Distance = (((int(b.x) - int(30)) ** 2) + ((int(b.y) - int(30)) ** 2)) ** 0.5
			pocket2Distance = (((int(b.x) - int(485)) ** 2) + ((int(b.y) - int(30)) ** 2)) ** 0.5
			pocket3Distance = (((int(b.x) - int(970)) ** 2) + ((int(b.y) - int(30)) ** 2)) ** 0.5
			pocket4Distance = (((int(b.x) - int(30)) ** 2) + ((int(b.y) - int(570)) ** 2)) ** 0.5
			pocket5Distance = (((int(b.x) - int(485)) ** 2) + ((int(b.y) - int(570)) ** 2)) ** 0.5
			pocket6Distance = (((int(b.x) - int(970)) ** 2) + ((int(b.y) - int(570)) ** 2)) ** 0.5

			if pocket1Distance <= int(30 + b.size):
				allBalls.remove(b)
			elif pocket2Distance <= int(30 + b.size):
				allBalls.remove(b)
			elif pocket3Distance <= int(30 + b.size):
				allBalls.remove(b)
			elif pocket4Distance <= int(30 + b.size):
				allBalls.remove(b)
			elif pocket5Distance <= int(30 + b.size):
				allBalls.remove(b)
			elif pocket6Distance <= int(30 + b.size):
				allBalls.remove(b)

	# The following function is used to draw the group the borders and pockets 
    # They are both drawn in this function   
	def drawTable(self,screen):
		self.drawBorders(screen)
		self.drawPockets(screen)
		
# This class creates the Cue Stick that will be controlled by the player         
class CueStick():
	# This is the constructor for the Cue Stick, which takes the x and y co-ordinates 
	# As well as the length and colour
	def __init__(self, x, y, length, colour):
		self.x = x
		self.y = y 
		self.length = length
		self.colour = colour 
		self.tangent = 0
	
	# This method applies the force on the cue ball when the user changes the length of the cue stick
	def applyForce(self, cueBall, force):
		cueBall.angle = self.tangent 
		cueBall.speed = force
    
	# This method draws both the cue stick and the guidline for the cue stick 
	def drawCueStick(self, cueBallX, cueBallY):
		self.x, self.y = pygame.mouse.get_pos() 
		self.tangent = (degrees(atan2((cueBallY - self.y), (cueBallX - self.x))))
		draw.line(screen, (0,0,0), (cueBallX + (self.length * cos(radians(self.tangent))), cueBallY + self.length * sin(radians(self.tangent))) , (cueBallX, cueBallY), 1)
		draw.line(screen, self.colour, (self.x, self.y), (cueBallX, cueBallY), 3) 

# This class creates the interactive buttons that are used by the player
# The buttons aid the transtion from the welcome screen to the game mode selected by the player
class Button(Rect):
	# This function is responsbile for checking if any click events have taken place
	def checkClick(self,pos):
		if self.collidepoint(pos):
			result = self.callback()
			if result != None: 
				return result
 
	def setText(self, text):
		self.text = text
 
	def setCallback(self,callback):
		self.callback = callback
		
	# The following method creates elements for the welcome screen
	# The elements include the button colour and the text for the button
	def draw(self,screen):
		draw.rect(screen,(150,75,0), self)
		buttonText = font.render("1 Player Mode", True, (255,255,255))
		screen.blit(buttonText, (365,215))
		buttonText2 = font.render("2 Player Mode", True, (255,255,255))
		screen.blit(buttonText2,(365,340))
 
# This class is used to create the ball and also moves the ball across the game screen
# Pygame Sprite Class has been used to detect collisions in the pixel level         
class Ball(pygame.sprite.Sprite): 
	def __init__(self, x, y, colour, size, angle, speed, ballNum):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.colour = colour
		self.size = size
		self.ballNum = ballNum
		self.angle = angle
		self.speed = speed
		self.font = pygame.font.SysFont("Arial", 13)

        # Masks are used to store which parts collide
        # The following code creates the mask
        # SCRALPHA will make sure the pixel format includes a per pixel alpha
		self.maskSurface = pygame.Surface((size,size), pygame.SRCALPHA)
		# This line will ensure that the Ball is drawn on the created surface
		draw.circle(self.maskSurface, self.colour, (0,0), self.size)
        # The Mask created above is generated from the given surface
		self.mask = pygame.mask.from_surface(self.maskSurface)
		self.rect = Rect(x, y, size, size)

	# This function is used to create a ball with the dimensions given
	# This function also displays the mask created above	
	def drawBall(self,screen):
		draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.size))
		
		# This If statement allows the colour of the number on the balls to be changed
		# This increases the usability of the game
		if self.ballNum == 1 or self.ballNum == 9:
			ballNumber = self.font.render(str(self.ballNum), True, (0,0,0))
		else:
			ballNumber = self.font.render(str(self.ballNum), True, (255,255,255))

		# This If statement changes the size of the text used to display the ball number
		# This also increases the usability of the game
		if self.ballNum > 9:
			screen.blit(ballNumber, (self.x - 13, self.y - 5))
			screen.blit(self.maskSurface, self.rect)
		else:
			screen.blit(ballNumber, (self.x - 7, self.y - 5))
			screen.blit(self.maskSurface, self.rect)

	def moveBall(self):
		# A friction variable is set up at the start, which slowly reduces the speed of the ball
		self.speed -= friction
		if self.speed <= 0:
			self.speed = 0 

		# This updates the x and y co-ordinates when the balls move, using sin and cos
		self.x = self.x + self.speed * cos(radians(self.angle))
		self.y = self.y + self.speed * sin(radians(self.angle))

		# Here, there are conditions that will update the angle and alloes the balls to bounce back from the pool table
		if not (self.x < width - self.size - border):
			self.x = width - self.size - border 
			self.angle = 180 - self.angle 
		if not (self.size + border < self.x):
			self.x = self.size + border 
			self.angle = 180 - self.angle
		if not (self.y < height - self.size - border):
			self.y = height - self.size - border 
			self.angle = 360 - self.angle 
		if not (self.size + border < self.y):
			self.y = self.size + border 
			self.angle = 360 - self.angle
		
		self.rect.x = self.x 
		self.rect.y = self.y
			
	def ballCollisionDetection(self, allBalls, poolTable):
		self.rect.x = self.x
		self.rect.y = self.y

		# This line of code implements the Check Pocket Collision method that is within the PoolTable Class
		# The method requires a list of allBalls to be inputted into the method
		poolTable.checkPockets(allBalls)
		
        # The following checks for any collisions that take place
		currentRect = self.rect
		for b in allBalls:
			if b != self:
				bRect = b.rect
				# This section of code is responsible for checking when collisions take place
				offset = currentRect[0] - bRect[0], currentRect[1] - bRect[1]
				overlap = b.mask.overlap(self.mask, offset) 
				if overlap:
					return True

	# This code is to check colliisons that will be used for non masked balls, such as the cue ball
	def collision(self, ball1, ball2):
		distance = ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5
		if distance <= 40: 
			return True
		else:
			return False

	# Here, collisions are implemented, which makes use of the math module
	# This uses the initial velocity of both balls, then calculates the new angles and new speeds for both balls
	def checkCueCollisions(self, cueBall, allBalls, poolTable):
		for i in range(len(allBalls)):
			if self.collision(cueBall, allBalls[i]):
				if allBalls[i].x == cueBall.x:
					angleIncline = 2 * 90 
				else:
					initialVelocity1 = allBalls[i].speed 
					initialVelocity2 = cueBall.speed 

					allBalls[i].speed = ((initialVelocity1 * cos(radians(allBalls[i].angle))) ** 2 + (initialVelocity2 * sin(radians(cueBall.angle))) ** 2) ** 0.5
					cueBall.speed = ((initialVelocity2 * cos(radians(cueBall.angle))) ** 2 + (initialVelocity1 * sin(radians(allBalls[i].angle))) ** 2) ** 0.5

					tangent = degrees((atan((allBalls[i].y - cueBall.y) / (allBalls[i].x - cueBall.x)))) + 90
					angle = tangent + 90 

					allBalls[i].angle = (2 * tangent - allBalls[i].angle)
					cueBall.angle = (2 * tangent - cueBall.angle)

					allBalls[i].x += (allBalls[i].speed) * sin(radians(angle))
					allBalls[i].y -= (allBalls[i].speed) * cos(radians(angle))
					cueBall.x -= (cueBall.speed) * sin(radians(angle))
					cueBall.y += (cueBall.speed) * cos(radians(angle))
					
	# Here, collisions are implemented, which makes use of the math module
	# This uses the initial velocity of both balls, then calculates the new angles and new speeds for both balls
	def checkBallCollisions(self, allBalls, poolTable):		
		for i in range(len(allBalls)):
			for j in range(len(allBalls) - 1, i, -1):
				if self.collision(allBalls[i], allBalls[j]):
					if allBalls[i].x == allBalls[j].x:
						angleIncline = 2 * 90 
					else:
						initialVelocity1 = allBalls[i].speed 
						initialVelocity2 = allBalls[j].speed 

						allBalls[i].speed = ((initialVelocity1 * cos(radians(allBalls[i].angle))) ** 2 + (initialVelocity2 * sin(radians(allBalls[j].angle))) ** 2) ** 0.5
						allBalls[j].speed = ((initialVelocity2 * cos(radians(allBalls[j].angle))) ** 2 + (initialVelocity1 * sin(radians(allBalls[i].angle))) ** 2) ** 0.5

						tangent = degrees((atan((allBalls[i].y - allBalls[j].y) / (allBalls[i].x - allBalls[j].x)))) + 90
						angle = tangent + 90 

						allBalls[i].angle = (2 * tangent - allBalls[i].angle)
						allBalls[j].angle = (2 * tangent - allBalls[j].angle)

						allBalls[i].x += (allBalls[i].speed) * sin(radians(angle))
						allBalls[i].y -= (allBalls[i].speed) * cos(radians(angle))
						allBalls[j].x -= (allBalls[j].speed) * sin(radians(angle))
						allBalls[j].y += (allBalls[j].speed) * cos(radians(angle))

# This class is responsible for filling the screen with the chosen colour 
# The class also manages clicks
class AbstractScreen():
    def drawScreen(self,screen):
        screen.fill((0,128,0))
        self.poolTable.drawTable(screen)
        
    def manageClick(self,pos):
        return self
      
    def update(self):
        pass
 
# This Class is a Menu Class, which contains code for all screen related functions
# Such as Drawing the screen, the transtion from welcome screen to game screen and manages clicks. 
# This class takes in the Abstract Class created above
class MenuScreen(AbstractScreen):
	def __init__(self): 
		self.gameTitle = font.render("Welcome to 8 Ball Pool", True, (255,255,255))
		# The following code will create the buttons itself, with the given location
		myButton = Button(350,200,250,70)
		myButton2 = Button(350,325,250,70)
		# The code below will check if any user inputs have taken place
		# The click is linked to a Callback, changing the screen when clicked
		myButton.setCallback(self.onePlayerModeButton)
		myButton2.setCallback(self.twoPlayerModeButton)
		self.listOfButtons = [myButton, myButton2]
        # This is for the background of the menu screen
		self.poolTable = PoolTable()
    
	def drawScreen(self, screen):
		super().drawScreen(screen)
		screen.blit(self.gameTitle, (320,80))
		for b in self.listOfButtons:
			b.draw(screen)  
	
	# The following method is one of two Callbacks seen above
	# This Callback is for Single Player Mode, which alerts the user and transitions to the game screen
	def onePlayerModeButton(self):
		global currentState
		print("Selected Option: 1 Player Mode")
		print("Please Wait, One Player Mode is loading...")
		print("The Aim of the game is to pot all of the balls")
		return GameScreen(1)
		
	# This method is the final Callback, which alerts the user that they have selected the Two Player Mode
	# It then transitions to the Two Player Mode game screen
	def twoPlayerModeButton(self):
		global currentState
		print("Selected Option: 2 Player Mode")
		print("Please Wait, Two Player Mode is loading...")
		print("Player 1 Pots balls 1-7, Player 2 Pots balls 9-15, The player with no balls remaining pots the 8 Ball")
		return GameScreen(2)
    
	def manageClick(self,pos):
		for b in self.listOfButtons:
			result = b.checkClick(pos)
			print(result)
			if result != None: 
				return result
		return self
 
# This class contains all the game logic and draws the game screen
# This class also updates the movement of the balls 
class GameScreen(AbstractScreen):
	def __init__(self, playerMode):
		self.poolTable = PoolTable()
		# An List is created, where all of the Pool Balls are appended to
		self.poolBalls = []
		self.cueBalls = []

		# The following Variables are responsible for creating the Cue Ball
		cueBallX = 300
		cueBallY = 300
		cueBallColour = (255,255,255)
        # The following line creates the Ball from the Ball Class seen above
        # It takes in the co-ordinates of the ball, the colour and the size of the ball
		cueBall = Ball(cueBallX, cueBallY, cueBallColour, 20, 0, 0, 0)

        # The following Variables are responsible for creating the rest of the pool balls
		yellowBall1X = 700
		yellowBall1Y = 300
		yellowBall1Colour = (255,255,0)
        # The following line creates the Ball from the Ball Class seen above
        # It takes in the co-ordinates of the ball, the colour and the size of the ball
		yellowBall1 = Ball(yellowBall1X, yellowBall1Y, yellowBall1Colour, 20, 0, 0, 1)
        
		# Here, a Yellow Ball has been created
		yellowBall2X = 735
		yellowBall2Y = 320
		yellowBall2Colour = (255,255,0)
		yellowBall2 = Ball(yellowBall2X, yellowBall2Y, yellowBall2Colour, 20, 0, 0, 9)

		# Here, a Blue Ball has been created
		blueBall1X = 735
		blueBall1Y = 280
		blueBall1Colour = (0,0,255)
		blueBall1 = Ball(blueBall1X, blueBall1Y, blueBall1Colour, 20, 0, 0, 2)

		# Here, a Blue Ball has been created
		blueBall2X = 770
		blueBall2Y = 340
		blueBall2Colour = (0,0,255)
		blueBall2 = Ball(blueBall2X, blueBall2Y, blueBall2Colour, 20, 0, 0, 10)

		# Here, The Black ball, also known as the 8 Ball has been created
		eightBallX = 770
		eightBallY = 300
		eightBallColour = (0,0,0)
		eightBall = Ball(eightBallX, eightBallY, eightBallColour, 20, 0, 0, 8)

		# Here, a Red ball has been created
		redBall1X = 770
		redBall1Y = 260
		redBall1Colour = (255,0,0)
		redBall1 = Ball(redBall1X, redBall1Y, redBall1Colour, 20, 0, 0, 3)

		# Here, a Orange ball has been created
		orangeBall1X = 805
		orangeBall1Y = 240
		orangeBall1Colour = (255,140,0)
		orangeBall1 = Ball(orangeBall1X, orangeBall1Y, orangeBall1Colour, 20, 0, 0, 13)

		# Here, a Green ball has been created
		greenBall1X = 805
		greenBall1Y = 280
		greenBall1Colour = (0,255,0)
		greenBall1 = Ball(greenBall1X, greenBall1Y, greenBall1Colour, 20, 0, 0, 6)

		# Here, a Purple ball has been created
		purpleBall1X = 805
		purpleBall1Y = 320
		purpleBall1Colour = (128,0,128)
		purpleBall1 = Ball(purpleBall1X, purpleBall1Y, purpleBall1Colour, 20, 0, 0, 12)

		# Here, a Purple ball has been created
		purpleBall2X = 805
		purpleBall2Y = 360
		purpleBall2Colour = (128,0,128)
		purpleBall2 = Ball(purpleBall2X, purpleBall2Y, purpleBall2Colour, 20, 0, 0, 4)

		# Here, a Red ball has been created
		redBall2X = 840
		redBall2Y = 220
		redBall2Colour = (255,0,0)
		redBall2 = Ball(redBall2X, redBall2Y, redBall2Colour, 20, 0, 0, 11)

		# Here, a Burgundy ball has been created
		burgundyBall1X = 840
		burgundyBall1Y = 260
		burgundyBall1Colour = (80,0,20)
		burgundyBall1 = Ball(burgundyBall1X, burgundyBall1Y, burgundyBall1Colour, 20, 0, 0, 7)
		
		# Here, a Burgundy ball has been created
		burgundyBall2X = 840
		burgundyBall2Y = 300
		burgundyBall2Colour = (80,0,20)
		burgundyBall2 = Ball(burgundyBall2X, burgundyBall2Y, burgundyBall2Colour, 20, 0, 0, 15)

		# Here, a Green ball has been created
		greenBall2X = 840
		greenBall2Y = 340
		greenBall2Colour = (0,255,0)
		greenBall2 = Ball(greenBall2X, greenBall2Y, greenBall2Colour, 20, 0, 0, 14)

		# Here, a Orange ball has been created
		orangeBall2X = 840
		orangeBall2Y = 380
		orangeBall2Colour = (255,140,0)
		orangeBall2 = Ball(orangeBall2X, orangeBall2Y, orangeBall2Colour, 20, 0, 0, 5)

		# Here, all of the Balls that have been created are appended to the List created above.
		# There is a seperate list for Cue Balls and Pool Balls
		self.cueBalls.append(cueBall)
		self.poolBalls.append(yellowBall1)
		self.poolBalls.append(yellowBall2)
		self.poolBalls.append(blueBall1)
		self.poolBalls.append(blueBall2)
		self.poolBalls.append(eightBall)
		self.poolBalls.append(redBall1)
		self.poolBalls.append(orangeBall1)
		self.poolBalls.append(greenBall1)
		self.poolBalls.append(purpleBall1)
		self.poolBalls.append(purpleBall2)
		self.poolBalls.append(redBall2)
		self.poolBalls.append(burgundyBall1)
		self.poolBalls.append(burgundyBall2)
		self.poolBalls.append(greenBall2)
		self.poolBalls.append(orangeBall2)
		
		self.cueStick = CueStick(0, 0, 100, (150,75,0))

	# Here, all the elements of the screen are drawn 
	# super() overrides the drawScreen method from AbstractScreen
	def drawScreen(self,screen):
		super().drawScreen(screen)
		for b in self.poolBalls:
			b.drawBall(screen)

		for b in self.cueBalls:
			b.drawBall(screen)
	
		# This is to only draw the cue stick when the ball is stationary
		if self.cueBalls[0].speed == 0:
			self.cueStick.drawCueStick(self.cueBalls[0].x, self.cueBalls[0].y)
	
	def manageClick(self, pos):
		start = [self.cueBalls[0].x, self.cueBalls[0].y]
		x, y = pygame.mouse.get_pos()
		end = [x, y]
		cueStickDistance = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
		cueStickForce = cueStickDistance / 10 

		if cueStickForce > 25:
			cueStickForce = 25

		self.cueStick.applyForce(self.cueBalls[0], cueStickForce) 

		return self

	# Here, the movement for the balls are implemented
	def update(self):
		for b in self.poolBalls:
			b.moveBall()
			b.checkBallCollisions(self.poolBalls, self.poolTable)
			b.ballCollisionDetection(self.poolBalls, self.poolTable)
			
		for c in self.cueBalls:
			c.moveBall()
			c.checkCueCollisions(self.cueBalls[0], self.poolBalls, self.poolTable)

currentScreen = MenuScreen()

start = 0 
end = 0

# Game Loop
running = True

while running == True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False 

        # This is the built in Pygame Mouse Detection event            
		elif event.type == pygame.MOUSEBUTTONDOWN:
			currentScreen = currentScreen.manageClick(pygame.mouse.get_pos())
	
	currentScreen.drawScreen(screen) 
	currentScreen.update()

	display.flip()
