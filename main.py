from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


class ChessGame:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP"] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ["wP"] * 8,
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.lastClicked = None
        self.whiteToMove = True
        self.checkmate = False
        self.stalemate = False
        self.isCapture = False
        self.isCheck = False
        self.isDoubleCheck = False
        self.movelog = []
        self.whiteCanCastleKingside = True
        self.whiteCanCastleQueenside = True
        self.blackCanCastleKingside = True
        self.blackCanCastleQueenside = True

        
    def move_piece(self, row, col, newRow, newCol, promotion_choice=None):
        castle = ""
        piece = self.get_piece(row, col)
        newSquare = self.get_piece(newRow, newCol)
        self.board[newRow][newCol] = self.board[row][col]
        self.board[row][col] = None
        if piece == "wK" or piece == "bK":
            if (row, col) == (7, 4) and (newRow, newCol) == (7, 6):
                self.board[7][5] = self.board[7][7]
                self.board[7][7] = None
                castle = "Kingside"
            elif (row, col) == (7, 4) and (newRow, newCol) == (7, 2):
                self.board[7][3] = self.board[7][0]
                self.board[7][0] = None
                castle = "Queenside"

            elif (row, col) == (0, 4) and (newRow, newCol) == (0, 6):
                self.board[0][5] = self.board[0][7]
                self.board[0][7] = None
                castle = "Kingside"
            elif (row, col) == (0, 4) and (newRow, newCol) == (0, 2): 
                self.board[0][3] = self.board[0][0]
                self.board[0][0] = None
                castle = "Queenside"

        if piece == "wK":
            self.whiteCanCastleKingside = False
            self.whiteCanCastleQueenside = False
        elif piece == "bK":
            self.blackCanCastleKingside = False
            self.blackCanCastleQueenside = False
        elif piece == "wR":
            if row == 7 and col == 0:
                self.whiteCanCastleQueenside = False
            elif row == 7 and col == 7:
                self.whiteCanCastleKingside = False
        elif piece == "bR":
            if row == 0 and col == 0:
                self.blackCanCastleQueenside = False
            elif row == 0 and col == 7:
                self.blackCanCastleKingside = False
                    
        if piece == "wP" and newRow == 0:
            self.board[newRow][newCol] = "w" + (promotion_choice)
        elif piece == "bP" and newRow == 7:
            self.board[newRow][newCol] = "b" + (promotion_choice)
                
        if (newRow, newCol) == (0,0):
            self.blackCanCastleQueenside = False
        elif (newRow, newCol) == (0,7):
            self.blackCanCastleKingside = False
        elif (newRow, newCol) == (7,0):
            self.whiteCanCastleQueenside = False
        elif (newRow, newCol) == (7,7):
            self.whiteCanCastleKingside = False

        self.whiteToMove = not self.whiteToMove
        self.movelog_builder(piece, col, newSquare, newRow, newCol, castle, promotion_choice)

    def col_to_letter(self, col):
        match(col):
            case 0:
                return "a"
            case 1:
                return "b"
            case 2:
                return "c"
            case 3:
                return "d"
            case 4:
                return "e"
            case 5:
                return "f"
            case 6:
                return "g"
            case 7:
                return "h"
                
    def movelog_builder(self, piece, col, newSquare, newRow, newCol, castle, promotion_choice = None):
        self.isCapture = False
        self.isCheck = False
        self.isDoubleCheck = False
        
        if self.is_checkmate():
            self.checkmate = True
    
        if newSquare is not None:
            self.isCapture = True

        move = ""
        piece = piece[1]
        
        if (game.whiteToMove and game.is_in_check("w") == 1) or (not game.whiteToMove and game.is_in_check("b") == 1):
            self.isCheck = True
        elif (game.whiteToMove and game.is_in_check("w") == 2) or (not game.whiteToMove and game.is_in_check("b") == 2):
            self.isDoubleCheck = True

        match piece:
            case "P":
                if self.isCapture:
                    move += self.col_to_letter(col) + "x"
                move += self.col_to_letter(newCol) + str(8-newRow)
                if promotion_choice is not None:
                    move += "=" + promotion_choice
            case "K":
                if castle == "Queenside":
                    move += "0-0-0"
                elif castle == "Kingside":
                    move += "0-0"
                else:
                    move += "K"
                    if self.isCapture:
                        move += "x"
                    move += self.col_to_letter(newCol) + str(8-newRow)
            case "Q":
                move += "Q"
                if self.isCapture:
                    move += "x"
                move += self.col_to_letter(newCol) + str(8-newRow)
            case "R":
                move += "R"
                if self.isCapture:
                    move += "x"
                move += self.col_to_letter(newCol) + str(8-newRow)
            case "N":
                move += "N"
                if self.isCapture:
                    move += "x"
                move += self.col_to_letter(newCol) + str(8-newRow)
            case "B":
                move += "B"
                if self.isCapture:
                    move += "x"
                move += self.col_to_letter(newCol) + str(8-newRow)

        if self.checkmate:
            move += "#"
        elif self.isDoubleCheck:
            move += "++"
        elif self.isCheck:
            move += "+"

        self.isCapture = False
        self.isCheck = False
        self.isDoubleCheck = False

        if not self.whiteToMove:
            self.movelog.append(move)
        else:
            if self.movelog:
                self.movelog[-1] += " "+move

                

    def get_piece(self, row, col):
        return self.board[row][col]

    def build_board(self):
        built = []
        for i in range(8):
            row = []
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                piece = self.board[i][j]
                row.append({"color": color, "piece": piece})
            built.append(row)
        return built

    def get_piece_color(self, row, col):
        if self.board[row][col] is None:
            return None
        return (self.board[row][col])[0]

    def check_whose_move(self, row, col):
        if self.get_piece_color(row, col) == "w" and self.whiteToMove:
            return True
        elif self.get_piece_color(row, col) == "b" and not self.whiteToMove:
            return True
        return False
    
    def is_in_check(self, color):
        numChecks = 0
        kingPos = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == color + "K":
                    kingPos = (row,col)
                    break
            if kingPos:
                break
        if color == "w":
            enemy_color = "b"
        else:
            enemy_color = "w"
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece[0] == enemy_color:
                    if self.check_piece_logic(row, col, kingPos[0], kingPos[1]):
                        numChecks+=1 
        return numChecks    
    
    def is_square_attacked(self, row, col, byColor):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == byColor:
                    if self.check_piece_logic(r, c, row, col):
                        return True
        return False

    
    def restart_game(self):
        self.__init__()

    
    def is_checkmate(self):
        if self.whiteToMove:
            color = "w"
        else:
            color = "b"
        if self.is_in_check(color) != 0:
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece is not None and piece[0] == color:
                        if len(self.get_legal_moves(row, col)) > 0:
                            return False
        else:
            return False
        self.checkmate = True
        return True
    
    def is_stalemate(self):
        if self.whiteToMove:
            color = "w"
        else:
            color = "b"
        if self.is_in_check(color) == 0:
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece is not None and piece[0] == color:
                        if len(self.get_legal_moves(row, col)) > 0:
                            return False
        else:
            return False
        self.stalemate = True
        return True
                        
                        
    def get_legal_moves(self, row, col):
        legal_moves = []
        piece = self.get_piece(row, col)
        
        if piece is None:
            return []
        
        for new_row in range(8):
            for new_col in range(8):
                if self.check_legal_move(row, col, new_row, new_col):
                    legal_moves.append((new_row, new_col))
        
        return legal_moves
        
    #Checks if the capture is the same color piece
    def capture_same_color(self, row, col, newRow, newCol):
        return self.get_piece_color(newRow, newCol) is not None and (self.get_piece_color(newRow, newCol) == self.get_piece_color(row,col))
    
    
    def check_piece_logic(self, row, col, newRow, newCol):
        if self.board[row][col] is not None:
            piece_type = (self.board[row][col])[1]
            legal = True
            if(self.capture_same_color(row, col, newRow, newCol)):
                return False
            match piece_type:
                case "P":
                    if self.get_piece_color(row, col) == "b":
                        normal_move = (newRow == row + 1 and col == newCol and self.get_piece(newRow, col) is None)
                        special_move = (row == 1 and newRow == row + 2 and col == newCol and self.get_piece(newRow, col) is None and self.get_piece(row + 1, col) is None)
                        capture = (abs(newCol - col) == 1 and newRow - row == 1 and self.get_piece(newRow, newCol) is not None)
                        if not (normal_move or special_move or capture):
                            legal = False
                    elif self.get_piece_color(row, col) == "w":
                        normal_move = (newRow == row - 1 and col == newCol and self.get_piece(newRow, col) is None)
                        special_move = (row == 6 and newRow == row - 2 and col == newCol and self.get_piece(newRow, col) is None and self.get_piece(row - 1, col) is None)
                        capture = (abs(newCol - col) == 1 and newRow - row == -1 and self.get_piece(newRow, newCol) is not None)
                        if not (normal_move or special_move or capture):
                            legal = False
                case "K":
                    if (abs(newRow - row), abs(newCol - col)) not in [(0, 1), (1, 0), (1, 1)]:
                        if self.get_piece_color(row, col) == "w" and row == 7 and col == 4:
                            if (newRow, newCol) == (7, 6):
                                if (self.whiteCanCastleKingside and self.board[7][5] is None and self.board[7][6] is None and not self.is_square_attacked(7, 5, "b") and not self.is_square_attacked(7, 6, "b")):
                                    return True
                                else:
                                    return False
                            elif (newRow, newCol) == (7, 2):
                                if (self.whiteCanCastleQueenside and self.board[7][3] is None and self.board[7][2] is None and self.board[7][1] is None and not self.is_square_attacked(7, 3, "b") and not self.is_square_attacked(7, 2, "b")):
                                    return True
                                else:
                                    return False
                        elif self.get_piece_color(row, col) == "b" and row == 0 and col == 4:
                            if (newRow, newCol) == (0, 6):
                                if (self.blackCanCastleKingside and self.board[0][5] is None and self.board[0][6] is None and not self.is_square_attacked(0, 5, "w") and not self.is_square_attacked(0, 6, "w")):
                                    return True
                                else:
                                    return False
                            elif (newRow, newCol) == (0, 2): 
                                if (self.blackCanCastleQueenside and
                                    self.board[0][3] is None and self.board[0][2] is None and self.board[0][1] is None and not self.is_square_attacked(0, 3, "w") and not self.is_square_attacked(0, 2, "w")):
                                    return True
                                else:
                                    return False
                        return False

                case "Q":
                    if abs(newRow-row) == abs(newCol-col):
                        if newRow > row:
                            rowStep=1
                        else:
                            rowStep=-1
                        if newCol > col:
                            colStep=1
                        else:
                            colStep=-1
                        r = row+rowStep
                        c = col+colStep
                        while r != newRow and c != newCol:
                            if self.get_piece(r, c) is not None:
                                legal = False
                                break
                            r += rowStep
                            c += colStep
                    elif (newRow != row and newCol == col):
                        for i in range(min(row, newRow)+1, max(row, newRow)):
                            if self.get_piece(i, col) is not None:
                                legal = False
                                break
                    elif(newRow == row and newCol != col):
                        for i in range(min(col, newCol)+1, max(col, newCol)):
                            if self.get_piece(row,i) is not None:
                                legal = False   
                                break
                    else:
                        legal = False
                case "N":
                    if not (abs(newRow - row), abs(newCol - col)) in [(2, 1), (1, 2)]:
                        legal = False
                case "B":
                    if abs(newRow-row) != abs(newCol-col):
                        legal=False
                    else:
                        if newRow > row:
                            rowStep=1
                        else:
                            rowStep=-1
                        if newCol > col:
                            colStep=1
                        else:
                            colStep=-1
                        r = row+rowStep
                        c = col+colStep
                        while r != newRow and c != newCol:
                            if self.get_piece(r, c) is not None:
                                legal = False
                                break
                            r += rowStep
                            c += colStep      
                case "R":
                    if newRow != row and newCol != col:
                        legal = False
                    elif (newRow != row and newCol == col):
                        for i in range(min(row, newRow)+1, max(row, newRow)):
                            if self.get_piece(i, col) is not None:
                                legal = False
                                break
                    elif(newRow == row and newCol != col):
                        for i in range(min(col, newCol)+1, max(col, newCol)):
                            if self.get_piece(row,i) is not None:
                                legal = False   
                                break                    
            return legal           
        return False
    
    def check_legal_move(self, row, col, newRow, newCol):
        piece = self.board[row][col]
        
        #Return False if not a piece
        if piece is None:
            return False
        
        #Return False if not that player"s move
        if not self.check_whose_move(row,col):
            return False
        
        #Return False if not game logic
        if not self.check_piece_logic(row, col, newRow, newCol):
            return False
        
        #Check if move leaves king in check
        original_piece = self.board[newRow][newCol]
        self.board[newRow][newCol] = self.board[row][col]
        self.board[row][col] = None
        in_check = self.is_in_check(piece[0]) != 0
        self.board[row][col] = piece
        self.board[newRow][newCol] = original_piece

        if in_check:
            return False
        
        return True
        
game = ChessGame()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        newRow = int(data.get("row"))
        newCol = int(data.get("col"))
        status = ""

        if game.checkmate:
            status = "Checkmate! Game over."
            
        if game.stalemate:
            status = "Stalemate! Game over."

        if game.lastClicked and game.get_piece(*game.lastClicked) and game.lastClicked != [newRow, newCol] and not game.checkmate and not game.stalemate:
            startRow, startCol = game.lastClicked
            piece = game.get_piece(startRow, startCol)

            if game.check_legal_move(startRow, startCol, newRow, newCol):
                if piece and piece[1] == "P" and (newRow == 0 or newRow == 7):
                    return jsonify({
                        "promotionPending": True,
                        "fromRow": startRow,
                        "fromCol": startCol,
                        "toRow": newRow,
                        "toCol": newCol
                    })

                game.move_piece(startRow, startCol, newRow, newCol)

                if game.checkmate:
                    status = "Checkmate! Game over."
                elif (game.whiteToMove and game.is_in_check("w") == 1) or (not game.whiteToMove and game.is_in_check("b") == 1):
                    status = "Check!"
                elif (game.whiteToMove and game.is_in_check("w") == 2) or (not game.whiteToMove and game.is_in_check("b") == 2):
                    status = "Double Check!"
                else:
                    status = "Move made."

                game.lastClicked = None
            else:
                status = "Illegal Move"
                game.lastClicked = None
        else:
            game.lastClicked = [newRow, newCol]

        return jsonify({
            "board": game.build_board(),
            "status": status,
            "moveLog": game.movelog
        })

    return render_template("chessboard.html", board=game.build_board())



@app.route("/board_state")
def board_state():
    return jsonify(game.build_board())

@app.route("/restart", methods=["POST"])
def restart():
    game.restart_game()
    return jsonify({
        "board": game.build_board(),
        "status": "Game Restarted",
        "moveLog": game.movelog

    })
    
@app.route("/promote", methods=["POST"])
def promote():
    data = request.json
    row = data["row"]
    col = data["col"]
    newRow = data["newRow"]
    newCol = data["newCol"]
    choice = data["promotion"]
    game.move_piece(row, col, newRow, newCol, promotion_choice=choice)
    return jsonify({"status": "", "board": game.build_board(), "movelog": game.movelog})




if __name__ == "__main__":
    app.run(debug=True)
