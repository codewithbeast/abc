symbols = {"r":"BR",
           "n":"BN",
           "b":"BB",
           "q":"BQ",
           "k":"BK",
           "p":"BP",
        
           "R":"WR",
           "N":"WN",
           "B":"WB",
           "Q":"WQ",
           "K":"WK",
           "P":"WP"}






def init(fen_string):
    board = []
    move = ""
    castling = ""
    for i in range(len(fen_string)):
        if (fen_string[i] == " "):
            return i+3,fen_string[i+1],board
        try:
            x = int(fen_string[i])
            for i in range(x):
                board.append(' ')

        except:
            if(fen_string[i]!="/"):
                board.append(symbols[fen_string[i]])

    return board

      
