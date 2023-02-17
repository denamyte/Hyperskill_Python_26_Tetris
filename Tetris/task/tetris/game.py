from board import Board


def main():
    fg_name = input()
    board = Board(*[int(x) for x in input().split()])
    print()
    prn(board)
    board.put_figure(fg_name)
    prn(board)
    while (cmd := input()) != 'exit':
        print()
        match cmd:
            case 'rotate':
                board.rotate()
            case c if c in ['left', 'right']:
                board.move(c)
            case 'down':
                board.down()

        prn(board)


def prn(b: Board):
    print(b, '', sep='\n')


if __name__ == '__main__':
    main()
