import pytest

from monday_stats.board import Board


@pytest.fixture
def board_item_dict():
    group_id = 'group_id_1'
    group_title = 'group_title_1'
    board_items = [
        {
            'name': 'item name1',
            'group': {
                'id': 'group_id_1',
                'title': 'group_title_1'
            },
            'column_values': [
                {'title': 'col_1', 'text': 'val 1-1'},
                {'title': 'col_2', 'text': 'val 2-1'}
            ]
        },
        {
            'name': 'item name2',
            'group': {
                'id': 'group_id_1',
                'title': 'group_title_1'
            },
            'column_values': [
                {'title': 'col_1', 'text': 'val 1-2'},
                {'title': 'col_2', 'text': 'val 2-2'}
            ]
        },
        {
            'name': 'item name3',
            'group': {
                'id': 'group_id_2',
                'title': 'group_title_2'
            },
            'column_values': [
                {'title': 'col_1', 'text': 'val 1-3'},
                {'title': 'col_2', 'text': 'val 2-3'}
            ]
        }
    ]
    return board_items


def test_board():
    board_id = 1
    board_name = 'test board'
    board = Board(board_id=board_id, board_name=board_name)
    assert board.id == board_id
    assert board.name == board_name


def test_board_with_items(board_item_dict):
    board = Board(board_id=1, board_name='board name', items=board_item_dict)
    assert 'group_title_1' in board.groups.keys()


def test_to_dataframe(board_item_dict):
    board = Board(board_id=1, board_name='board name', items=board_item_dict)
    df = board.to_dataframe()
    assert 'col_1' in df.columns and 'col_2' in df.columns
