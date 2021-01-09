import argparse

from monday_stats.monday_model import MondayModel


def main(board_id):
    """Get the item count for each group.

    Args:
        board_id (str): monday board_id.

    """
    mm = MondayModel()
    board_ids = [b.id for b in mm.boards()]
    if board_id not in board_ids:
        raise ValueError(f"board_id must be one of {board_ids}")
    board = mm.board_with_items(board_id)
    for group_id, df in board.groups_dataframes().items():
        print(group_id, len(df))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count items in groups")
    parser.add_argument("-b", "--board-id", required=True, help="monday board ids")
    args = parser.parse_args()
    main(board_id=args.board_id)
