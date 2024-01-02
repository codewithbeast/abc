import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import chessdotcom

from flask import redirect, render_template, session
from functools import wraps
from chessdotcom import Client , get_player_stats
import requests
import chess
import chess.pgn
from io import StringIO


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_blitz(name):
    Client.request_config["headers"]["User-Agent"] = (
   "My Python Application. "
   "Contact me at ossvasi2020@gmail.com"
    )

    response = get_player_stats(name)
    blitz_rating = response.stats.chess_blitz.last.rating

    return blitz_rating

def get_rapid(name):
    Client.request_config["headers"]["User-Agent"] = (
   "My Python Application. "
   "Contact me at ossvasi2020@gmail.com"
    )

    response = get_player_stats(name)
    rapid_rating = response.stats.chess_rapid.last.rating

    return rapid_rating

def get_bullet(name):
    Client.request_config["headers"]["User-Agent"] = (
   "My Python Application. "
   "Contact me at ossvasi2020@gmail.com"
    )

    response = get_player_stats(name)
    bullet_rating = response.stats.chess_bullet.last.rating

    return bullet_rating


def pgn_to_fen(pgn_text):
    # Create a new chess board
    board = chess.Board()
    

    # Load the PGN
    pgn_game = chess.pgn.read_game(StringIO(pgn_text))

    # Iterate through the moves in the game
    for move in pgn_game.mainline_moves():
        board.push(move)

    # Get the resulting FEN after all moves
    fen = board.fen()
    return fen


def get_puzzle_by_id(puzzle_id):
    api_token = 'lip_bF9mqGx9ys7ElQbuSe9Z'
    headers = {'Authorization': f'Bearer {api_token}'}

    # Example: Get information about a specific puzzle by ID
    url = f'https://lichess.org/api/puzzle/{puzzle_id}'
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        puzzle_data = response.json()
        # fen 
        pgn = puzzle_data["game"]["pgn"]
        sol = puzzle_data["puzzle"]["solution"]
        fen = pgn_to_fen(pgn)

        return fen,sol
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return 1


def check_move(fen):
    board = chess.Board(fen=fen)

    return "w" if board.turn == chess.WHITE else "b"