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
    dfs = board.groups_dataframes()
    df = pd.concat([dfs[g] for g in groups])
    summary = df.replace('', None)\
                .groupby(group_key)\
                .apply(lambda x: x[columns].apply(pd.value_counts))
    output_index = pd.MultiIndex.from_product([df[group_key].unique(), value_texts])
    summary.loc[output_index, :].fillna(0).astype(int).to_csv('output.csv')


if __name__ == '__main__':
    main()
