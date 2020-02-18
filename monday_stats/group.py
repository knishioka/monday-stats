import pandas as pd

from .item import Item


class Group:
    """Monday group class."""

    def __init__(self, group_id, group_title):
        """Initialize group.

        Args:
            group_id (str): group id.
            group_title (str): group title.

        """
        self.id = group_id
        self.title = group_title
        self.items = []

    def add_item(self, item):
        """Add item class to the group.

        Args:
            items (Item): Item class.

        """
        assert Item == type(item), 'item should be Item object.'
        self.items.append(item)

    def to_dataframe(self):
        """Convert item list to pandas.DataFrame.

        Returns:
            pandas.DataFrame: each row stands for an item.

        """
        return pd.concat(map(lambda x: x.values, self.items), axis=1).T
