import unittest
from unittest.mock import Mock, patch

import bird


class BirdFlightTests(unittest.TestCase):
    def test_wing_cycle_draws_all_poses_and_keeps_the_body_anchor(self):
        image = Mock()
        for frame, (left, bottom, width, height, body_y) in enumerate(bird.BIRD_FRAMES):
            elapsed = (frame + 0.5) / (14 * bird.FLAPS_PER_SECOND)
            phase = bird.wing_phase(elapsed, 0)
            for direction, flip in ((1, ''), (-1, 'h')):
                bird.draw_bird(image, 200, 300, direction, phase)
                args = image.clip_composite_draw.call_args.args
                self.assertEqual(args[:6], (left, bottom, width, height, 0, flip))
                self.assertAlmostEqual(
                    args[6] + direction * (bird.BODY_X - width / 2) * bird.DRAW_SCALE, 200
                )
                self.assertAlmostEqual(
                    args[7] + (height / 2 - body_y) * bird.DRAW_SCALE, 300
                )
        self.assertEqual(len(bird.BIRD_FRAMES), 14)
        self.assertEqual(bird.wing_phase(1 / bird.FLAPS_PER_SECOND, 0), 0)

    def test_patrol_reflects_at_each_end_and_preserves_overshoot(self):
        left, right = 42, 482
        self.assertEqual(bird.patrol_position(0, left, right), (42, 1))
        self.assertEqual(bird.patrol_position(2, left, right), (482, -1))
        self.assertEqual(bird.patrol_position(2.5, left, right), (372, -1))
        self.assertEqual(bird.patrol_position(4, left, right), (42, 1))
        self.assertEqual(bird.patrol_position(8.5, left, right), (152, 1))

    @patch('bird.load_image')
    @patch('bird.get_canvas_width', return_value=1600)
    @patch('bird.get_canvas_height', return_value=600)
    @patch('bird.draw_bird')
    def test_formation_stays_visible_and_mirrors_together(self, draw, _height, _width, load):
        flock = bird.BirdFlock()
        load.assert_called_once_with('bird_animation.png')
        separation = []
        for elapsed, direction in ((0, 1), ((flock.right - flock.left) / bird.FLIGHT_SPEED, -1)):
            draw.reset_mock()
            flock.elapsed = 0
            with patch('game_framework.frame_time', elapsed, create=True):
                flock.update()
            flock.draw()
            birds = [call.args[1:] for call in draw.call_args_list]
            self.assertEqual(len(birds), 10)
            self.assertEqual(len({phase for _, _, _, phase in birds}), 10)
            self.assertEqual({facing for _, _, facing, _ in birds}, {direction})
            self.assertTrue(all(bird.SPRITE_MARGIN <= x <= 1600 - bird.SPRITE_MARGIN
                                for x, _, _, _ in birds))
            separation.append([x - birds[0][0] for x, _, _, _ in birds])
        self.assertEqual(separation[0], separation[1])
