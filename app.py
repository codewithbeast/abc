import os,random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required , get_bullet , get_blitz , get_rapid , get_puzzle_by_id , check_move
from fen_reader import init
import chess

# Configure application
app = Flask(__name__)



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chess.db")
puzzle_db = SQL("sqlite:///puzzle.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/",methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        username = request.form.get("username")

        try:
            blitz = get_blitz(username)
            rapid = get_rapid(username)
            bullet = get_bullet(username)

        except:
            return apology("An error has occured")
        
        return render_template("index.html",blitz=blitz,rapid=rapid,bullet=bullet)

    else:
        return render_template("index.html")
    

@app.route("/login",methods=["GET","POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Username Not Provided ):")
        
        if not request.form.get("password"):
            return apology("Password Not Provided ):")

        rows = db.execute("SELECT * FROM users WHERE username = ?",request.form.get("username"))

        if len(rows)!=1 or not check_password_hash(rows[0]["hash"],request.form.get("password")):
            return apology("Incorrect Password ):")
        
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        
        if not request.form.get("username"):
            return apology("Username Not Provided ):")
        
        if not request.form.get("password"):
            return apology("Password Not Provided ):")
        
        name = db.execute("SELECT username FROM users WHERE username = ? ",request.form.get("username"))

        if len(name)!=0:
            return apology("Username Already Taken ):")
        
        db.execute("INSERT INTO users (username,hash) VALUES(?,?)",request.form.get("username"),generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?",request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect("/")


    else:
        return render_template("register.html")
    
@app.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect("/login")

@app.route("/puzzle",methods=["GET","POST"])
@login_required
def puzzle():
    if request.method == "GET":
        return render_template("puzzle.html")
    
    else:
        id = request.form.get("puzzle_id")
        data = get_puzzle_by_id(id)
        fen = data[0]
        sol = data[1]

        # Add puzzle to database 

        rows = puzzle_db.execute("SELECT * FROM puzzle WHERE id = ?",id)

        if len(rows)==0:
            puzzle_db.execute("INSERT INTO puzzle (puzzle_id) VALUES(?)",id)

        session['puzzle_solution'] = sol
        session['fen'] = fen
        session['move_no'] = 0
        

        init_data = init(fen)
        board = init_data[2]

        
        move = check_move(fen)

        return render_template("board.html",board=board,move=move)
    
@app.route("/puzzle_data_base")
@login_required
def puzzle_data_base():
    rows = puzzle_db.execute("SELECT * FROM puzzle")
    
    if len(rows)==0:
        return apology("Database is empty ):")
    
    index = random.randint(0,len(rows)-1)
    id = rows[index]["puzzle_id"]

    data = get_puzzle_by_id(id)
    fen = data[0]
    sol = data[1]

    session['puzzle_solution'] = sol
    session['fen'] = fen
    session['move_no'] = 0
    

    init_data = init(fen)
    board = init_data[2]

    
    move = check_move(fen)

    return render_template("board.html",board=board,move=move)
        


@app.route("/puzzle_response",methods=["GET","POST"])

@login_required

def puzzle_response():
    
    binary = {"w":0,"b":1}
    if request.method == "POST":
        solution = session["puzzle_solution"]
    
        turn = check_move(session['fen'])
        board1 = chess.Board(fen=session['fen'])
        
        white_moves = []
        black_moves = []

        for i in range(len(solution)):
            if turn == 'w':
                if i%2 == 0:
                    white_moves.append(solution[i])

                else:
                    black_moves.append(solution[i])

            else:
                if i%2 == 0:
                    black_moves.append(solution[i])

                else:
                    white_moves.append(solution[i])


        user_solution = []
        
        move = request.form.get("sol")

        if turn == 'w':
            if move == white_moves[session['move_no']]:     
                user_solution.append(move)
                board1.push(chess.Move.from_uci(move))

                try:
                    board1.push(chess.Move.from_uci(black_moves[session['move_no']]))
                
                except:
                    db.execute("UPDATE users SET correct = correct+1 WHERE id = ?",session["user_id"])
                    return render_template("correct.html")
                
                session['fen'] = board1.fen()

                data = init(session['fen'])
                board = data[2]
                
                
                session['move_no']+=1

            else:
                db.execute("UPDATE users SET incorrect = incorrect+1 WHERE id = ?",session["user_id"])
                return render_template("incorrect.html")

        else:
            if move == black_moves[session['move_no']]:
       
                user_solution.append(move)
                board1.push(chess.Move.from_uci(move))
                session['fen'] = board1.fen()
                try:
                    board1.push(chess.Move.from_uci(white_moves[session['move_no']]))

                except:
                    return render_template("correct.html")

                session['fen'] = board1.fen()

                data = init(session['fen'])
                board = data[2]
                try:
                    opp_move = white_moves[session['move_no']]

                except:
                    return render_template("correct.html")
                
                session['move_no']+=1

            else:
                return render_template("incorrect.html")

        return render_template("board.html",board=board)


    else:
        return redirect("/puzzle")
    
@app.route("/puzzle_stats")
def puzzle_stats():
    correct_puzzles = db.execute("SELECT correct FROM users WHERE id = ?",session["user_id"])[0]["correct"]
    incorrect_puzzles = db.execute("SELECT incorrect FROM users WHERE id = ?",session["user_id"])[0]["incorrect"]
    total_puzzles = int(correct_puzzles+incorrect_puzzles)

    correct_percentage = float(correct_puzzles/total_puzzles)*100
    incorrect_percentage = float(incorrect_puzzles/total_puzzles)*100

    return render_template("puzzle_stats.html",correct_puzzles=correct_puzzles,incorrect_puzzles=incorrect_puzzles,total_puzzles=total_puzzles,correct_percentage=correct_percentage , incorrect_percentage=incorrect_percentage)