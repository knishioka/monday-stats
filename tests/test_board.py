from monday_stats.board import Board


def test_board():
    board_id = 1
    board_name = 'test board'
    board = Board(board_id=board_id, board_name=board_name)
    assert board.id == board_id
    assert board.name == board_name


def test_board_with_items():
    group_id = 'group id'
    group_title = 'group title'
    items = [{
        'name': 'item name1',
        'group': {
            'id': group_id,
            'title': group_title
        },
        'column_values': [
            {'title': 'col 1', 'text': 'val 1-1'},
            {'title': 'col 2', 'text': 'val 2-1'}
        ]
    }]
    board = Board(board_id=1, board_name='board name', items=items)
    assert group_title in board.groups.keys()
