
from flask import make_response, abort
from models import db, Game, GameSchema, Mark, MarkSchema


def get_version():
    return {"version": 1.0}


def create_game():
    schema = GameSchema()
    new_game = Game(winner=None, is_over=False, current_player='X', grid='_________' )

    db.session.add(new_game)
    db.session.commit()

    body = schema.dump(new_game)

    return body, 201


def get_game(game_id):

    game = Game.query.filter(Game.game_id == game_id).one_or_none()

    if game:
        schema = GameSchema()
        body = schema.dump(game)
        return body

    else:
        abort(404, "Game not found")

def place_mark(game_id, mark):

    # Retrieve the game to be updated
    game = Game.query.filter(Game.game_id == game_id).one_or_none()

    if game:
        index = 3*mark['row'] + mark['col']
        updated_grid = list(game.grid)
        updated_grid[index]=mark['player']
        game.grid = ''.join(updated_grid)

        schema = GameSchema()

        db.session.commit()

        body = schema.dump(game)


        return body, 200

    else:
        abort(404, "Game not found")
