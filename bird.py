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


def wing_phase(elapsed, offset):
    return (elapsed * FLAPS_PER_SECOND + offset) % 1.0
