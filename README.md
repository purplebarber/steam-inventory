# steam inventory
 A simple python package that uses proxies to bypass steam's rate limits on their game inventory API.

## Usage
```python
from steam_inventory.inventories import Inventory
import asyncio

proxy_list = [
    "proxy1:port",
    "proxy2:port",
    "proxy3:port",
    "..."
]

async def main() -> None:
    inventory_client = Inventory(proxies=proxy_list)
    # Get the tf2 inventory of a user with steamID of 00000000000000000
    inventory = await inventory_client.get_inventory(steam_id_64="00000000000000000", app_id=440, context_id="2")
    # Close the client
    await inventory_client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Installation
```bash
pip install steam-inventory
```