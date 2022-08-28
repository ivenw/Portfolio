from board import Board
from game_state import GameState
from window import Window

BOARD_WIDTH = 36
BOARD_HEIGHT = 15


def main():
    window = Window(BOARD_WIDTH, BOARD_HEIGHT)
    game_state = GameState(Board(BOARD_WIDTH, BOARD_HEIGHT))
    window.flash(game_state.board)

    while True:
        while game_state.player_has_valid_move:
            window.draw_board(game_state.board, game_state.score)
            player_direction_input = window.get_player_input()
            game_state.update(player_direction_input)

        window.draw_game_over()
        if not window.continue_playing():
            break

        game_state = GameState(Board(BOARD_WIDTH, BOARD_HEIGHT))
        window.flash(game_state.board)

    window.close()


if __name__ == "__main__":
    main()
