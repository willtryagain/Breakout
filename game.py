import os
import sys
from random import choice, randint, random
from time import monotonic as clock
from time import sleep

import icecream as ic
from colorama import Back, Fore, Style

import settings
from ball import Ball
from brick import Brick
from display import Display
from expand import Expand
from fastball import Fastball
from kbhit import KBHit
from multi import Multi
from paddle import Paddle
from pgrab import Pgrab
from powerup import Powerup
from shrink import Shrink
from thruball import Thruball

debug = ""


class Game:
    """
    This class acts like the puppeteer for the sprites. It orchestrates the game from start to end.
    """

    def __init__(self, display, kbhit, ball, paddle, brick_container, player):
        """ """
        self.PAUSED = False
        self.display = display
        self.kbhit = kbhit
        self.ball = ball
        self.paddle = paddle
        self.brick_container = brick_container
        self.player = player
        self._powerups = []

    def ball_paddle_collide(self):
        """
        check if ball collided with the paddle
        """
        left_paddle = self.paddle.y
        right_paddle = self.paddle.y + self.paddle.width - 1
        height_paddle = self.paddle.x

        height_ball = self.ball.x
        left_ball = self.ball.y
        right_ball = self.ball.y + self.ball.width

        # ball is just above paddle
        if height_ball == height_paddle - 1:
            if left_paddle <= left_ball and right_ball <= right_paddle:
                return True

        return False

    def ball_paddle_collide_handle(self):
        if self.ball._dead or self.paddle._grab:
            self.ball._velocity.vx = -1
            self.ball._velocity.vy = 1

        # middle position of paddle
        mid = (2 * self.paddle.y + self.paddle.width - 1) // 2

        # in first half
        if self.ball.y < mid:
            # go left
            sign = -1
        else:
            # go right
            sign = 1
        vx = self.ball._velocity.vx
        if vx > 0:
            raise ValueError("check vx")

        vy = self.ball._velocity.vy

        # distance from the middle
        bias = abs(mid - self.ball.y) // 2

        vy = sign * abs(Powerup.inc_mag(vy, bias))
        self.ball._velocity.vx = vx
        self.ball._velocity.vy = vy

    def ball_side_walls_collide(self):
        """
        check if ball collided with the side walls
        """
        left_ball = self.ball.y
        right_ball = self.ball.y + self.ball.width - 1

        left_wall = 0
        right_wall = self.display.width - 1

        # hits the side walls
        if left_ball == left_wall or right_wall == right_ball:
            return True

        return False

    def ball_top_collide(self):
        """
        check if ball collided with the top wall
        """
        top_ball = self.ball.x
        top_wall = 0

        if top_ball == top_wall:
            return True

        return False

    def ball_brick_horizontal_collide(self):
        """
        handle collision with brick
        atmost one at a time
        Above brick
           O
           V
        [|||||]

        Below brick
        [|||||]
           ^
           o

        """
        top_ball = self.ball.x
        bottom_ball = self.ball.x + self.ball.height

        left_ball = self.ball.y
        right_ball = self.ball.y + self.ball.width

        for index, brick in enumerate(self.brick_container.sprites):
            left_brick = brick.y
            right_brick = left_brick + brick.width

            top_brick = brick.x
            bottom_brick = top_brick + brick.height

            in_between = left_brick <= left_ball and right_ball <= right_brick

            if in_between:
                # above
                if bottom_ball == top_brick:
                    return index
                # below
                elif top_ball == bottom_brick:
                    return index

        return -1

    def ball_brick_vertical_collide(self):
        """
        handle collision with brick
        atmost one at a time
        Left of brick

        o   [|||||]

        Right of brick
            [|||||]    o
        """

        top_ball = self.ball.x
        bottom_ball = self.ball.x + self.ball.height

        left_ball = self.ball.y
        right_ball = self.ball.y + self.ball.width

        for index, brick in enumerate(self.brick_container.sprites):
            left_brick = brick.y
            right_brick = left_brick + brick.width

            top_brick = brick.x
            bottom_brick = top_brick + brick.height

            in_between = top_brick <= top_ball and bottom_ball <= bottom_brick

            if in_between:
                # left
                if right_ball == left_brick:
                    return index
                # right
                elif left_ball == right_brick:
                    return index

        return -1

    def ball_brick_corners_collide(self):
        top_ball = self.ball.x
        bottom_ball = self.ball.x + self.ball.height

        left_ball = self.ball.y
        right_ball = self.ball.y + self.ball.width

        for index, brick in enumerate(self.brick_container.sprites):
            left_brick = brick.y
            right_brick = left_brick + brick.width

            top_brick = brick.x
            bottom_brick = top_brick + brick.height

            if bottom_ball == top_brick:
                if (left_ball <= left_brick and left_brick <= right_ball) or (
                    left_ball <= right_brick and right_brick <= right_ball
                ):
                    return index

            if top_ball == bottom_brick:
                if (left_ball <= left_brick and left_brick <= right_ball) or (
                    left_ball <= right_brick and right_brick <= right_ball
                ):
                    return index

        return -1

    def lost_ball(self):
        bottom_ball = self.ball.x + self.ball.height
        bottom_display = self.display.height

        return bottom_ball >= bottom_display

    def ball_brick_intersection(self):
        global debug
        vx = self.ball._velocity.vx
        vy = self.ball._velocity.vy
        while self.ball.intersects(self.brick_container.sprites):
            if vx < 0:
                self.ball.move_down()
            else:
                self.ball.move_up()

            if vy < 0:
                self.ball.move_right()
            else:
                self.ball.move_right()
        # debug += str(self.ball_brick_horizontal_collide(ball)) + ':' + \
        #     str(self.ball_brick_vertical_collide(ball)) + '\n'
        # self.ball.reverse_vx()

    def collide(self):
        global debug
        if self.ball._dead:
            return

        if self.ball_side_walls_collide():
            self.ball.reverse_vy()
            return

        if self.ball_top_collide():
            self.ball.reverse_vx()
            return

        if self.ball_paddle_collide():
            if self.paddle._grab:
                self.ball._velocity.vx = 0
                self.ball._velocity.vy = 0
            else:
                self.ball.reverse_vx()
                self.ball_paddle_collide_handle()
            return

        if self.ball.intersects(self.brick_container.sprites):
            self.ball_brick_intersection()

        index = self.ball_brick_corners_collide()
        if index != -1:
            # debug += 'corners\n'
            self.ball.reverse_vx()
            self.player._score += self.brick_container.sprites[index].get_damage_points(
                self.ball
            )
            self.brick_container.sprites[index].repaint_brick()
            return

        index = self.ball_brick_horizontal_collide()
        if index != -1:
            # debug += 'horizontal\n'
            self.ball.reverse_vx()
            self.player._score += self.brick_container.sprites[index].get_damage_points(
                self.ball
            )
            self.brick_container.sprites[index].repaint_brick()
            return

        index = self.ball_brick_vertical_collide()
        if index != -1:
            self.ball.reverse_vy()
            self.player._score += self.brick_container.sprites[index].get_damage_points(
                self.ball
            )
            self.brick_container.sprites[index].repaint_brick()
            return

        return

    def get_powerup(self, pos):
        type = choice(["expand", "shrink", "fastball", "pgrab", "thruball"])
        # type = choice(['multi'])

        if type == "expand":
            powerup = Expand(pos, clock())
        elif type == "shrink":
            powerup = Shrink(pos, clock())
        elif type == "fastball":
            powerup = Fastball(pos, clock())
        elif type == "multi":
            powerup = Multi(pos, clock())
        elif type == "pgrab":
            powerup = Pgrab(pos, clock())
        elif type == "thruball":
            powerup = Thruball(pos, clock())
        powerup._state = "FALL"
        return powerup

    def remove_bricks(self):
        global debug
        indices = []
        for index, brick in enumerate(self.brick_container.sprites):
            if brick._strength == 0:
                indices.append(index)
                pos = [brick.x, brick.y]
                # powerup = self.get_powerup(pos)
                # self._powerups.append(powerup)

        indices.sort(reverse=True)
        for index in indices:
            del self.brick_container.sprites[index]

    def remove_powerups(self):
        global debug
        indices = []
        for index, powerup in enumerate(self._powerups):
            if powerup._state == "DELETE":
                # debug += str(index) + '\n'
                indices.append(index)

        indices.sort(reverse=True)
        for index in indices:
            del self._powerups[index]

    def remove_items(self):
        self.remove_bricks()
        self.remove_powerups()

    def ball_paddle_centre(self, ball, rel=None):
        left_paddle = self.paddle.y
        right_paddle = self.paddle.y + self.paddle.width - 1
        mid = (left_paddle + right_paddle) // 2

        if rel:
            y = left_paddle + rel
            self.ball.move_y_to(y)
            return ball

        self.ball.move_y_to(mid)

    def handle_keys(self):
        global debug
        if self.kbhit.kbhit():
            key = self.kbhit.getch()

            # Pause / Unpause
            if key == "q":
                self.end_game()

            # Pause / Unpause
            if key == "p":
                self.PAUSED = not self.PAUSED

            # Paddle left / right
            elif key == "a" or key == "d":
                self.paddle.move(key, self.display.width)
                if self.ball._dead or (
                    self.paddle._grab and self.ball._velocity.vx == 0
                ):
                    self.ball_paddle_centre(self.ball, rel=None)

            # Ball left / right
            elif key == "w" or key == "s":
                if not self.ball._dead:
                    pass
                else:
                    self.ball.move(self.display.height, self.display.width, key)

            # Start the game
            elif key == " ":
                if self.ball_paddle_collide():
                    self.ball_paddle_collide_handle()
                    self.ball._dead = False
            self.kbhit.flush()

    def reset_game(self, ball):
        global debug
        self.remove_items()
        self.display.clrscr()
        self.add_items()
        self.display.show()

        self.ball._dead = True
        self.display.alert()
        self._powerups = self.deactivate()
        self.paddle = Paddle(self.display.height, self.display.width)
        self.ball.x = self.display.height - 2
        self.ball.y = randint(self.paddle.y, self.paddle.y + self.paddle.width - 2)
        self.player.lose_life()
        if self.player._lives == 0:
            self.end_game()
        self.ball._velocity.vx = 0
        self.ball._velocity.vy = 0

    def move_items(self):
        self.ball.move(self.display.height, self.display.width)

        powerups = []
        for powerup in self._powerups:
            if powerup._state == "FALL":
                powerup.move(self.display.height)
            powerups.append(powerup)
        self._powerups = powerups

    def add_items(self):
        # put the balls
        self.display.put(self.ball)

        self.display.put(self.paddle)
        for brick in self.brick_container.sprites:
            if brick._strength:
                self.display.put(brick)

        for powerup in self._powerups:
            if powerup._state == "FALL":
                self.display.put(powerup)

    def powerup_magic(self, powerup):
        if powerup._kind == "pgrab":
            self.paddle = powerup.magic(self.paddle, self._balls[0])
        elif powerup._kind == "fastball":
            self._balls = powerup.magic(self._balls)
        elif powerup._kind == "thruball":
            self._balls = powerup.magic(self._balls)
        else:
            self.paddle = powerup.magic(self.paddle)

    def powerup_reverse(self, powerup):
        if powerup._kind == "multi":
            self._balls = powerup.reverse(self._balls)
        elif powerup._kind == "pgrab":
            self.paddle = powerup.reverse(self.paddle)
        elif powerup._kind == "fastball":
            self._balls = powerup.reverse(self._balls)
        elif powerup._kind == "thruball":
            self._balls = powerup.reverse(self._balls)
        else:
            self.paddle = powerup.reverse(self.paddle)

    def powerup_handle(self):
        global debug
        powerups = []
        for powerup in self._powerups:
            if powerup._state == "FALL":
                if powerup.collision(self.paddle):
                    self.powerup_magic(powerup)
                    if self._balls[0]._fast:
                        self._balls[0].go_fast()
                    debug += "magic\n"

            elif powerup._state == "ACTIVE":
                if powerup.time_up():
                    self.powerup_reverse(powerup)
            powerups.append(powerup)
        self._powerups = powerups

    def wait(self, time):
        while clock() - time < 0.1:
            pass

    def end_game(self):
        global debug
        out = open("debug.txt", "w")
        out.write(debug)
        out.close
        sys.exit(0)

    def deactivate(self):
        powerups = []
        for powerup in self._powerups:
            if powerup._state == "ACTIVE":
                self.powerup_reverse(powerup)
                powerup._state = "DELETE"

            powerups.append(powerup)
        return powerups

    def ball_collisions_handle(self):
        self.collide()
        if self.lost_ball():
            self.reset_game()

    def mainloop(self):
        global debug
        while True:
            time = clock()
            self.handle_keys()
            if self.PAUSED:
                self.wait(time)
                continue

            self.move_items()

            self.ball_collisions_handle()
            self.powerup_handle()
            self.remove_items()
            self.display.clrscr()
            self.add_items()
            self.display.show()
            self.player.display_stats(self.paddle.width, self.ball)
            self.wait(time)
            # debug += str(self._balls[0]._thru) + "\n"
