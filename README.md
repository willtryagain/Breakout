# breakout-21
## Introduction
This is a CLI game written in Python3, inspired by the original **Breakout**. The ball moves straight around the screen, bouncing off the top and two sides of the screen. When a brick is hit, the ball bounces back and the brick is destroyed. The player loses a life when the ball touches the bottom of the screen; to prevent this from happening, the player has a horizontally movable paddle to bounce the ball upward, keeping it in play.  
## Gameplay
* You control the paddle to increase your score and to save the ball from falling down. There are three balls.

## Start the game
> $ python3 main.py

## Controls
- <kbd>W</kbd>: move the ball right 
- <kbd>A</kbd>: move the paddle left
- <kbd>S</kbd>: move the ball left
- <kbd>D</kbd>: move the paddle right

- <kbd>SPACE</kbd>: move the ball if lost a life
- <kbd>P</kbd>: pause / unpause
- <kbd>Q</kbd>: quit
- <kbd>L</kbd>: level up





## Classes
These are the classes used in the game
### Game
The `Game` class manages all the other the classes. It handles collisions between objects, adding and removing items from screen. 
### Meta
The `Meta` class is responsible for storing the coordinates and ascii representation of objects. It forms a backbone of all the object classes visible on the screen.
### Display
The `Display` class is responsible for showing all the objects on the console.

### Paddle 
The `Paddle` class is responsible for movement and appearance of paddle. It inherits from Meta class.

### Brick 
The `Brick` class is responsible for strength and color of bricks.

### Ball 
The `Ball` class handles the movement of the ball. It also has a function called go_fast which is invoked when the fastball powerup is activated.

### Powerup
It is the parent class of all the powerups. This handles the movement of the powerup and the collision with the paddle.

* #### Expand 
    Expand Paddle: Increases the size of the paddle by a certain amount.
* #### Shrink 
    Shrink Paddle: Reduce the size of the paddle by a certain amount but not completely.
* #### Fastball 
    Increases the speed of the ball.
* #### Thruball 
    Thru-ball: This enables the ball to destroy and go through any brick it touches, irrespective of the
strength of the wall.(Even the unbreakable ones which you couldn’t previously destroy)
* #### Pgrab 
    Paddle Grab: Allows the paddle to grab the ball on contact and relaunch the ball at will.
