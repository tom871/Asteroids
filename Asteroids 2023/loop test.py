import random
from graphics import *
import math




class Center(object):
    '''This parent class creates a cartesian point that is used for the Asteroid, Ufo, and Rocket child class. An X and
    Y integer value is stored as a private attribute which are then appended to a list for processing. Keyboard inputs
    change the heading and acceleration of the Rocket by modifying the theta value of the Polar coordinate and
    calculating a new cartesian coordinate to draw the Rocket at. '''

    def __init__(self, x1: int, y1: int):
        self.__centerX = x1  # X value of center point
        self.__centerY = y1  # Y value of center point
        self.__newlistCenter = [0, 0]  # List of zero values for storing X, Y values

        self.__listCenter = []  # Empty list to append X and Y values to elements for future processing
        self.__listCenter.append(x1)  # Append X to the first element of the list
        self.__listCenter.append(y1)  # Append Y to the second element of the list
        self.__listCenter.append(90)  # Append the degree heading to the 3rd element of the list

        self.__point = Point(self.__listCenter[0], self.__listCenter[1])  # Create the point


    def newCenter(self):
        '''Calculates a center point to store the coordinates of the new position to move to. The X and Y values are
        calculated using X = radius * Cos(Θ). Y = radius + Sin(Θ). Self calls are made to getTheta function passing the
        3rd element of the listCenter(which is the heading in degrees) to obtain theta in radians. The X,Y values are
        stored in the first and second elements respectively. Sin is negative because graphWin is inverted/ positive
        in the down direction. The newCenter list is returned.'''

        self.__newlistCenter[0] = 1.0 * math.cos(self.getTheta(self.__listCenter[2]))
        self.__newlistCenter[1] = 1.0 * -math.sin(self.getTheta(self.__listCenter[2]))

        return self.__newlistCenter

    def getTheta(self, degrees):
        '''Modulus division of the degree to be within 360 degrees for easy calculation of theta and clean rotation of
        the rocket ship.Returns the radian value of degrees'''

        remainder = degrees % 360

        return remainder * math.pi / 180


    def rotateCenter(self, direction):
        '''Add the value of direction to the 3rd element of listCenter to modify the heading of the point(used for the
         rocket ship rotation)'''

        self.__listCenter[2] = self.__listCenter[2] + direction

    def moveCenter(self, win: GraphWin):
        '''Move the point around the GraphWin. If the destination point moves the point off the screen the X or Y value
        needs to be modified by the width of the GraphWin to give the appearance of a donut universe where the object
        can transition seamlessly top to bottom or left to right. A list is created and populated with the new X,Y point
        to move to. '''

        center = self.newCenter()

        dx = center[0]
        dy = center[1]

        if self.__listCenter[0] + dx > win.getWidth():  # If destination X value is grater than the window
            center[0] -= win.getWidth()  # Subtract the window width value to "warp" object across screen

        elif self.__listCenter[0] + dx < 0:  # If destination X value is less than the window
            center[0] += win.getWidth()  # Add the window width value to "warp" object across screen

        if self.__listCenter[1] + dy > win.getWidth():  # If destination Y value is grater than the window
            center[1] -= win.getWidth()  # Subtract the window width value to "warp" object across screen

        elif self.__listCenter[1] + dy < 0:  # If destination Y value is less than the window
            center[1] += win.getWidth()  # Add the window width value to "warp" object across screen

        self.updateCenter(center)  # Updates the coordinates of the Point
        self.__point.move(center[0], center[1])  # Moves the Point to the new point(x,y)


    def coast(self, win):
        '''Coasting feature moves the point(The Rocket ship) a few move pixels on the screen to give the appearence of
        inertia. While the 'Up' key has been pressed and then depressed this function is called to move the ship each
        time by a radius of 1 when using the Polar cartesian conversion formulas. '''
        center = self.__newlistCenter

        center[0] = 1.0 * math.cos(self.getTheta(self.__listCenter[2]))
        center[1] = 1.0 * -math.sin(self.getTheta(self.__listCenter[2]))

        dx = center[0]
        dy = center[1]


        if self.__listCenter[0] + dx > win.getWidth():  # If destination X value is grater than the window
            center[0] -= win.getWidth()  # Subtract the window width value to "warp" object across screen

        elif self.__listCenter[0] + dx < 0:  # If destination X value is less than the window
            center[0] += win.getWidth()  # Add the window width value to "warp" object across screen

        if self.__listCenter[1] + dy > win.getWidth():  # If destination Y value is grater than the window
            center[1] -= win.getWidth()  # Subtract the window width value to "warp" object across screen

        elif self.__listCenter[1] + dy < 0:  # If destination Y value is less than the window
            center[1] += win.getWidth()  # Add the window width value to "warp" object across screen

        self.updateCenter(center)  # Updates the coordinates of the Point
        self.__point.move(center[0], center[1])  # Moves the Point to the new point(x,y)



    def updateCenter(self, center):
        '''Updates the X,Y of the listCenter for the Point'''

        self.__listCenter[0] += center[0]
        self.__listCenter[1] += center[1]


    def getList(self):
        return self.__listCenter  # Returns the list of the Point containing X,Y and theta

    def getHeading(self):
        heading = self.__listCenter[2]
        return self.getTheta(heading)  # Returns the heading of the point in radians

    def getX(self):
        return self.__listCenter[0]  # Returns the X coordinate of the Point

    def getY(self):
        return self.__listCenter[1]  # Returns the Y coordinate of the Point

    def setX(self, x):
        self.__listCenter[0] += x  # Sets element 0 to the value of x

    def setY(self, y):
        self.__listCenter[1] += y  # Sets element 1 to the value of y

    def getPoint(self):
        return Point(self.__listCenter[0], self.__listCenter[1])  # Returns the Point(X,Y) of Center



class Asteroid(Center):
    '''A child class of Center. Asteroids are circles with a variable radius and random starting location variables
    which are tracked by the parent class Center. Asteroids can warp around the screen by either adding or subtracting
    the width of the window to the X or Y coordinate. This creates the impression of a donut shaped universe.'''

    def __init__(self, x, y):
        super().__init__(x, y)

        self.__radius = random.randrange(12, 25)  # Random number generated to create differing sized asteroids

        self.__dx = random.randrange(-1, 1, 1)  # Random X value for the rate of change/speed of asteroid
        self.__dy = random.randrange(-1, 1, 1)  # Random Y value for the rate of change/speed of asteroid

        self.__asteroid = Circle(Point(self.getX(), self.getY()), self.__radius)  # Circle object of the asteroid


    def drawAsteroid(self, win: GraphWin):
        self.__asteroid.setFill("grey")  # Color the asteroid grey
        self.__asteroid.draw(win)  # Draw the asteroid to the window


    def moveAsteroid(self, win: GraphWin):
        ''' Moves the Asteroid on the window. If the Asteroid floats off screen the If statements modify the X or Y
        coordinate by the width of the window to reposition the asteroid on the screen. Once the self.__dX/Y attribute
        has been modified the list holding the Center coordinates is updated using the setX/Y setters and the move()
        function is called to move the asteroid object.'''

        if self.getX() + self.__dx > win.getWidth():
            self.__dx -= win.getWidth()

        elif self.getX() + self.__dx < 0:
            self.__dx += win.getWidth()

        if self.getY() + self.__dy > win.getWidth():
            self.__dy -= win.getWidth()

        elif self.getY() + self.__dy < 0:
            self.__dy += win.getWidth()


        self.setX(self.__dx)
        self.setY(self.__dy)

        self.__asteroid.move(self.__dx, self.__dy)


    def collision(self, originPoint):
        '''Determines if a collisiono with the Rocket has taken place, if so then True is returned. Otherwise False is
        returned.'''

        if Circle.testCollision_CircleVsPoint(self.__asteroid, originPoint):
            return True

        return False


    def getLocation(self):
        '''Returns the coordinate of the object in point form Point(X,Y)'''
        point = Point(self.getX(), self.getY())
        return point

    def isHit(self, missileList: list):
        '''Determines if the object has been struck by a missile. A while loop is used to iterate over the list of
        missiles passed through. If a collision between circles is true then the asteroid and missile are undrawn and
        the missile removed from the list. The asteroid is removed from the list in the If statement calling this
        definition. '''
        listIndex = 0

        while listIndex < len(missileList):
            if Circle.testCollision_CircleVsCircle(self.__asteroid, missileList[listIndex].getSelf()):
                self.__asteroid.undraw()
                missileList[listIndex].getSelf().undraw()
                missileList.pop(listIndex)

                return True
            listIndex += 1
            return False

    def remove(self):
        self.__asteroid.undraw()



class Rocket(Center):
    '''Creates the Rocket that is used by the player to fly around the universe and shoot missiles. Rocket is a child
    class of Center. The X and Y coordinates are passed to the parent super while theta(the direction it's pointing) is
    assigned as a private variable. From the X and Y values, which is the center of the triangle, the 3 points are
    calculated. The nose and corner points are calculated using Polar math. Since the GraphWin is flipped the theta
    needs to be negative(-) to account for this discrepancy. '''

    def __init__(self, x, y, theta):
        super().__init__(x, y)
        self.__theta = theta  # Assign theta to a private variable

        self.__P1 = self.nosePoint()  # Call the nosePoint method and assign its return value to P1
        self.__P2, self.__P3 = self.cornerPoint()  # Call the cornerPoint method and assign its return values to P2, P3

        self.__ship = Polygon(self.__P1, self.__P2, self.__P3)  # Create a triangle using points P1, P2, P3


    def nosePoint(self):
        ''' X = radius * Cos(Θ). Y = radius + Sin(Θ). Radius is fixed at 16 for the nose of the rocket ship. 16 was
        dervived by drawing a mockup on graph paper. Theta is negative to account for the GraphWin being inverted. '''
        x = 16 * math.cos(-self.__theta)
        y = 16 * math.sin(-self.__theta)

        return Point((self.getX() + x), (self.getY() + y))


    def cornerPoint(self):
        ''' X = radius * Cos(Θ). Y = radius + Sin(Θ). Radius is fixed at (725)^1/2 for the corners of the rocket ship.
        The theta calcuation is an offset to either add or subtract to the private theta attribute so two points can be
        calculated across the mirror/heading of the rocket ship. Theta is negative to account for the GraphWin being
        inverted. '''

        theta = math.atan(2.5) + math.pi / 2

        x = math.sqrt(725) * math.cos(-self.__theta - theta)
        y = math.sqrt(725) * math.sin(-self.__theta - theta)

        x2 = math.sqrt(725) * math.cos(-self.__theta + theta)
        y2 = math.sqrt(725) * math.sin(-self.__theta + theta)

        return Point((self.getX() + x), (self.getY() + y)), Point((self.getX() + x2), (self.getY() + y2))


    def drawShip(self, win: GraphWin):
        self.__ship.setFill(color_rgb(255, 255, 255))  # Color the ship white
        self.__ship.draw(win)  # Draw the ship to the window


    def undraw(self):
        self.__ship.undraw()  # Undraws the ship from the window


    def angle(self):
        return -self.__theta  # Return the direction of the ship heading


class Missile(object):
    '''Missile class draws a small circle with a fixed radius to simulate the firing of a missile. The X and Y center
    point of the circle are the Nose point values of the rocket ship. Getters are used to access the parent class Center
    which returns a Point(X, Y). Getters for the X and Y values are used to assign their respective values to private
    attributes of the missile. A distance variable is created to track how far the missile has traveled so it can be
    deleted if it doesnt hit anything. dX and dY variables are also created so the missiles can be moved across the
    window once they are drawn. '''

    def __init__(self, rocket: Rocket):
        self.__xy = rocket.getPoint()  # Assign the Point(X,Y) to private attribute. Also used for separate calculation
        self.__x = self.__xy.getX()  # Assign the X value of the Point(X, Y) to the attribute
        self.__y = self.__xy.getY()  # Assign the Y value of the Point(X, Y) to the attribute
        self.__size = 5  # Radius of the circle is small to simulate missile/bomb
        self.__disTravel = 0  # Distance tracker to prevent inaccurate missiles from flying forever

        self.__dx = 0  # X value of movement
        self.__dy = 0  # Y value of movement
        self.calcAngle(rocket)  # Call to self method to calculate the angle of the rocket and thus the X,Y values

        self.___missile = Circle(self.__xy, self.__size)  # Circle is the missile


    def calcDistance(self):
        '''Calculates the distance the missile has traveled. A missile is deleted after a determined distance to prevent
        errant missiles from flying forever and preventing the player from being unable to shoot. self.__xy is used to
        keep track of the initial x,y values of the missile to calculate the distance traveled. This isnt a perfect
        solution to the problem. '''

        x1 = self.__xy.getX()
        y1 = self.__xy.getY()
        self.__disTravel += math.sqrt((x1 - self.__x)**2 + (y1 - self.__y)**2)
        return self.__disTravel


    def calcAngle(self, rocket: Rocket):
        '''Calculates the X and Y values of dY/dX so the missile can move along the same direction the Rocket ship is
        pointing. '''
        theta = rocket.angle()
        self.__dx = math.cos(theta)
        self.__dy = math.sin(theta)


    def drawMissile(self, win: GraphWin):
        self.___missile.setFill("orange")  # Set the color of the missiles
        self.___missile.draw(win)  # Draw the missile to the window


    def moveMissile(self, win: GraphWin):
        '''Moves the missile on the window. If the missile moves off screen the If statements modify the X or Y
        coordinate by the width of the window to reposition the asteroid on the screen. Once the self.__dX/Y attribute
        has been modified they are summed to the X and Y attributes of the missile and the move() function is called
        to move the missile.'''

        if self.__x + self.__dx > win.getWidth():
            self.__dx -= win.getWidth()

        elif self.__x + self.__dx < 0:
            self.__dx += win.getWidth()

        if self.__y + self.__dy > win.getWidth():
            self.__dy -= win.getWidth()

        elif self.__y + self.__dy < 0:
            self.__dy += win.getWidth()

        self.__x += self.__dx
        self.__y += self.__dy

        self.___missile.move(self.__dx, self.__dy)


    def undrawMissile(self):
        self.___missile.undraw()  # Undraws the missile from the screen


    def getSelf(self):

        return self.___missile  # Return the object


class Ufo(Center):
    '''Creates a UFO in the shape of an ellipse. The starting position of the UFO is random and passed through to the
    parent class Center. The center point of the oval is tracked to calculate collision with other objects by creating
    a hitbox-cricle. The vertices of the ellipse are calculated by using the initial X,Y values and adding values to
    them.'''

    def __init__(self, x, y):
        super().__init__(x, y)

        # Random slope values for UFO movement
        self.__dx = random.randrange(-1, 3, 2)
        self.__dy = random.randrange(-1, 5, 2)

        self.__ufo = Oval(Point(self.getX(), self.getY()), Point(self.getX() + 20, self.getY() + 10))  # UFO

    def drawUfo(self, win: GraphWin):
        self.__ufo.setFill("green")  # color the ufo green
        self.__ufo.draw(win)  # draw the ufo to the window

    def hitBox(self):
        '''Calculate the midpoint of the ellipse to create a hitbox-cricle for collision detection.'''
        midX = (2 * self.getX() + 20) / 2
        midY = (2 * self.getY() + 10) / 2

        return Circle(Point(midX, midY), 5)


    def moveUfo(self, win: GraphWin):
        '''Moves the UFO on the window. If the UFO floats off screen the If statements modify the X or Y
        coordinate by the width of the window to reposition the UFO on the screen. Once the self.__dX/Y attribute
        has been modified the list holding the Center coordinates is updated using the setX/Y setters and the move()
        function is called to move the UFO object.'''

        if self.getX() + self.__dx > win.getWidth():
            self.__dx -= win.getWidth()

        elif self.getX() + self.__dx < 0:
            self.__dx += win.getWidth()

        if self.getY() + self.__dy > win.getWidth():
            self.__dy -= win.getWidth()

        elif self.getY() + self.__dy < 0:
            self.__dy += win.getWidth()

        self.setX(self.__dx)
        self.setY(self.__dy)

        self.__ufo.move(self.__dx, self.__dy)


    def isHit(self, missileList: list):
        '''Collision detection for the UFO and missiles. A while loop is used to iterate through the missile list passed
        to this function. If a collision is detected the UFO and missile are undrawn and the missile is removed from the
        list. An index value is initialized to 0 and incremented each iteration of the while loop by the return false
        boolean logic'''
        listIndex = 0

        while listIndex < len(missileList):
            if Circle.testCollision_CircleVsCircle(self.hitBox(), missileList[listIndex].getSelf()):
                self.__ufo.undraw()
                missileList[listIndex].getSelf().undraw()
                missileList.pop(listIndex)

                return True
            listIndex += 1
            return False


    def collision(self, originPoint):
        '''Collision detection for the UFO and Rocket. If a collision is detected boolean logic True is returned to the
        calling function. If no collision is detected False is returned.'''

        if Circle.testCollision_CircleVsPoint(self.hitBox(), originPoint):
            return True

        return False

    def removeUFO(self):
        self.__ufo.undraw()



class Score(object):
    '''Displays a scoreboard in the topleft of the screen. The number of asteroids that have been destroyed along with
    the number of missiles fired by the player is tracked via a private data attribute and is updated with each
    iteration of the game's while loop. The board is drawn before the loop starts and is updated with a call to
    updateBoard() at the end of each while loop. A third private attribute sets the text color of the UFO notification
    from black to yellow, displaying the message once the UFO has been destroyed.'''

    def __init__(self):
        self.__asteroidCount = 0  # Initialize the count to zero
        self.__missilesFired = 0  # Initialize the count to zero

        self.__ufoText = "Red"  # Initialize the color of the text for ufo to black(hidden on screen)

        # Create text objects for the score board
        self.__asteroidBoard = Text(Point(150, 30), f"Asteroids Destroyed: {self.__asteroidCount}")
        self.__missileBoard = Text(Point(120,60), f"Missiles Fired: {self.__missilesFired}")
        self.__ufoBoard = Text(Point(120, 90), "UFO Destroyed!")
        self.__ufoBoardDrawn = False


    def drawBoard(self, win):
        '''Draw the three text objects to the screen with their stylized attributes'''
        self.__asteroidBoard.setTextColor("White")
        self.__asteroidBoard.setStyle("bold")
        self.__asteroidBoard.setSize(18)
        self.__asteroidBoard.draw(win)

        self.__missileBoard.setTextColor("White")
        self.__missileBoard.setStyle("bold")
        self.__missileBoard.setSize(18)
        self.__missileBoard.draw(win)

        self.__ufoBoard.setTextColor(self.__ufoText)
        self.__ufoBoard.setStyle("bold")
        self.__ufoBoard.setSize(22)


    def updateBoard(self):
        '''Eech time this function is called it will update the text of the scoreboard to their current values'''
        self.__asteroidBoard.setText(f"Asteroids Destroyed: {self.__asteroidCount}")
        self.__missileBoard.setText(f"Missiles Fired: {self.__missilesFired}")
        self.__ufoBoard.setTextColor(self.__ufoText)

    def setMissile(self, shot):
        self.__missilesFired += shot  # Increment the number of shots fired by the value of 'shot', which is 1

    def setAsteroid(self, asteroid):
        self.__asteroidCount += asteroid  # Increment the number of asteroids by the value of 'asteroid', which is 1

    def setUFO(self, win):
        self.__ufoBoardDrawn = True
        self.__ufoBoard.draw(win)  # Draws the message to the window once the ufo is destroyed

    def removeUfo(self):
        self.__ufoBoard.undraw()

    def setScore(self):
        self.__asteroidCount = 0
        self.__missilesFired = 0

    def getScore(self):
        return self.__asteroidCount, self.__missilesFired

    def getUfoDrawn(self):
        return self.__ufoBoardDrawn




class Message(object):
    '''Displays a victory or game over message to the player when called. The class creates all of the text objects to
    display with their attributes but only returns the called message as needed. '''


    title = Text(Point(450, 450), "Asteroids!!!\nPress 'Up' to play\nOr 'Down' to exit")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("White")

    lose = Text(Point(450, 450), "GAME OVER!")
    lose.setSize(36)
    lose.setStyle("bold")
    lose.setTextColor("Red")

    winMessage = Text(Point(450, 450), "YOU WIN THE\nEMPTINESS OF SPACE!")
    winMessage.setSize(36)
    winMessage.setStyle("bold")
    winMessage.setTextColor("BLUE")

    winStatus = False
    loseStatus = False




    def __init__(self):
        self.__title = Text(Point(300, 300), "Asteroids!!!\nPress 'Up' to play\nOr 'Down' to exit")
        self.__title.setSize(36)
        self.__title.setStyle("bold")
        self.__title.setTextColor("White")

        self.__lose = Text(Point(300, 300), "GAME OVER!")
        self.__lose.setSize(36)
        self.__lose.setStyle("bold")
        self.__lose.setTextColor("Red")

        self.__winMessage = Text(Point(300, 300), "YOU WIN THE\nEMPTINESS OF SPACE!")
        self.__winMessage.setSize(36)
        self.__winMessage.setStyle("bold")
        self.__winMessage.setTextColor("BLUE")




    def getVictory(self):
        return self.__winMessage  # Returns the victory message text object

    def getLose(self):
        return self.__lose  # Returns the game over message text object

    def Victory(self, win: GraphWin):
        self.__winMessage.draw(win)  # Draws the object to the window

    def gameOver(self, win: GraphWin):
        self.__lose.draw(win)  # Draws the object to the window

    def title(self):
        return self.__title










def main():
    win = GraphWin("Asteroids", 900, 900, autoflush = False)
    win.setBackground("black")

    exit = False
    play = True
    drawTitle = False
    drawScore = True

    title = Text(Point(450, 450), "Asteroids!!!\nPress 'Enter' to play\nOr 'Escape' to exit")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("White")

    message = Text(Point(450, 450), "Test Message")
    message.setSize(36)
    message.setStyle("bold")
    message.setTextColor("White")

    exitMsg = Text(Point(450, 450), "Mouse click to exit")
    exitMsg.setSize(36)
    exitMsg.setStyle("bold")
    exitMsg.setTextColor("White")

    keyboard = win.checkKeys()

    asteroidList = []  # Empty list for processing asteroids
    missileList = []  # Empty list for processing missiles
    ufoList = []  # Empty list for processing the UFO

    scoreBoard = Score()




    while exit == False:
        print(keyboard)


        if len(asteroidList) == 0:
            for i in range(random.randint(5,15)):  # random.randint(50,100)
                asteroidList.append((Asteroid(random.randrange(50, 850), random.randrange(50, 850))))
                asteroidList[i].drawAsteroid(win)  # Draws the asteroid to the window

        for asteroid in asteroidList:
            asteroid.moveAsteroid(win)  # Move the asteroid if no collision detected

        if drawTitle == False and Message.winStatus == False and Message.loseStatus == False:
            title.draw(win)
            drawTitle = True
        print(f"List length {len(asteroidList)}")
        print(asteroidList)
        time.sleep(.001)




        if 'Return' in keyboard or 'KP_Enter' in keyboard:

            while len(asteroidList) != 0:
                asteroidList[-1].remove()
                asteroidList.pop(-1)

            while len(missileList) != 0:
                missileList[-1].undrawMissile()
                missileList.pop(-1)

            while len(ufoList) != 0:
                ufoList[-1].removeUFO()
                ufoList.pop(-1)


            if drawScore == True:
                scoreBoard.drawBoard(win)
                drawScore = False

            else:
                scoreBoard.setScore()
                scoreBoard.updateBoard()
                Message.lose.undraw()
                Message.winMessage.undraw()

            if scoreBoard.getUfoDrawn() == True:
                scoreBoard.removeUfo()






            title.undraw()
            drawTitle = False

            coast = False  # Coast value initialized to zero to prevent unlimited coasting all the time
            play = True  # play initialized to true to start while loop


            exciter = Message()  # Create the object containing exciter messages



            ufoAlive = True  # Ufo is set to true until its removed from the game for displaying message

            ufoList.append(Ufo(random.randrange(0, 900, 15), random.randrange(0, 900, 15)))  # Append a UFO to the ufo list

            origin = Center(300, 300)  # Create a point to move the rocket on screen
            rocket = Rocket(300, 300, math.pi / 2)  # (x,y) starting point and pi/2 (90 degrees) starting direction
            rocket.drawShip(win)  # Draw rocket to the window

            # For loop to append an instance of the Asteroid class to the asteroid list with random attributes
            for i in range(5):
                asteroidList.append((Asteroid(random.randrange(50, 850), random.randrange(50, 850))))
                asteroidList[i].drawAsteroid(win)  # Draws the asteroid to the window

            for ufo in ufoList:
                ufo.drawUfo(win)  # Draws the ufo to the window


            # Game loop breaks when the player dies or wins the game
            while play == True:
                keyboard = win.checkKeys()  # is a SET of strings of the keyboard inputs

                print(keyboard)  # displays the inputs of the SET keyboard to console
                print(origin.getList())  # Displays (X,Y,Θ) of the origin(the center of the rocket ship) to console
                print(len(ufoList))  # prints the len of the ufo list to console
                print(f"Asteroid list:{asteroidList}")
                print(f"Missile List: {missileList}")

                # Control input from the player to rotate rocket ship counter-clockwise
                if 'Left' in keyboard:
                    degree = .5  # Initialize the value of degree to half a degree for each input
                    origin.rotateCenter(degree)  # Pass degree to the origin to rotate the center point of the rocket ship
                    rocket.undraw()  # Undraw the current rocket ship
                    rocket = Rocket(origin.getX(), origin.getY(),origin.getHeading())  # Make a new ship with new heading
                    rocket.drawShip(win)  # Draw new rocket to window in the new direction

                # Control input from the player to rotate rocket ship clockwise
                if 'Right' in keyboard:
                    degree = -.5  # Initialize the value of degree to half a degree for each input
                    origin.rotateCenter(degree)  # Pass degree to the origin to rotate the center point of the rocket ship
                    rocket.undraw()  # Undraw the current rocket ship
                    rocket = Rocket(origin.getX(), origin.getY(),origin.getHeading())  # Make a new ship with new heading
                    rocket.drawShip(win)  # Draw new rocket to window in the new direction

                # Control input to move the rocket ship forward in the direction its pointing
                if 'Up' in keyboard:
                    origin.moveCenter(win)  # Call the move function of the origin to calculate and move to the new (x,y)
                    rocket.undraw()  # Undraw the current rocket ship
                    rocket = Rocket(origin.getX(), origin.getY(),origin.getHeading())  # Make a new ship with new heading
                    rocket.drawShip(win)  # Draw new rocket to window in the new direction
                    coast = True  # Change the value of coast from False to True to enable coasting after up input

                # Selection statement determines if the rocket ship to coast if coast is true and 'UP' not in the keyboard Set
                if coast == True and 'Up' not in keyboard:
                    # A for loop iterates to move the rocket ship one radius value for each iteration to simulate movement
                    for i in range(13):
                        origin.coast(win)  # Move the origin point
                        rocket.undraw()  # Undraw the current rocket ship
                        rocket = Rocket(origin.getX(), origin.getY(),origin.getHeading())  # Make a new ship with new heading
                        rocket.drawShip(win)  # Draw new rocket to window in the new direction

                    coast = False  # Change the value of coast to False to prevent eternal coasting

                # Control input to fire a missile from the rocket
                if 'Down' in keyboard:

                    # Selection statement allows for up to 5 missiles to be fired on screen.
                    if len(missileList) < 5:
                        missileList.append(Missile(rocket))  # Appends a new missile to the missile list at the end of index
                        missileList[-1].drawMissile(win)  # Draws the last index value missile to the window
                        scoreBoard.setMissile(1)  # Increment the score counter by value of 1 on scoreboard
                        time.sleep(.01)

                # For loop to iterate through the asteroid list to detect collision and move the asteroid
                for asteroid in asteroidList:

                    # Selection statement determines if the asteroid is hit(true)
                    if asteroid.isHit(missileList):
                        element = asteroidList.index(asteroid)  # Find the current element value and assign it to a variable
                        asteroidList.pop(element)  # Remove the indexed asteroid from the list
                        scoreBoard.setAsteroid(1)  # Increment the score counter by a value of 1 for the scoreboard

                    # Selection statement determines if the Rocket has collided with the asteroid
                    if asteroid.collision(origin.getPoint()):
                        rocket.undraw()  # Undraw the rocket since it collided

                        Message.lose.draw(win)
                        Message.loseStatus = True
                        print(f"GAME OVER")  # print game over to console
                        play = False  # Break the game loop to end the game

                    asteroid.moveAsteroid(win)  # Move the asteroid if no collision detected

                # For loop iterates over the missile list, moving or removing it
                for missile in missileList:

                    # Determine if the missile has moved too far, if so then remove it
                    if missile.calcDistance() > 10000:
                        element = missileList.index(missile)  # Find the index value of current missile and store it
                        missile.undrawMissile()  # undraw the missile that has traveled too far
                        missileList.pop(element)  # Remove the missile that has traveled too far

                    missile.moveMissile(win)  # Double move missile so it outpaces forward movement of spaceship
                    missile.moveMissile(win)  # Double move missile so it outpaces forward movement of spaceship

                print(f"Asteroids remaining: {len(asteroidList)}")  # Console output for debugging
                print(f"Missile List: {len(missileList)}")  # Console output for debugging

                # Iterator through the ufo list, determine if it is hit or collided with the rocket, move it
                for ufo in ufoList:
                    # If the ufo is hit by a missile remove it from the game
                    if ufo.isHit(missileList):
                        element = ufoList.index(ufo)  # Find the index value of the ufo
                        ufoList.pop(element)  # Remove the indexed ufo from the list

                    # If the ufo collided with the rocket, remove the rocket and end the game
                    if ufo.collision(origin.getPoint()):
                        rocket.undraw()  # Undraw the rocket since it collided

                        Message.lose.draw(win)
                        Message.loseStatus = True
                        print(f"GAME OVER")  # print game over to console
                        play = False  # Break the game loop to end the game

                    ufo.moveUfo(win)  # Move the ufo if no collision detected

                # If the ufo has been destroyed draw a message to the scoreboard once
                if len(ufoList) == 0 and ufoAlive == True:
                    scoreBoard.setUFO(win)  # draw the message to the window
                    ufoAlive = False  # Change value to false to prevent redrawing of existing object error message

                # End the game in victory if all asteroids and ufo have been destroyed
                if len(ufoList) == 0 and len(asteroidList) == 0:
                    rocket.undraw()  # Undraw Rocket ship

                    for missile in missileList:
                        missile.undrawMissile()  # Clear window of missiles for clean victory screen


                    Message.winMessage.draw(win)
                    Message.winStatus = True
                    print(f"YOU WIN")  # Print 'You Win' to console
                    play = False  # Break the while loop to end the game

                scoreBoard.updateBoard()  # Update the scoreboard with current values
                win.update()  # update the window




        if 'Escape' in keyboard:
            title.undraw()
            exitMsg.draw(win)

            exit = True


        win.update()



        # if 'Up' in keyboard:
        #
        #     while play == True:
        #         title.undraw()
        #
        #
        # if 'Down' in keyboard:
        #     exit = True


    win.getMouse()  # Wait for mouse click
    win.close()  # Close window


if __name__ == "__main__":
    main()