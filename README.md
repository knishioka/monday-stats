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
