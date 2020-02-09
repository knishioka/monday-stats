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
