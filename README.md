# CHESS TRAINER
#### Video Demo:  <URL HERE>
#### Description:   

Chess Trainer is a website made in flask designed for chess enthusiasts who want to improve their tactics lets take a look at each file and it's functions. 

1. apology.html - Apology.html provides an apology if there is a runtime error for example the user submits the login form but he/she forgot the provide the password i can use the apology functions as follows- apology("Password not provided :C") it takes 2 arguments a error message and an error code (default error code is 400). 


2. board.html - board.html represents a chessboard(a 1d array in an 8*8 grid) which makes it easier for the user to look at the position it also contains a form where the user submits the solution to the puzzle. 

3. correct.html - correct.html is a message which is displayed if the user solves the puzzle correctly.

4. incorrect.html - incorrect.html is a message which is displayed if the user solves the puzzle incorrectly. 

5. index.html  - index.html is the homepage where the user can access his chess.com stats like his 
blitz_rating rapid_rating etc. 

6. layout.html - layout.html is the basic structure of a page it contains a navbar which displays buttons which redirect to differnt routes (the navbar depends on weather the user has logged in or not). 

7. login.html - login.html contains a form which the user submits to login. 
8. puzzle_stats.html - puzzle_stats.html displays the data of the user related to his puzzles like how total puzzles attempted , total correct , total incorrect , correct percentage , incorrect percentage etc. 

9. fen_reader.py - it contains an init function which takes a fen string as an argument and returns a 1d array represnting a chess board 

10. puzzle.html - puzzle.html is a form which takes the puzzle_id as input from the user.
11. register.html - register.html contains a form which the user submits to register(creating a new account). 
12. app.py

13. helpers.py 
14. chess.db 
15. puzzle.db 



app.py contains 8 routes 
1. "/" - "/" is the homepage where the user can enter his chess.com username and get his rating. 

2. "/login" - "/login" is the route which logs the user in it first gets the username and password enterd in the form (if not any it return an apology) then it querys the database to get the data of the user then it checks weather the provided user exists and the password is valid if yes then it logs the user in if no then it returns an apology if the user is redirected to the login route (Through GET method) it renders the login form. 

3. "/register" - "/register" is the register page where the user can create a new account it accepts 2 methods GET,POST if the user it redirected to the page throught GET it renders the registration form but if the user is there by the POST method (the user submits a form) it checks weather the username doesnt not exists if yes then it returns an apology but if not then it checks the password and the password conformation if they dont match then it returns an apology if not it logs the user and redirects him/her to the homepage ("/" route). 

4. "/logout" - "/logout" this route is pretty simple it just logs the user out by clearing his/her session object.

5. "/puzzle" - "/puzzle" this route is responsible for getting the puzzle id provided by the user and rendering it in an html it first gets the puzzle_id and checks weather it's valid or not if no then it returns an apology if yes then it querys the puzzles database to check weather if the puzzle exists in the databse or not if yes then it adds the puzzle id provided by the user to the puzzle database if not then it renders the board and a form to submit the soution.

6. "/puzzle_data" - "/puzzle_data" this route is pretty simmilar to "/puzzle" only differnce is it only accepts the GET method what it does is it  gets a random puzzle from the databse (if the databse is not empty) and renders it in board.html it renders the board and a form to submit the solution. 

7. "/puzzle_response" - "/puzzle_response" this route is responsible for handling the user's solution of the puzzle it first checks weather all the fields have a move in it or not if not it returns an apology if yes then it checks the user_solution with the actual_solution(provided by the /puzzle and /puzzle_data routes which is stored in the session object) if the user_solution matches with the actual_solution then it renders correct.html else it renders incorrect.html 

8. "/puzzle_stats" - and finally  "/puzzle_sats" this route is responsible of calculating the stats like total puzzles solved correct percentage etc it calculates these 5 things correct_puzzles , incorrect_puzzles , total_puzzles(total puzzles attempted) , correct_percentage , incorrect_percentage and renders it in an html (using jinja).



helpers.py contains 8 functions 

1. apology -  apology function returns an apology it takes 2 arguments message , code(default error code is 400) it is used to render apologies when user input is not expected like blank password while logging in.

2. login_required(decorated function) - login_required decorates function to require login like there are some features which i dont want the user to be acessing without login so i decorate those functions with @login_required.

3. get_blitz , get_rapid , get_bullet - get_blitz , get_rapid , get_bullet take username as an arugment and querys the chess.com api and returns the blitz , rapid , bullet rating accordingly. 

4. pgn_to_fen - pgn_to_fen this function takes pgn_text as an argument plays all the move on a chess board  generates the fen and returns the fen.

5. get_puzzle_by_id - get_puzzle_by_id this takes the puzzle id as an arugment querys the lichess api if sucessfull (response.staus.code = 200) it returns data related to the puzzle like the pgn , solution etc if not it returns 1 and prints the exception

6. check_move - the check_move function takes a fen string as an argument and returns whose turn is it. 

chess.db contains data related to users like their 

1. password_hash 
2. username 
3. id 
4. correct(correct puzzes) 
5. incorrect(incorrect puzzle)  

this database makes it easier to manage users. this is the schema of chess.db CREATE TABLE sqlite_sequence(name,seq); CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, correct NUMERIC NOT NULL DEFAULT 0 ,incorrect NUMERIC NOT NULL DEFAULT 0); 

puzzle.db contains

1. puzzle_ids of various puzzles given by the users schema of puzzle.db CREATE TABLE puzzle (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, puzzle_id TEXT NOT NULL);  CREATE TABLE sqlite_sequence(name,seq); THIS WAS CS50X
