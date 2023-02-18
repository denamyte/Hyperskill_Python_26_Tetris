import copy
from typing import List, Callable

import numpy as np

PIECES = {
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


class Piece:
    ADDED_HEIGHT = 4

    def __init__(self, name: str, w: int, h: int):
        self._name = name
        self._w = w
        self._h = h + self.ADDED_HEIGHT
        self._rotate = 0
        self._arrays: List[np.ndarray] = self._ini_transform_into_arrays(PIECES[name])

    def _ini_transform_into_arrays(self, lists: List[List[int]]) -> List[np.ndarray]:
        arrays = []
        for lst in lists:
            array = np.array([[0] * self._w] * self._h)
            for num in lst:
                array[divmod(num, self._w)] = 1
            arrays.append(array)
        return arrays

    def shift_w(self, shift: int) -> 'Piece':
        permutation = [(n + self._w - shift) % self._w for n in range(self._w)]
        self._arrays = [a[:, permutation] for a in self._arrays]
        return self.move_down()

    def rotate(self) -> 'Piece':
        self._rotate = (self._rotate + 1) % len(self._arrays)
        return self.move_down()

    def move_down(self) -> 'Piece':
        for a in self._arrays:
            for row_num in range(self._h - 1, 0, -1):
                a[row_num] = a[row_num - 1]
            a[0] = np.array([0] * self._w)
        return self

    @property
    def state(self) -> np.ndarray:
        return self._arrays[self._rotate]

    @property
    def copy(self) -> 'Piece':
        other = copy.copy(self)
        other._arrays = [np.copy(a) for a in self._arrays]
        return other

    @property
    def consistent(self) -> bool:
        a = self.state
        left_sum = a[:, 0].sum()
        right_sum = a[:, -1].sum()
        bottom_sum = a[self._h - self.ADDED_HEIGHT].sum()
        return not ((left_sum and right_sum) or bottom_sum)

    def line_busy(self, row_num: int) -> bool:
        return np.amax(self.state[row_num]) > 0


class Board:
    def __init__(self, w: int, h: int):
        self._w = w
        self._h = h
        self._array = np.array([[0] * w] * h)
        self._array_bgr = self._array
        self._piece: Piece | None = None
        self._game_over = False

    def _bg_render(self):
        """
        Make a copy from the static array and paint the current piece on it
        """
        self._array_bgr = self._array if not self._piece \
            else np.add(self._array, self._piece.state[:self._h])

    def put_piece(self, piece_name: str):
        if not self._piece:
            self._after_move_check(Piece(piece_name, self._w, self._h), False)

    def rotate(self):
        if self._piece:
            self._after_move_check(self._piece.copy.rotate())

    def shift(self, shift: str):
        if self._piece:
            self._after_move_check(self._piece.copy.shift_w(MOVE_MAP[shift]))

    def move_down(self):
        if self._piece:
            self._after_move_check(self._piece.copy.move_down(), False)

    def break_(self):
        for row_num in range(self._h):
            if np.sum(self._array[row_num]) == self._w:
                for row_num2 in range(row_num, 0, -1):
                    self._array[row_num2] = self._array[row_num2 - 1]
                self._array[0] = np.array([0] * self._w)
        self._bg_render()

    def _after_move_check(self, test_piece, move_down=True):
        if test_piece.consistent:
            self._piece = test_piece
            self._bg_render()
            if not self._piece_may_fall:
                # applying the piece to the static board
                self._array = np.add(self._array, self._piece.state[:self._h])
                self._piece = None
                # check if the upper line of the board is filled
                if np.sum(self._array[0]):
                    self._game_over = True
        elif move_down:
            self.move_down()

    @property
    def _piece_may_fall(self) -> bool:
        """ Check if the piece can move at least one line down """
        if not self._piece:
            return True
        for row_num in range(self._h):
            if self._piece.line_busy(row_num):
                if row_num == self._h - 1:
                    return False
                comb = np.add(self._piece.state[row_num],
                              self._array[row_num + 1])
                if np.amax(comb) > 1:
                    return False
        return True

    @property
    def game_over(self) -> bool:
        return self._game_over

    def __str__(self):
        return '\n'.join(' '.join(SYM_MAP[num] for num in row)
                         for row in self._array_bgr)
