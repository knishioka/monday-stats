from .group import Group
from .item import Item


class Board:
    """Monday board class."""

    def __init__(self, board_dict):
        """Initialize board.

        Args:
            board_dict: board dict including id and name
        """
        self.id = board_dict['id']
        self.name = board_dict['name']
        if 'items' in board_dict:
            self.groups = self.parse_groups(board_dict['items'])

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
