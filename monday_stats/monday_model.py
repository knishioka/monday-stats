import os
import json
import requests

from .board import Board


class MondayModel:
    """Model to fetch monday data."""

    def __init__(self):
        """Initializer."""
        self.endpoint = 'https://api.monday.com/v2/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': os.environ['MONDAY_TOKEN']
        }

    def query(self, gql):
        """Post GraphQL to monday.

        Args:
            gql (str): gql for query.

        Returns:
            `list` of `dict`: monday data list.

        Examples:
            >>> mm = MondayModel()
            >>> mm.query('{boards {id name}}')
            [{'id': '1111111', 'name': 'test board 1'},
             {'id': '2222222', 'name': 'test board 2'}]

        """
        r = requests.post(self.endpoint,
                          data=json.dumps({"query": gql}),
                          headers=self.headers)
        return r.json()['data']

    def boards(self):
        """Get boards list.

        Returns:
            `list` of `Board`: Board class list.

        Examples:
            >>> mm = MondayModel()
            >>> mm.boards()
            [<monday_stats.board.Board at 0x111389090>,
             <monday_stats.board.Board at 0x111ff3990>,

        """
        gql = '{boards {id name}}'
        boards = [Board(b) for b in self.query(gql)['boards']]
        return boards

    def board_items(self, board_id):
        """Get specific board with items.

        Args:
            board_id: monday board id.

        Returns:
            `list` of `dict`: board data.

        """
        gql = """
        {
          boards(ids: %s) {
            name
            items {
              name
              group {
                title
              }
              column_values {
                title
                text
              }
            }
          }
        }
        """ % (board_id)
        return self.query(gql)['boards']
