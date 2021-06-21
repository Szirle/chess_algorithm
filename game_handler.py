from board import Board


class GameHandler:
    def __init__(self, is_white, game_id, client, is_game_played_from_the_start):
        self.is_white = is_white
        self.game_ID = game_id
        self.client = client
        self.is_luc4y_turn = True

        self.all_possible_moves = None
        self.current_board = Board(self.is_white)

        if is_white and is_game_played_from_the_start:
            self.move('d2d4')

    def update(self, move):
        if self.is_luc4y_turn:
            self.current_board.update_board_state(move, False)
            self.all_possible_moves = self.current_board.calculate_all_possible_moves(True)
            # for move in self.all_possible_moves:
            #     print(f'POSSIBLE MOVE - {move}')
            move = self.current_board.calculate_best_move()
            self.move(move)
        else:
            self.is_luc4y_turn = True

    def move(self, move):
        try:
            self.client.bots.make_move(self.game_ID, move)
            self.current_board.update_board_state(move, True)
            self.is_luc4y_turn = False
        except Exception as e:
            print(f'\nSORRY! I TRIED WRONG MOVE - {e}')
            self.iterate_through_moves_until_there_is_legal(self.all_possible_moves)

    def iterate_through_moves_until_there_is_legal(self, all_possible_moves):
        print(all_possible_moves)
        for move in all_possible_moves:
            try:
                self.client.bots.make_move(self.game_ID, move)
                self.current_board.update_board_state(move, True)
                self.is_luc4y_turn = False
                print(f'{move} - WENT GREAT\n')
                break
            except:
                print(f'{move} - WENT WRONG\n')
                continue
