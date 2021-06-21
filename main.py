import berserk
import threading
from game_handler import GameHandler

token = "xMHDqHckmSa0kDyn"
#            |
#            |
#           \/
game_id = "Wt1J6Ayk"
#           /\
#           |
#           |


class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
        self.number_of_moves = 0
        self.is_game_played_from_the_start = True

        try:
            if self.current_state['white']['id'] == 'luc4y':
                is_white = True
            else:
                is_white = False
        except:
            is_white = False

        moves_string = self.current_state['state']['moves']

        if len(moves_string) > 2:
            # GAME ALREADY STARTED / NOT MY TURN - solution to the problem when white moves before luc4y is online
            moves_list = self.current_state['state']['moves'].split(' ')
            print(f'PLAYING A GAME ALREADY STARTED: MOVES DONE - {len(moves_list)}')
            self.is_game_played_from_the_start = False
            self.game_handler = GameHandler(is_white, game_id, client, self.is_game_played_from_the_start)
            self.game_handler.update(moves_list[-1])
        else:
            # PLAYING A GAME FROM THE START / MY TURN
            print('PLAYING A GAME FROM THE START')
            self.game_handler = GameHandler(is_white, game_id, client, self.is_game_played_from_the_start)

    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    def handle_state_change(self, game_state_event):
        moves_list = game_state_event['moves'].split(' ')
        self.number_of_moves = len(moves_list)
        print(f"MOVE NO. {(self.number_of_moves + 1)//2}: {moves_list[-1]}")
        self.game_handler.update(moves_list[-1])

    def handle_chat_line(self, chat_line):
        pass


session = berserk.TokenSession(token)
client = berserk.Client(session)
client.account.get()

random_game = Game(client, game_id)
random_game.start()