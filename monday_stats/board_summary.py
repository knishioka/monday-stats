import argparse
import datetime

import pandas as pd

from monday_stats.monday_model import MondayModel


def main(board_id, group_key, groups=[], value_texts=[], columns=[]):
    """Summarize board.

    Args:
        board_id (str): monday board id.
        group_key (str): group key which need to be one of board columns.
        groups (`list` of `str`): monday group title list.
        value_texts (`list` of `str`): target values.
        columns (`list` of `str`): target columns

    """
    mm = MondayModel()
    board = mm.board_with_items(board_id)
    df = board_summary(board, group_key, groups, value_texts, columns)
    file = f'{datetime.datetime.today().strftime("%Y%m%d")}_{board.name}.csv'
    df.to_csv(file)


def board_summary(board, group_key, groups=[], value_texts=[], columns=[]):
    """Summarize board.

    Args:
        board (monday.board.Board): monday Board class.
        group_key (str): group key which need to be one of board columns.
        groups (`list` of `str`): monday group title list.

    Returns:
        pandas.DataFrame: summarized dashboard.

    """
    dfs = board.groups_dataframes()
    existing_groups = set(groups).intersection(dfs.keys())
    df = pd.concat([dfs[g] for g in existing_groups])
    summary = pd.concat(
        [
            summarize_group(gdf, group_id, value_texts=value_texts, columns=columns)
            for group_id, gdf in df.groupby("Position")
        ]
    )
    output_index = pd.MultiIndex.from_product([df[group_key].unique(), value_texts])
    return summary.reindex(output_index).fillna(0).astype(int)


def summarize_group(gdf, group_id, value_texts=[], columns=[]):
    """Summarize group df.

    Args:
        gdf (pd.DataFrame): items in the group.
        group_id (str): monday group id.
        value_texts (`list` of `str`): target values.
        columns (`list` of `str`): target columns

    Returns:
        pd.DataFrame: group summary.

    """
    summary = gdf[columns].apply(pd.value_counts).reindex(value_texts)
    summary.index = summary.index.map(lambda x: (group_id, x))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize board data.")
    parser.add_argument("-b", "--board-id", required=True, help="monday board id")
    parser.add_argument("-k", "--group-key", required=True, help="Key for grouping")
    parser.add_argument("-g", "--groups", required=True, help="groups list separated by comma")
    parser.add_argument("-v", "--values", required=True, help="value list separated by comma")
    parser.add_argument("-c", "--columns", required=True, help="columns list separated by comma")
    args = parser.parse_args()
    groups = args.groups.split(",")
    value_texts = args.values.split(",")
    columns = args.columns.split(",")
    main(
        board_id=args.board_id,
        group_key=args.group_key,
        groups=groups,
        value_texts=value_texts,
        columns=columns,
    )
