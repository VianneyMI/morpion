
from flask import abort
from models import db, Game, GameSchema, Player


def get_version():
    """Returns version of the API"""

    return {"version": 1.0}


def create_game():
    """Creates a new game"""

    schema = GameSchema()
    new_game = Game(winner=None, is_over=False, current_player='X', grid='_________' )

    db.session.add(new_game)
    db.session.commit()

    body = schema.dump(new_game)

    return body, 201


def get_game(game_id):
    """Retrieves a game from the database"""

    game = Game.query.filter(Game.game_id == game_id).one_or_none()

    if game:

        schema = GameSchema()
        body = schema.dump(game)
        return body.data # BUG: ? I am not sure why without the .data,
                         #the api crashes here while it works fine below <VM, 16/05/21

    else:
        abort(404, "Game not found")

def place_mark(game_id, mark):
    """Places mark"""

    # Retrieve the game to be updated
    game = Game.query.filter(Game.game_id == game_id).one_or_none()

    if game:
        index = 3*mark['row'] + mark['col']
        updated_grid = list(game.grid)
        # Check if coup is allowed

        if updated_grid[index]=='_' and game.current_player.value==mark['player']:
            updated_grid[index]=mark['player']
        else:
            abort(400,"Invalid input or Can't place mark here")
        game.grid = ''.join(updated_grid)

        gameover, winner = is_gameover(game.grid,mark)

        if gameover:
            game.is_over = True
            if winner:
                game.winner = winner

        # Switch current_player
        if game.current_player.value == 'X':

            game.current_player = Player.O
        else:
            game.current_player = Player.X

        # Updating database
        schema = GameSchema()
        db.session.commit()
        body = schema.dump(game)

        return body, 200

    else:
        abort(404, "Game not found")

def is_gameover(grid:str, mark)->(bool,str):
    """Checks if the game is over either with a winner or because the grid is full"""

    winner, player = has_winner(grid,mark)
    if winner:
        return True, player

    complete = is_complete(grid)
    if complete:
        return True, None
    else:
        return False, None


def has_winner(grid:str, mark)->(bool,str):
    """Checks if the game has a winner after a given coup"""

    winner = True

    # Checking row
    for j in range(3):
        index = to_index(mark['row'],j)
        winner = winner and grid[index]==mark['player']

    if not winner:
        # Checking column
        winner = True
        for i in range(3):
            index = to_index(i,mark['col'])
            winner = winner and grid[index]==mark['player']

    if not winner:
        # Checking diagonals if necessary
        index = to_index(mark['row'],mark['col'])
        if index%2 == 0:
            winner = grid[2]==grid[4]==grid[6]==mark['player'] or grid[0]==grid[4]==grid[8]==mark['player']
            #There are only 2 diagonals on indexes 0,2,4 and 0,4, 8
                # 0 1 2
                # 3 4 5
                # 6 7 8

    # Return
    return (winner, mark['player'])

def is_complete(grid:str)->bool:
    """Checks if grid is full"""

    complete = True
    for crc in grid:
        if crc == '_':
            complete = False
    return complete

def to_index(row:int,col:int)->int:
    """Flatten coordinates"""

    return 3*row + col
