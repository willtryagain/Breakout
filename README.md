# breakout-21
## Introduction
This is a CLI game written in Python3, inspired by the original **Breakout**. The ball moves straight around the screen, bouncing off the top and two sides of the screen. When a brick is hit, the ball bounces back and the brick is destroyed. The player loses a life when the ball touches the bottom of the screen; to prevent this from happening, the player has a horizontally movable paddle to bounce the ball upward, keeping it in play.  
## Gameplay
* You control the paddle and 


## Controls
- <kbd>W</kbd>: move the ball right 
- <kbd>A</kbd>: move the paddle left
- <kbd>S</kbd>: move the ball left
- <kbd>D</kbd>: move the paddle right

- <kbd>SPACE</kbd>: move the ball if lost a life
- <kbd>P</kbd>: pause / unpause
- <kbd>Q</kbd>: quit

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

### Powerup

