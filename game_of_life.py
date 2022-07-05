import random
from copy import deepcopy
from threading import Lock

CellType = tuple[int, int]
CoordinatesType = tuple[
    CellType, CellType, CellType, CellType, CellType, CellType, CellType, CellType
]
UniverseType = list[list[int]]


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameOfLife(metaclass=SingletonMeta):
    def __init__(self, width: int = 20, height: int = 20):
        self.__width = width
        self.__height = height
        self.world = self.generate_universe()
        self.old_world = self.world
        self.iteration = 0

    def form_new_generation(self) -> None:
        universe = self.world
        self.old_world = deepcopy(universe)
        new_world = [[0 for _ in range(self.__width)] for _ in range(self.__height)]

        for i in range(len(universe)):
            for j in range(len(universe[0])):

                if universe[i][j]:
                    if self.__get_near(universe, (i, j)) not in (2, 3):
                        new_world[i][j] = 0
                        continue
                    new_world[i][j] = 1
                    continue

                if self.__get_near(universe, (i, j)) == 3:
                    new_world[i][j] = 1
                    continue
                new_world[i][j] = 0
        self.world = new_world

    def generate_universe(self) -> UniverseType:
        return [[random.randint(0, 1) for _ in range(self.__width)] for _ in range(self.__height)]

    @staticmethod
    def __get_near(
        universe: UniverseType, pos: CellType, system: CoordinatesType | None = None
    ) -> int:
        if system is None:
            system = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

        count = 0
        for i in system:
            if universe[(pos[0] + i[0]) % len(universe)][(pos[1] + i[1]) % len(universe[0])]:
                count += 1
        return count
