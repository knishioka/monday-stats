# monday-stats

## Quick Start

Add your monday token to .env.

```bash
cp .env.sample .env
vim .env
```

Get the item count for each group.

```bash
python -m monday_stats.group_item_count --board-id <your board id>
```
