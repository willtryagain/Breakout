# Generated by CodiumAI

import unittest

from colorama import Back, Fore, Style

from brick import Brick


class TestBrick(unittest.TestCase):
    # creating a new instance of Brick with default strength should set strength to 3 and color to red
    def test_default_strength_and_color(self):
        brick = Brick(0, 0)
        self.assertEqual(brick._strength, 3)
        self.assertEqual(brick._ascii[0][0], Back.RED + " ")

    # creating a new instance of Brick with strength 2 should set color to green
    def test_strength_2_color(self):
        brick = Brick(0, 0, strength=2)
        self.assertEqual(brick._ascii[0][0], Back.GREEN + " ")

    # creating a new instance of Brick with strength 1 should set color to magenta
    def test_strength_1_color(self):
        brick = Brick(0, 0, strength=1)
        self.assertEqual(brick._ascii[0][0], Back.MAGENTA + " ")

    # creating a new instance of Brick with strength -1 should raise an exception
    def test_negative_strength_exception(self):
        with self.assertRaises(Exception):
            Brick(0, 0, strength=-1)

    # calling get_damage_points with strength -1 should return 0 and not decrement strength
    def test_get_damage_points_negative_strength(self):
        brick = Brick(0, 0, strength=-1)
        self.assertEqual(brick.get_damage_points(), 0)
        self.assertEqual(brick._strength, -1)

    # calling reset_ascii with length 0 should raise an exception
    def test_reset_ascii_length_zero_exception(self):
        brick = Brick(0, 0)
        with self.assertRaises(Exception):
            brick.reset_ascii(length=0)


if __name__ == "__main__":
    unittest.main()
