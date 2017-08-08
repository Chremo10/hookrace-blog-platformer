from basic2d import Point2d, Vector2d
from enum import Enum, IntEnum
from sdl2.ext import Renderer, Resources, SpriteFactory, TextureSprite
from typing import List, Optional, Tuple


TILE_WIDTH = 64
TILE_HEIGHT = 64
TILES_PER_ROW = 16


# tile types defined in *.map files
class Tile(IntEnum):
    AIR = 0
    START = 78
    FINISH = 110


class Collision(Enum):
    X = 1
    Y = 2
    CORNER = 3


class Map:
    def __init__(self, resources: Resources) -> None:
        self.texture = None  # type: Optional[TextureSprite]
        self.texture_path = resources.get_path("grass.png")
        self.tiles = []  # type: List[int]
        self.width = 0
        self.height = 0

        file_name = resources.get_path("default.map")
        file = open(file_name, "r")
        for line in file.readlines():
            width = 0
            for word in line.split(' '):
                if word == "":
                    continue
                value = int(word)
                self.tiles.append(value)
                width += 1

            if self.width > 0 and self.width != width:
                raise RuntimeError("Incompatible line length in map " + file_name)
            self.width = width
            self.height += 1

    def __get_tile(self, x: int, y: int) -> int:
        nx = min(max(int(x / TILE_WIDTH), 0), self.width - 1)
        ny = min(max(int(y / TILE_HEIGHT), 0), self.height - 1)
        pos = ny * self.width + nx
        return self.tiles[pos]

    def get_tile(self, pos: Point2d) -> int:
        return self.__get_tile(int(round(pos.x)), int(round(pos.y)))

    def __is_solid(self, x: int, y: int) -> bool:
        return self.__get_tile(x, y) not in {Tile.AIR, Tile.START, Tile.FINISH}

    def is_solid(self, pos: Point2d) -> bool:
        return self.__is_solid(int(round(pos.x)), int(round(pos.y)))

    def on_ground(self, pos: Point2d, size: Vector2d) -> bool:
        half_size = size * 0.5  # type: Vector2d
        return (self.is_solid(Point2d(pos.x - half_size.x, pos.y + half_size.y + 1)) or
                self.is_solid(Point2d(pos.x + half_size.x, pos.y + half_size.y + 1)))

    def test_box(self, pos: Point2d, size: Vector2d) -> bool:
        half_size = size * 0.5  # type: Vector2d
        return (
            self.is_solid(Point2d(pos.x - half_size.x, pos.y - half_size.y)) or
            self.is_solid(Point2d(pos.x + half_size.x, pos.y - half_size.y)) or
            self.is_solid(Point2d(pos.x - half_size.x, pos.y + half_size.y)) or
            self.is_solid(Point2d(pos.x + half_size.x, pos.y + half_size.y))
        )

    def move_box(self, pos: Point2d, vel: Vector2d, size: Vector2d) -> Tuple[Point2d, Vector2d]:
        distance = vel.norm
        maximum = int(distance)

        if distance < 0:
            return pos, vel

        fraction = 1.0 / float(maximum + 1)

        for i in range(0, maximum + 1):
            new_pos = pos + vel * fraction  # type: Point2d
            if self.test_box(new_pos, size):
                hit = False
                if self.test_box(Point2d(pos.x, new_pos.y), size):
                    new_pos.y = pos.y
                    vel.y = 0
                    hit = True

                if self.test_box(Point2d(new_pos.x, pos.y), size):
                    new_pos.x = pos.x
                    vel.x = 0
                    hit = True

                if not hit:
                    new_pos = pos
                    vel = Vector2d(0, 0)

            pos = new_pos

        return pos, vel

    def render(self, renderer: Renderer, camera: Vector2d):
        if self.texture is None:
            factory = SpriteFactory(renderer=renderer)
            self.texture = factory.from_image(self.texture_path)
        texture = self.texture  # type: TextureSprite

        for i, tile_nr in enumerate(self.tiles):
            if tile_nr == 0:
                continue
            clip_x = (tile_nr % TILES_PER_ROW) * TILE_WIDTH
            clip_y = int(tile_nr / TILES_PER_ROW) * TILE_HEIGHT
            dest_x = (i % self.width) * TILE_WIDTH - int(camera.x)
            dest_y = int(i / self.width) * TILE_HEIGHT - int(camera.y)

            clip = (clip_x, clip_y, TILE_WIDTH, TILE_HEIGHT)
            dest = (dest_x, dest_y, TILE_WIDTH, TILE_HEIGHT)
            renderer.copy(texture, clip, dest)

