class Board:
    def __init__(self, board_dict):
        """Initializer.

        Args:
            board_dict: board dict including id and name
        """
        self.id = board_dict['id']
        self.name = board_dict['name']
