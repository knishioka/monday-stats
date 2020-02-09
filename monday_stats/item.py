import pandas as pd


class Item():
    """Monday item class."""

    def __init__(self, name, column_values):
        """Initialize Item class.

        Args:
            name (str): item name.
            column_values (`list` of `dict`): dict includes title and text.

        """
        self.name = name
        titles = map(lambda x: x['title'], column_values)
        values = map(lambda x: x['text'], column_values)
        self.values = pd.Series(values, titles).rename(name)
