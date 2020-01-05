from chess.game.ChessGame import ChessGame
from chess.game.Config import Config


game_dict = {
                0: "./static/configs/standard_chess_cfg.json", 
                1: "./static/configs/weak_chess_cfg.json",
                2: "./static/configs/endgame_chess_cfg.json"
            }

players_dict = {0: 
                    {
                        0: "minimax", 
                        1: "alpha_beta_prunning", 
                        2: "reinforcement_learning"}, 
                1: {
                        
                }}

strategy_dict = {0: "minimax"}


def setup(game, players, strategy):



def get_board():
    chess_config = Config("./static/configs/standard_chess_cfg.json")
    chess = ChessGame(chess_config)
    return chess.render()


if __name__ == '__main__':
    print(get_board())
