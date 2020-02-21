# monday-stats

## Quick Start

Add your monday token to .env.

```bash
cp .env.sample .env
vim .env
```

Install dependent libraries.

```bash
pipenv install
```

Get the item count for each group.

```bash
pipenv run group_item_count --board-id <your board id>
```

Get the board summary.

```bash
pipenv run python -m  monday_stats.board_summary -b $board_id -k $keyname -g $group1,$group2 -v $value1,$value2,$value3 -c $column1,$column2,$column3
```
