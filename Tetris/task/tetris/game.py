from board import Board


def main():
    board = Board(*[int(x) for x in input().split()])
    prn(board)
    while (cmd := input()) != 'exit':
        match cmd:
            case 'piece':
                board.put_piece(input())
            case 'rotate':
                board.rotate()
            case c if c in ['left', 'right']:
                board.shift(c)
            case 'down':
                board.move_down()
            case 'break':
                board.break_()

        prn(board)

        if cmd != 'piece' and board.game_over:
            print('Game Over!')
            break


def prn(b: Board):
    print(b, '', sep='\n')


if __name__ == '__main__':
    main()
