from math import ceil


SHEET_HEIGHT = 506
COLUMN_WIDTH = 182
LAST_COLUMN_WIDTH = 190
ROW_BOUNDS = ((0, 180), (180, 354), (354, 506))
EYE_Y_BY_ROW = (
    (93, 92, 91, 88, 85),
    (254, 253, 253, 254, 256),
    (429, 431, 432, 433),
)

BIRD_FRAMES = tuple(
    (column * COLUMN_WIDTH, SHEET_HEIGHT - bottom,
     LAST_COLUMN_WIDTH if column == 4 else COLUMN_WIDTH, bottom - top,
     eye_y + 10 - top)
    for (top, bottom), eye_positions in zip(ROW_BOUNDS, EYE_Y_BY_ROW)
    for column, eye_y in enumerate(eye_positions)
)

FLAPS_PER_SECOND = 2.5
FLIGHT_SPEED = 220.0
DRAW_SCALE = 0.4
BODY_X = 103
SPRITE_MARGIN = ceil(max(BODY_X, LAST_COLUMN_WIDTH - BODY_X) * DRAW_SCALE)


def wing_phase(elapsed, offset):
    return (elapsed * FLAPS_PER_SECOND + offset) % 1.0


def draw_bird(image, x, y, direction, phase):
    left, bottom, width, height, body_y = BIRD_FRAMES[int(phase * len(BIRD_FRAMES))]
    center_x = x + direction * (width / 2 - BODY_X) * DRAW_SCALE
    center_y = y + (body_y - height / 2) * DRAW_SCALE
    image.clip_composite_draw(
        left, bottom, width, height, 0, 'h' if direction < 0 else '',
        center_x, center_y, round(width * DRAW_SCALE), round(height * DRAW_SCALE),
    )


def patrol_position(elapsed, left, right):
    span = right - left
    distance = (elapsed * FLIGHT_SPEED) % (2 * span)
    if distance < span:
        return left + distance, 1
    return right - (distance - span), -1
