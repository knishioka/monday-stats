import pandas as pd
from monday_stats.monday_model import MondayModel


def main(board_id, groups=[], index=[], columns=[]):
    mm = MondayModel()
    board = mm.board_with_items(board_id)
    dfs = board.groups_dataframes()
    df = pd.concat([dfs[g] for g in groups])
    summary = df.replace('', None)\
                .groupby('Position')\
                .apply(lambda x: x[columns].apply(pd.value_counts))
    output_index = pd.MultiIndex.from_product([df.Position.unique(), index])
    summary.loc[output_index, :].fillna(0).astype(int).to_csv('output.csv')


if __name__ == '__main__':
    main()
