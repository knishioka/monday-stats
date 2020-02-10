import pandas as pd

from .group import Group
from .item import Item


class Board:
    """Monday board class."""

    def __init__(self, board_id, board_name, items=[]):
        """Initialize board.

        Args:
            board_id (str): board id.
            board_name (str): board name

        """
        self.id = board_id
        self.name = board_name
        if items:
            self.groups = self.parse_groups(items)
        else:
            self.groups = {}

    def parse_groups(self, items):
        """Parse group data from dict.

        Args:
            items (list): item list including group.

        Returns:
            dict: key is group_id and value is Group class.

        """
        groups = {}
        for item in items:
            group_title = item['group']['title']
            if group_title not in groups:
                groups[group_title] = Group(group_id=item['group']['id'],
                                            group_title=group_title)
            groups[group_title].add_item(Item(item['name'], item['column_values']))
        return groups

    def groups_dataframes(self):
        """Return dict of group dataframes.

        Returns:
            `dict` of `pandas.DataFrame`: key is group_id and value is items pandas.DataFrame.

        """
        return {group_id: g.to_dataframe() for group_id, g in self.groups.items()}

    def to_dataframe(self, index='item'):
        """Return dataframe including all groups.

        Args:
            index (str): 'item' or 'column'

        Returns:
            pandas.DataFrame: dataframe includes all group items.

        """
        df = pd.concat(self.groups_dataframes().values(), axis=1)
        if index == 'column':
            return df.T
        elif index == 'item':
            return df
        else:
            raise ValueError("index must be 'columns' or 'item'")
