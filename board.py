from copy import deepcopy
from random import randint
from operator import itemgetter

ORD_INT = 96

DEPTH_2_WEIGHT = 1.5
AVERAGE_SCORE_WEIGHT = 1


def calculate_piece_sum(pieces):
    calculated_piece_sum = 0
    for piece in pieces:
        calculated_piece_sum += piece.value
    return calculated_piece_sum


def check_if_a_piece_is_in_a_tile(position, pieces):
    for piece in pieces:
        if (piece.position[0] == position[0]) & (piece.position[1] == position[1]):
            return True
    return False


class Piece:
    def __init__(self, position, value, name):
        self.name = name
        self.position = position
        self.value = value
        self.possible_positions = []


class Pawn(Piece):
    def __init__(self, position, ):
        Piece.__init__(self, position, 1, 'pawn')

    def calculate_possible_positions(self, moved_pieces, enemy_pieces, is_moving_white):
        self.possible_positions.clear()

        direction = 1
        if not is_moving_white:
            direction = direction * (-1)

        normal_move = f'{self.position[0]}{int(self.position[1]) + (1 * direction)}'
        if (not check_if_a_piece_is_in_a_tile(normal_move, moved_pieces)) and (
                not check_if_a_piece_is_in_a_tile(normal_move, enemy_pieces)) and 0 < int(normal_move[1:]) < 9:
            self.possible_positions.append(self.position + normal_move)

        long_move = f'{self.position[0]}{int(self.position[1]) + (2 * direction)}'
        if (not check_if_a_piece_is_in_a_tile(long_move, moved_pieces)) and (not check_if_a_piece_is_in_a_tile(long_move, enemy_pieces)) and\
                (not check_if_a_piece_is_in_a_tile(normal_move, moved_pieces)) and (not check_if_a_piece_is_in_a_tile(normal_move, enemy_pieces)) and \
                ((self.position[1] == 2 and is_moving_white) or (self.position[1] == 7 and (not is_moving_white))) and 0 < int(long_move[1:]) < 9:
            self.possible_positions.append(self.position + long_move)

        right_take = f'{chr(ord(self.position[0]) + 1)}{int(self.position[1]) + (1 * direction)}'
        if check_if_a_piece_is_in_a_tile(right_take, enemy_pieces):
            self.possible_positions.append(self.position + right_take)

        left_take = f'{chr(ord(self.position[0]) - 1)}{int(self.position[1]) + (1 * direction)}'
        if check_if_a_piece_is_in_a_tile(left_take, enemy_pieces):
            self.possible_positions.append(self.position + left_take)

        return self.possible_positions


class Bishop(Piece):
    def __init__(self, position):
        Piece.__init__(self, position, 3, 'bishop')
        self.possible_positions = []

    def check_if_move_is_legal(self, position, pieces):
        if ord(position[0]) - ORD_INT > 8 or ord(position[0]) - ORD_INT < 1 or int(position[1:]) > 8 or int(position[1:]) < 1:
            return False
        else:
            if check_if_a_piece_is_in_a_tile(position, pieces):
                return False
            else:
                return True

    def calculate_possible_positions(self, moved_pieces, enemy_pieces, is_moving_white):
        self.possible_positions.clear()
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) + m)}{int(self.position[1]) + m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) + m)}{int(self.position[1]) - m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) - m)}{int(self.position[1]) + m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) - m)}{int(self.position[1]) - m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        return self.possible_positions


class King(Piece):
    def __init__(self, position):
        Piece.__init__(self, position, 3, 'king')
        self.kings_theoretically_possible_positions = []

    def check_if_move_is_legal(self, position, moved_pieces):
        if len(position) > 2 or ord(position[0]) - ORD_INT > 8 or ord(position[0]) - ORD_INT < 1 or int(position[1]) > 8 or int(position[1]) < 1:
            return False
        else:
            if check_if_a_piece_is_in_a_tile(position, moved_pieces):
                return False
            else:
                return True

    def calculate_possible_positions(self, moved_pieces, enemy_pieces, is_moving_white):
        self.kings_theoretically_possible_positions.clear()
        self.possible_positions.clear()

        self.kings_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 1)}{int(self.position[1]) + 1}')
        self.kings_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 1)}{self.position[1]}')
        self.kings_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 1)}{int(self.position[1]) - 1}')
        self.kings_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 1)}{int(self.position[1] )+ 1}')
        self.kings_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 1)}{self.position[1]}')
        self.kings_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 1)}{int(self.position[1]) - 1}')
        self.kings_theoretically_possible_positions.append(
            f'{self.position[0]}{int(self.position[1]) + 1}')
        self.kings_theoretically_possible_positions.append(
            f'{self.position[0]}{int(self.position[1]) - 1}')

        for position in self.kings_theoretically_possible_positions:
            if self.check_if_move_is_legal(position, moved_pieces):
                self.possible_positions.append(self.position + position)
        return self.possible_positions


class Knight(Piece):
    def __init__(self, position):
        Piece.__init__(self, position, 3, 'knight')
        self.knights_theoretically_possible_positions = []

    def check_if_move_is_legal(self, position, luc4y_pieces):
        if ord(position[0]) - ORD_INT > 8 or ord(position[0]) - ORD_INT < 1 or int(position[1:]) > 8 or int(position[1:]) < 1:
            return False
        else:
            if check_if_a_piece_is_in_a_tile(position, luc4y_pieces):
                return False
            else:
                return True

    def calculate_possible_positions(self, moved_pieces, enemy_pieces, is_moving_white):
        self.knights_theoretically_possible_positions.clear()
        self.possible_positions.clear()

        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 1)}{int(self.position[1]) + 2}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 1)}{int(self.position[1]) - 2}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 2)}{int(self.position[1]) + 1}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) + 2)}{int(self.position[1]) - 1}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 1)}{int(self.position[1]) + 2}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 1)}{int(self.position[1]) - 2}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 2)}{int(self.position[1]) + 1}')
        self.knights_theoretically_possible_positions.append(
            f'{chr(ord(self.position[0]) - 2)}{int(self.position[1]) - 1}')

        for position in self.knights_theoretically_possible_positions:
            if self.check_if_move_is_legal(position, moved_pieces):
                self.possible_positions.append(self.position + position)
        return self.possible_positions


class Rook(Piece):
    def __init__(self, position):
        Piece.__init__(self, position, 5, 'rook')

    @staticmethod
    def check_if_move_is_legal(position, pieces):
        if ord(position[0]) - ORD_INT > 8 or ord(position[0]) - ORD_INT < 1 or int(position[1]) > 8 or int(position[1]) < 1:
            return False
        else:
            if check_if_a_piece_is_in_a_tile(position, pieces):
                return False
            else:
                return True

    def calculate_possible_positions(self, moved_pieces, enemy_pieces, is_moving_white):
        self.possible_positions.clear()

        for x in range(ord(self.position[0]) + 1, 9):
            position = f'{chr(x + ORD_INT)}{self.position[1]}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        for x in range(ord(self.position[0]) - 1, 0, -1):
            position = f'{chr(x + ORD_INT)}{self.position[1]}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        for y in range(int(self.position[1]) + 1, 9):
            position = f'{self.position[0]}{y}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        for y in range(int(self.position[1]) - 1, 0, -1):
            position = f'{self.position[0]}{y}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        return self.possible_positions


class Queen(Piece):
    def __init__(self, position):
        Piece.__init__(self, position, 9, 'queen')

    @staticmethod
    def check_if_move_is_legal(position, pieces):
        if ord(position[0]) - ORD_INT > 8 or ord(position[0]) - ORD_INT < 1 or int(position[1:]) > 8 or int(position[1:]) < 1:
            return False
        else:
            if check_if_a_piece_is_in_a_tile(position, pieces):
                return False
            else:
                return True

    def calculate_possible_positions(self, moved_pieces, enemy_pieces, is_moving_white):
        self.possible_positions.clear()

        #
        # BISHOP MOVES
        #
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) + m)}{int(self.position[1]) + m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) + m)}{int(self.position[1]) - m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) - m)}{int(self.position[1]) + m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        for m in range(1, 8):
            position = f'{chr(ord(self.position[0]) - m)}{int(self.position[1]) - m}'
            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        #
        # ROOK MOVES
        #
        for x in range(ord(self.position[0]) + 1, 9):
            position = f'{chr(x + ORD_INT)}{self.position[1]}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        for x in range(ord(self.position[0]) - 1, 0, -1):
            position = f'{chr(x + ORD_INT)}{self.position[1]}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        for y in range(int(self.position[1]) + 1, 9):
            position = f'{self.position[0]}{y}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break

        for y in range(int(self.position[1]) - 1, 0, -1):
            position = f'{self.position[0]}{y}'

            if self.check_if_move_is_legal(position, moved_pieces):
                if check_if_a_piece_is_in_a_tile(position, enemy_pieces):
                    self.possible_positions.append(self.position + position)
                    break
                else:
                    self.possible_positions.append(self.position + position)
            else:
                break
        return self.possible_positions


class Board:
    def __init__(self, is_luc4y_white):
        self.is_luc4y_white = is_luc4y_white
        self.material_difference = 0

        #   CREATING TILES
        self.tiles = {}
        for x in range(1, 9):
            for y in range(1, 9):
                self.tiles[f'{chr(x + ORD_INT)}{y}'] = {'piece': None, 'controlled_by_luc4y': 0, 'controlled_by_ernst': 0}

        #   CREATING AND ASSIGNING PIECES TO PLAYERS
        white_pieces = {'a1': Rook('a1'), 'b1': Knight('b1'), 'c1': Bishop('c1'), 'd1': Queen('d1'),
                        'e1': King('e1'), 'f1': Bishop('f1'), 'g1': Knight('g1'), 'h1': Rook('h1'),
                        'a2': Pawn('a2'), 'b2': Pawn('b2'), 'c2': Pawn('c2'), 'd2': Pawn('d2'),
                        'e2': Pawn('e2'), 'f2': Pawn('f2'), 'g2': Pawn('g2'), 'h2': Pawn('h2')}

        black_pieces = {'a8': Rook('a8'), 'b8': Knight('b8'), 'c8': Bishop('c8'), 'd8': Queen('d8'),
                        'e8': King('e8'), 'f8': Bishop('f8'), 'g8': Knight('g8'), 'h8': Rook('h8'),
                        'a7': Pawn('a7'), 'b7': Pawn('b7'), 'c7': Pawn('c7'), 'd7': Pawn('d7'),
                        'e7': Pawn('e7'), 'f7': Pawn('f7'), 'g7': Pawn('g7'), 'h7': Pawn('h7')}
        if self.is_luc4y_white:
            self.luc4y_pieces = white_pieces
            self.ernst_pieces = black_pieces
        else:
            self.luc4y_pieces = black_pieces
            self.ernst_pieces = white_pieces

        #   ASSIGNING PIECES TO TILES
        for piece in list(self.luc4y_pieces.values()):
            pos = piece.position
            x = self.tiles[pos]
            x['piece'] = piece
        for piece in self.ernst_pieces.values():
            self.tiles[piece.position]['piece'] = piece

        #   ASSIGNING CONTROL TO TILES
        luc4y_initial_moves = []
        for piece in self.luc4y_pieces.values():
            luc4y_initial_moves.extend(piece.calculate_possible_positions(self.luc4y_pieces.values(), self.ernst_pieces.values(), self.is_luc4y_white))
        ernst_initial_moves = []
        for piece in self.ernst_pieces.values():
            ernst_initial_moves.extend(piece.calculate_possible_positions(self.ernst_pieces.values(), self.luc4y_pieces.values(), not self.is_luc4y_white))

        for luc4y_move in luc4y_initial_moves:
            self.tiles[luc4y_move[2:4]]['controlled_by_luc4y'] += 1
        for ernst_move in ernst_initial_moves:
            self.tiles[ernst_move[2:4]]['controlled_by_ernst'] += 1

    def update_board_state(self, move, is_moving_luc4y):
        start_position = move[0:2]
        end_position = move[2:4]
        from_tile = self.tiles[start_position]
        to_tile = self.tiles[end_position]

        if is_moving_luc4y:
            moved_pieces = self.luc4y_pieces
            enemy_pieces = self.ernst_pieces
        else:
            moved_pieces = self.ernst_pieces
            enemy_pieces = self.luc4y_pieces

        moved_piece = moved_pieces[start_position]
        previous_possible_moves = moved_piece.calculate_possible_positions(moved_pieces.values(), enemy_pieces.values(), (is_moving_luc4y and self.is_luc4y_white) or (not is_moving_luc4y and not self.is_luc4y_white))

        moved_piece.position = end_position

        possible_moves = moved_piece.calculate_possible_positions(moved_pieces.values(), enemy_pieces.values(), (is_moving_luc4y and self.is_luc4y_white) or (not is_moving_luc4y and not self.is_luc4y_white))

        for previous_move in previous_possible_moves:
            if is_moving_luc4y:
                self.tiles[previous_move[2:4]]['controlled_by_luc4y'] -= 1
            else:
                self.tiles[previous_move[2:4]]['controlled_by_ernst'] -= 1

        for move in possible_moves:
            if is_moving_luc4y:
                self.tiles[move[2:4]]['controlled_by_luc4y'] += 1
            else:
                self.tiles[move[2:4]]['controlled_by_ernst'] += 1

        del moved_pieces[start_position]
        moved_pieces[end_position] = moved_piece
        to_tile['piece'] = moved_piece

        from_tile['piece'] = None
        if end_position in enemy_pieces:
            del enemy_pieces[end_position]

    def calculate_pieces_difference_score(self):
        material_difference = calculate_piece_sum(self.luc4y_pieces.values()) - calculate_piece_sum(self.ernst_pieces.values())
        self.material_difference = material_difference
        return material_difference

    def calculate_all_possible_moves(self, calculate_luc4y_moves):

        is_moving_white = (calculate_luc4y_moves and self.is_luc4y_white) or (not calculate_luc4y_moves and not self.is_luc4y_white)
        if calculate_luc4y_moves:
            moved_pieces = self.luc4y_pieces.values()
            enemy_pieces = self.ernst_pieces.values()
        else:
            moved_pieces = self.ernst_pieces.values()
            enemy_pieces = self.luc4y_pieces.values()

        all_possible_moves = []
        for piece in moved_pieces:
            all_possible_moves.extend(piece.calculate_possible_positions(moved_pieces, enemy_pieces, is_moving_white))
        return all_possible_moves

    def calculate_best_move(self):

        all_possible_luc4y_moves_depth_1 = self.calculate_all_possible_moves(True)

        best_score_so_far = self.calculate_pieces_difference_score()
        best_average_score_so_far = -100
        best_move_so_far = all_possible_luc4y_moves_depth_1[randint(0, len(all_possible_luc4y_moves_depth_1) - 1)]

        for lucky_move_depth_1 in all_possible_luc4y_moves_depth_1:
            # print(f'LUC4Y MOVE - {lucky_move_depth_1}')
            current_final_positions_sum = 0.0
            number_of_moves_simulated = 0.0
            worst_score_depth_2 = best_score_so_far

            simulated_board_depth_1 = deepcopy(self)
            simulated_board_depth_1.update_board_state(lucky_move_depth_1, True)
            all_possible_ernst_moves_depth_2 = simulated_board_depth_1.calculate_all_possible_moves(False)

            rated_ernst_moves_depth_2 = []
            for ernst_move_depth_2 in all_possible_ernst_moves_depth_2:
                # print(ernst_move_depth_2)
                simulated_board_depth_2 = deepcopy(simulated_board_depth_1)
                simulated_board_depth_2.update_board_state(ernst_move_depth_2, False)
                simulated_score_depth_2 = simulated_board_depth_2.calculate_pieces_difference_score()
                rated_ernst_moves_depth_2.append({'score': simulated_score_depth_2, 'move': ernst_move_depth_2})

                if simulated_score_depth_2 < worst_score_depth_2:
                    worst_score_depth_2 = simulated_score_depth_2
            rated_ernst_moves_depth_2.sort(key=itemgetter('score'), reverse=True)

            for best_ernst_move_depth_2_index in range(0, 2):
                simulated_board_depth_2 = deepcopy(simulated_board_depth_1)
                simulated_board_depth_2.update_board_state(rated_ernst_moves_depth_2[best_ernst_move_depth_2_index]['move'], False)
                all_possible_luc4y_moves_depth_3 = simulated_board_depth_2.calculate_all_possible_moves(True)

                for lucky_move_depth_3 in all_possible_luc4y_moves_depth_3:
                    simulated_board_depth_3 = deepcopy(simulated_board_depth_2)

                    simulated_board_depth_3.update_board_state(lucky_move_depth_3, True)

                    simulated_score_depth_3 = simulated_board_depth_3.calculate_pieces_difference_score()
                    current_final_positions_sum += simulated_score_depth_3
                    number_of_moves_simulated += 1

            current_average_score = ((current_final_positions_sum / number_of_moves_simulated)*AVERAGE_SCORE_WEIGHT) + (worst_score_depth_2*DEPTH_2_WEIGHT)
            print(f'CURRENT BEST AVRG SCR - {current_average_score} = {current_final_positions_sum} / {number_of_moves_simulated}')
            if current_average_score > best_average_score_so_far:
                best_move_so_far = lucky_move_depth_1
                best_average_score_so_far = current_average_score

        # print(best_score_so_far)
        print(f'BEST AVERAGE SCORE - {best_average_score_so_far}')
        return best_move_so_far
