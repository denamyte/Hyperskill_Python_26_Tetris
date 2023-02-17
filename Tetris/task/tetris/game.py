from board import Board


def main():
    piece_name = input()
    board = Board(*[int(x) for x in input().split()])
    print()
    prn(board)
    board.put_piece(piece_name)
    prn(board)
    while (cmd := input()) != 'exit':
        print()
        match cmd:
            case 'rotate':
                board.rotate()
            case c if c in ['left', 'right']:
                board.shift(c)
            case 'down':
                board.move_down()

        prn(board)


def prn(b: Board):
    print(b, '', sep='\n')


if __name__ == '__main__':
    main()
