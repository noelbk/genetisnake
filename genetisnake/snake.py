import logging

from . import snake_board

LOG = logging.getLogger(__name__)

class GenetiSnake(object):
    ARITY = 6 # number of arguments my decision function takes
    
    def __init__(self, move_func):
        self.move_func = move_func
        self.games = 0
        self.turns = 0

    def move(self, game, board, self_index):
        board_id = game.snakes[self_index].board_id
        self_head = game.snakes[self_index].body[0]
        self_health = game.snakes[self_index].health
        
        food_smell,   _food_max = board.smell_food(board_id)
        enemy_smell, _enemy_max = board.smell_enemy(board_id)

        LOG.debug("snake.move board_id=%s head=%s health=%s", board_id, board.coords(self_head), self_health)

        max_move = board.moves[0]
        max_score = None

        max_moves = float(board.width + board.height)
        max_space = float(board.width * board.height)
        
        for move_pos, move in board.neighbours(self_head):
            if not snake_board.CellTypeSnake.can_move(board[move_pos]):
                continue
            space_cone, _space_smell_cone = board.smell_space_cone(board_id, self_head, move.name)
            space_all, _space_smell_all = board.smell_space_all(board_id, move_pos)
            # the number of arguments here is self.ARITY
            score = self.move_func(
                float(self_health) / game.MAX_HEALTH,
                float(food_smell[move_pos]) / max_moves,
                float(enemy_smell[move_pos]) / max_moves,
                float(space_cone) / max_space,
                float(space_all) / max_space,
                0,
                )

            LOG.debug("snake.move board_id=%s pos=%s move=%s score=%s"
                      " food=%s enemy=%s",
                      board_id, board.coords(move_pos), move.name, score,
                      food_smell[move_pos], enemy_smell[move_pos])

            if max_score is None or score > max_score:
                max_score = score
                max_move = move
                
        LOG.debug("snake.move self_index=%s best move=%s score=%s", self_index, max_move.name, max_score)
        return max_move.name
        
