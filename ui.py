import logging
import chess

class ChessUI():

    uni_pieces = {'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
              'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙', '.': '·'}

    rank_labels = ['1', '2', '3', '4', '5', '6', '7', '8']
    file_labels = "   a b c d e f g h "
    separator   = "   ----------------"

    def print_board(self, board):
      print(self.file_labels)
      print(self.separator)
      for rank in range(7, -1, -1):  # Start from the 8th rank (row 7) to the 1st rank (row 0)
        row_str = []
        for file in range(8):
          square = chess.square(file, rank)
          piece = board.piece_at(square)
          if piece is None:
            row_str.append(self.uni_pieces['.'])
          else:
            row_str.append(self.uni_pieces.get(piece.symbol(), piece.symbol()))  # Use piece.symbol() as fallback
        print(self.rank_labels[rank] + "|", " ".join(row_str), "|", self.rank_labels[rank])  # Rank label
      print(self.separator)
      print(self.file_labels)

    def get_move_and_execute(self, board):
      exit = False
      while True:
          try:
            user_move = input("Enter your move (e.g., 'e2e4'): ")
            if user_move == "exit":
              return True, None
            board.push_san(user_move)
            return False, user_move
          except ValueError:
            print("Invalid move. Please try again.")