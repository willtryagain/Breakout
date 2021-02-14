import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

from screen import Screen
import config as conf
from thing import Thing
from obstacle import FireBeam, MandalorianBullet, Boost, Magnet
from kbhit import KBHit
from mandalorian import Mandalorian
import utils
from boss import Boss
from dragon import Dragon

class Game:
    PLAY_KEYS = ('w', 'a', 'd')
    CONTROL_KEYS = ('q',)

    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        self._height = int(rows) - conf.BUFFER_DOWN
        self._width = int(cols) - conf.BUFFER_RIGHT
        
        self._screen = Screen(self._height, self._width)
        self._keyboard = KBHit()
        self._frame_count = 0

        self._lives = conf.MAX_LIVES
        self._score = 0
        self._init_time = clock()
        self._money = 0

        self._fire_beams = []
        self._coins = []
        self._mandalorian_bullets = []
        self._boosts = []
        self._boost = None 
        self._magnets = []
        self._player = Mandalorian(self._height, self._width, conf.MANDALORIAN_START_Y)

        self._shield = False
        self._shield_time = clock()

        self._boss = None
        self._boss_bullets = []
        self._boss_time = None 

        self._dragon = None
        self._dragon_done = False
        self._dragon_time = None

    def build_firebeam(self):
        num = random.randint(0, 2)

        if num != 0:
            for i in range(num):
                direc = random.randint(0, 3)
                size = random.randint(
                    conf.MIN_BEAM_SIZE, conf.MAX_BEAM_SIZE - num
                ) 
                self._fire_beams.append(FireBeam(self._height, self._width, direc, random.randint(
                    conf.SKY_DEPTH, self._height - conf.GND_HEIGHT - size), self._width)
                )

    def build_coins(self):
        h = random.randint(conf.MIN_COIN_SIZE, conf.MAX_COIN_SIZE)
        w = random.randint(conf.MIN_COIN_SIZE, conf.MAX_COIN_SIZE)

        x = random.randint(conf.SKY_DEPTH, self._height - conf.GND_HEIGHT - h)

        self._coins.extend(utils.make_coin_group(self._height, self._width, h, w))

    def build_boost(self):
        if random.random() < conf.BOOST_PROBAB:
            self._boosts.append(Boost(self._height, self._width))

    def build_magnet(self):
        if random.random() < conf.MAGNET_PROBAB:
            self._magnets.append(Magnet(self._height, self._width))

    def build_boss_bullet(self):
        self._boss_bullets.append(self._boss.shoot(self._player))

    def build_world(self):
        if self._boss is None:
            if self._frame_count % conf.MIN_BEAM_DIST_X:
                self.build_firebeam()

            if random.random() < conf.COIN_PROBAB:
                self.build_coins()

            if random.random() < conf.MAGNET_PROBAB:
                self.build_magnet()     

            if self._boost is None and len(self._boosts) == 0:
                self.build_boost()

        else:
            if random.random() < conf.BOSS_SHOOT_PROBAB:
                self.build_boss_bullet()
    
    def handle_beam_collisions(self):
        if self._dragon is not None:
            return

        for fb in self._fire_beams:
            if self.check_collision(self._player, fb):
                self._lives -= 1
                if self._lives == 0:
                    self.game_over(won=False) 
                else:
                    self._screen.flash(Back.RED + ' ', self._frame_count) 
                    self._fire_beams.remove(fb)

    def handle_coin_collisions(self):
        obj = self._dragon
        if self._dragon is None:
            obj = self._player        

        for co in self._coins:
            if self.check_collision(obj, co, cheap=True, buffer=True):
                self._money += 1
                self._score += conf.SCORE_COIN_FACTOR
                self._coins.remove(co)

    
    def handle_mandalorian_bullet_collisions(self):
        for bu in self._mandalorian_bullets:
            hit = False
            for fb in self._fire_beams:
                if self.check_collision(fb, bu, cheap=True, buffer=True):
                    self._score += conf.SCORE_BEAM_FACTOR
                    hit = True
            
            if self._boss is not None:
                if self.check_collision(self._boss, bu, cheap=False, buffer=False):
                    self._score += conf.SCORE_BOSS_HIT_FACTOR
                    hit = True
                    if self._boss.take_hit():
                        raise self.game_over(won=True)

                for fi in self._boss_bullets:
                    if self.check_collision(fi, bu, cheap=True, buffer=True):
                        self._score += conf.SCORE_BOSS_BULLET_FACTOR
                        self._boss_bullets.remove(fi)
                        hit = True
                    
            if hit:
                self._mandalorian_bullets.remove(bu)

    def handle_boost_collisions(self):

        if self._dragon is not None:
            return 

        for bo in self._boosts:
            if self.check_collision(self._player, bo, cheap=True):
                for obj in self._fire_beams:
                    bo.affect(obj)
                for obj in self._magnets:
                    bo.affect(obj)
                for obj in self._boosts:
                    bo.affect(obj)
                for obj in self._coins:
                    bo.affect(obj)
                self.move_objs()
                conf.GAME_SPEED += conf.BOOST_SPEED
                self._boost = [bo, clock()]
                self._boosts.remove(bo)
                self._screen.flash(Back.MAGENTA + ' ', self._frame_count)
                self._score += conf.SCORE_BOOST_FACTOR

    def handle_boss_collisions(self):

        if self.check_collision(self._player, self._boss, cheap=False, buffer=False):
            self.game_over(won=False) 

    def handle_boss_bullet_collisions(self):
        for bu in self._boss_bullets:
            if self.check_collision(self._player, bu, cheap=True, buffer=True):
                self._boss_bullets.remove(bu)
                self._lives -= 1
                if self._lives <= 0:
                    self.game_over(won=False) 
                else:
                    self._screen.flash(Back.RED + ' ', self._frame_count, times=1)
            
    
    def handle_collisions(self):
        self.handle_coin_collisions()
        self.handle_mandalorian_bullet_collisions()
        self.handle_boost_collisions()
        if not self._shield:
            self.handle_beam_collisions()
        
        if self._boss is not None:
            self.handle_boss_collisions()
            if not self._shield:
                self.handle_boss_bullet_collisions()

    def end_boost(self, forceful=False):
        if self._boost is None:
            return

        if forceful or clock() < self._boost[1] > conf.BOOST_UP_TIME:
            bo = self._boost[0]
            for obj in self._fire_beams:
                bo.unaffect(obj)
            for obj in self._magnets:
                bo.unaffect(obj)
            for obj in self._boosts:
                bo.unaffect(obj)
            for obj in self._coins:
                bo.unaffect(obj)
            self.move_objs()
            conf.GAME_SPEED -= conf.BOOST_SPEED
            self._boost = None
            self._screen.flash(Back.MAGENTA + ' ', self._frame_count)

    def pull_magnet(self):

        if self._dragon is not None:
            return

        if len(self._magnets) != 0:
            for ma in self._magnets:
                ma.affect(self._player)

    def start_shield(self):
        if self._dragon is not None:
            return

        if self._shield:
            return

        if clock() - self._shield_time > conf.SHIELD_SLEEP_TIME:
            self._shield = True
            self._player.set_shield(True)
            self._shield_time = clock()
            self._screen.flash(Back.CYAN + ' ', self._frame_count)

    def end_shield(self):
        if not self._shield:
            return

        if clock() - self._shield_time > conf.SHIELD_UP_TIME:
            self._shield = False
            self._player.set_shield(False)
            self._shield_time = clock()
            self._screen.flash(Back.CYAN + ' ', self._frame_count)

    def remove_old_objs(self):
        for fb in self._fire_beams:
            if fb.is_out()[1]:
                self._fire_beams.remove(fb)

        for co in self._coins:
            if co.is_out()[1]:
                self._coins.remove(co)

        for ma in self._magnets:
            if ma.is_out()[1]:
                self._magnets.remove(ma)

        for bo in self._boosts:
            if bo.is_out()[1]:
                self._boosts.remove(bo)

        for bu in self._mandalorian_bullets:
            if bu.is_out()[1]:
                self._mandalorian_bullets.remove(bu)

        if self._boss is not None:
            for bu in self._boss_bullets:
                if bu.is_out()[3]:
                    self._mandalorian_bullets.remove(bu)

    def paint_objs(self):

        for fb in self._fire_beams:
            self._screen.add(fb)

        for co in self._coins:
            self._screen.add(co)

        for ma in self._magnets:
            self._screen.add(ma)

        for bo in self._boosts:
            self._screen.add(bo)
        
        if self._boss is not None:
            self._screen.add(self._boss)

            for bu in self._boss_bullets:
                self._screen.add(bu)

        for bu in self._mandalorian_bullets:
            self._screen.add(bu)

        if self._player is None:
            self._screen.add(self._dragon)
        else:
            self._screen.add(self._player)

    def move_objs(self):
        for fb in self._fire_beams:
            fb.move()

        for co in self._coins:
            co.move()

        for ma in self._magnets:
            ma.move()

        for bo in self._boosts:
            bo.move()
        
        for bu in self._mandalorian_bullets:
            bu.move()

        if self._dragon is None:
            self._player.move()
        else:
            self._dragon.move()
        
        if self._boss is not None:
            self._boss.move()

            for bu in self._boss_bullets:
                bu.move()

    def reset_acc_objs(self):
        for fb in self._fire_beams:
            fb.reset_acc()

        for co in self._coins:
            co.reset_acc()

        for ma in self._magnets:
            ma.reset_acc()

        for bo in self._boosts:
            bo.reset_acc()
        
        for bu in self._mandalorian_bullets:
            bu.reset_acc()

        if self._player is None:
            self._dragon.reset_acc()
        else:
            self._player.reset_acc()
        
        if self._boss is not None:
            self._boss.reset_acc()

            for bu in self._boss_bullets:
                bu.reset_acc()

    def fire(self):
        if self._dragon is not None:
            return 
        
        pos = self._player.show()[0]
        self._mandalorian_bullets.append(MandalorianBullet(self._height, self._width, int(pos[0]) + 1, int(pos[1]) + 2))

    def handle_input(self):
        if self._keyboard.kbhit():
            inp = self._keyboard.getch()

            if inp in self.PLAY_KEYS:
                if self._dragon is None:
                    self._player.nudge(inp)
                else:
                    self._dragon.nudge(inp)
            
            elif inp == 'e':
                self.fire()
            
            elif inp == ' ':
                self.start_shield()
            
            elif inp == 'g':
                self.setup_dragon()
            
            elif inp == 'q':
                self.game_over(won=False)
            
            self._keyboard.flush()

    def game_over(self, won=False):
        sleep(1)
        self._screen.game_over(won, self._score, int(clock() - self._init_time))
        while True:
            if self._keyboard.kbhit():
                if self._keyboard.getch() == 'f':
                    break
        self._keyboard.set_normal_term()
        raise SystemExit

    def setup_boss(self):
        if self._boss is not None:
            return
        
        if clock() - self._init_time <= conf.BOSS_ARRIVAL_TIME:
            return

        self._screen.flash(Back.YELLOW + ' ', self._frame_count)
        self._boss = Boss(self._height, self._width)
        self._boss_time = clock()

        self.end_boost(forceful=True)
        self.end_dragon(forceful=True)
        self._fire_beams.clear()
        self._coins.clear()
        self._mandalorian_bullets.clear()
        self._boosts.clear()
        self._magnets.clear()

    def setup_dragon(self):
        if self._boss is not None:
            return
        
        if self._dragon is not None or self._dragon_done:
            return

        self._dragon_time = clock()
        self._dragon = Dragon(self._height, self._width)
        self.end_boost(forceful=True)

    def end_dragon(self, forceful=False):
        if self._dragon is None:
            return

        if not forceful and clock() - self._dragon_time <= conf.DRAGON_TIME:
            return

        self._dragon = False
        self._dragon_done = True
    
    def end_boss(self):
        if self._boss is None:
            return

        if clock() - self._boss_time > conf.BOSS_TIME_LIMIT:
            self.game_over(won=False)

    def check_collision(self, obj_a, obj_b, cheap=False, buffer=False):
        if buffer and not cheap:
            raise ValueError

        a_pos, a_size, a_repr = obj_a.show()
        b_pos, b_size, b_repr = obj_b.show()

        a_rec = [a_pos[0], a_pos[0] + a_size[0] - 1, a_pos[1], a_pos[1] - 1]
        if buffer:
            b_rec = [b_pos[0] - 1, b_pos[0] + b_size[0], b_pos[1] - 1, b_pos[1] + b_size[1]]
        else:
            b_rec = [b_pos[0], b_pos[0] + b_size[0] - 1, b_pos[1], b_pos[1] + b_size[1] - 1]  

        bump, common = utils.intersect(a_rec, b_rec)

        if cheap or buffer:
            return bump

        if not bump:
            return False
        
        a_idx = [common[0] - a_pos[0], common[1] - a_pos[0] + 1, common[2] - a_pos[1], common[3] - a_pos[1] + 1]
        b_idx = [common[0] - b_pos[0], common[1] - b_pos[0] + 1, common[2] - b_pos[1], common[3] - b_pos[1] + 1]

        for i in range(common[1] + 1 - common[0]):
            for j in range(common[3] + 1 - common[2]):
                a_i = a_idx[0] + i
                a_j = a_idx[2] + j

                b_i = b_idx[0] + i
                b_j = b_idx[2] + j

                if a_repr[a_i][a_j] != ' ' and b_repr[b_i][b_j] != ' ':
                    return True
                
        return False

    def print_info(self):

        print(Style.RESET_ALL + Style.BRIGHT, end='')
        print('\033[0K', end='')
        print('LIVES:', str(self._lives).rjust(1), end='\t')
        print('SCORE:', str(self._score).rjust(5), end='\t')
        time = int(clock() - self._init_time)
        print('TIME:', str(time).rjust(5), end='\t')

    def play(self):
        while True:
            self.setup_boss()
            start_time = clock()

            self.build_world()
            self.reset_acc_objs()
            self.handle_input()
            self.pull_magnet()
            self.move_objs()
            self.remove_old_objs()
            self.handle_collisions()

            self._screen.clear()
            self.paint_objs()
            
            self.end_shield()
            self.end_boost()
            self.end_dragon()
            self.end_boss()

            self._screen.print_board(self._frame_count)
            self.print_info()
            self._frame_count += 1
            self._score += conf.SCORE_TIME_FACTOR
            while clock() - start_time < 0.1:
                pass

   