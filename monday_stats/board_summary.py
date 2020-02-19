import pandas as pd
import argparse

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
    dfs = board.groups_dataframes()
    df = pd.concat([dfs[g] for g in groups])
    summary = df.replace('', None)\
                .groupby(group_key)\
                .apply(lambda x: x[columns].apply(pd.value_counts))
    output_index = pd.MultiIndex.from_product([df[group_key].unique(), value_texts])
    summary.loc[output_index, :].fillna(0).astype(int).to_csv('output.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summarize board data.')
    parser.add_argument('-b', '--board-id',
                        required=True,
                        help='monday board ids')
    parser.add_argument('-k', '--group-key',
                        required=True,
                        help='Key for grouping')
    parser.add_argument('-g', '--groups',
                        required=True,
                        help='groups list separated by comma')
    parser.add_argument('-v', '--values',
                        required=True,
                        help='value list separated by comma')
    parser.add_argument('-c', '--columns',
                        required=True,
                        help='columns list separated by comma')
    args = parser.parse_args()
    groups = args.groups.split(',')
    value_texts = args.values.split(',')
    columns = args.columns.split(',')
    main(board_id=args.board_id, group_key=args.group_key,
         groups=groups, value_texts=value_texts, columns=columns)
