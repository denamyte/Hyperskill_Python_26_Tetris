from typing import List

import numpy as np

FIGURES = {
    'O': [[4, 14, 15, 5]],
    'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
    'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
    'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
    'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
    'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
    'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
}

SYM_MAP = ['-', '0']
MOVE_MAP = {'left': -1,
            'right': 1}


class Figure:
    def __init__(self, name: str, w: int, h: int):
        self._w = w
        self._h = h + 4
        self._rotate = 0
        self.arrays: List[np.ndarray] = self._ini_transform_into_arrays(FIGURES[name])

    def _ini_transform_into_arrays(self, lists: List[List[int]]) -> List[np.ndarray]:
        arrays = []
        for lst in lists:
            array = np.array([[0] * self._w] * self._h)
            for num in lst:
                array[divmod(num, self._w)] = 1
            arrays.append(array)
        return arrays

    def shift_w(self, shift: int):
        permutation = [(n + self._w - shift) % self._w for n in range(self._w)]
        self.arrays = [a[:, permutation] for a in self.arrays]
        self.move_down()

    def rotate(self):
        self._rotate = (self._rotate + 1) % len(self.arrays)
        self.move_down()

    def move_down(self):
        for a in self.arrays:
            for row_num in range(self._h - 1, 0, -1):
                a[row_num] = a[row_num - 1]
            a[0] = np.array([0] * self._w)

    @property
    def state(self) -> np.ndarray:
        return self.arrays[self._rotate]


class Board:
    def __init__(self, w: int, h: int):
        self._w = w
        self._h = h
        self.array = np.array([[0] * w] * h)
        self.array_f = self.array  # the copy for rendering with the current figure
        self.figure: Figure | None = None

    def put_figure(self, fg_name: str):
        self.figure = Figure(fg_name, self._w, self._h)
        self._bg_render()

    def _bg_render(self):
        """
        Make a copy from the static array and paint the current figure on it
        """
        self.array_f = np.copy(self.array)
        figure = self.figure.state
        for row_num in range(self._h):
            self.array_f[row_num] = figure[row_num]

    def rotate(self):
        self.figure.rotate()
        self._bg_render()

    def move(self, shift: str):
        self.figure.shift_w(MOVE_MAP[shift])
        self._bg_render()

    def down(self):
        self.figure.move_down()
        self._bg_render()

    def __str__(self):
        return '\n'.join(' '.join(SYM_MAP[num] for num in row)
                         for row in self.array_f)
