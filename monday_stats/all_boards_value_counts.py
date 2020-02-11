import pandas as pd

from monday_stats.monday_model import MondayModel


def main():
    """Get value counts for each columns."""
    mm = MondayModel()
    board_ids = [b.id for b in mm.boards()]
    for board_id in board_ids:
        board = mm.board_with_items(board_id)
        df = board.to_dataframe()
        print(df.apply(pd.value_counts).fillna(0).astype(int))


if __name__ == '__main__':
    main()
