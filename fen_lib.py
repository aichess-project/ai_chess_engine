def remove_counters_from_fen(fen):
    # Split the FEN string by spaces
    parts = fen.split()

    # Keep only the relevant parts, excluding the last two elements (half move and full move counters)
    fen_without_counters = ' '.join(parts[:-2])

    return fen_without_counters

def get_color_from_fen(fen):
    # Split the FEN string by spaces
    parts = fen.split()

    # Get the color from the sixth element (at index 1)
    color = parts[1]

    return color
