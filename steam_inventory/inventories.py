from httpx import AsyncClient
from random import choice


class Inventory:
    def __init__(self, proxies: list = None) -> None:
        if not proxies:
            raise ValueError('steam-inventory must be supplied a list of proxies to bypass steam\'s rate limits! You '
                             'can continue, but you will be rate limited by steam.')

        if not isinstance(proxies, list):
            raise TypeError('steam-inventory only accepts a list of proxies!')

        self.proxies = proxies
        self.current_proxy = choice(range(len(proxies) - 1))
        self.inventory_session = None if self.proxies else AsyncClient(verify=False)

    # GET method using a proxy
    async def get_inventory(self, steam_id_64: str, app_id: int, context_id: str) -> dict:
        if not self.inventory_session and self.proxies:
            self.inventory_session = AsyncClient(
                proxies={
                    "https://": f'http://{self.proxies[self.current_proxy]}',
                    "http://": f'http://{self.proxies[self.current_proxy]}'},
                verify=False
            )

        async def get_steam_inventory_data(url: str) -> dict | None:
            return_dict = {"assets": list(), "descriptions": list(), "last_assetid": 0, "more_items": True}
            response = None

            while return_dict["more_items"]:  # loop until we have all the items
                request_iterator = 0
                status_code = 0

                while status_code != 200 and request_iterator <= 5:  # till we get a 200 code, or if we've tried 5 times
                    params = {
                        "count": 2000,
                        "l": "en",
                        "start_assetid": return_dict.get("last_assetid"),  # start from the last assetid we got
                    }

                    try:
                        response = await self.inventory_session.get(url, params=params)
                        status_code = response.status_code  # get the status code

                    except Exception:
                        response.raise_for_status()
                        return dict()

                    request_iterator += 1  # increment the iterator

                    if status_code == 429 and self.proxies:
                        self.current_proxy += 1
                        if self.current_proxy >= len(self.proxies) - 1:
                            self.current_proxy = 0
                        proxies = {
                            "https://": f'http://{self.proxies[self.current_proxy]}',
                            "http://": f'http://{self.proxies[self.current_proxy]}'
                        }
                        await self.inventory_session.aclose()
                        self.inventory_session = AsyncClient(proxies=proxies, verify=False)

                # if we've tried 5 times and still fail, return dict()
                if status_code != 200 and request_iterator > 5 or not response:
                    response.raise_for_status()
                    return dict()

                resp = response.json()  # convert the response to json

                return_dict.get("assets").extend(resp["assets"])
                return_dict.get("descriptions").extend(resp["descriptions"])
                return_dict["last_assetid"] = resp.get("last_assetid", 0)  # get the last assetid
                return_dict["more_items"] = resp.get("more_items",
                                                     False)  # if there are more items, we need to loop again

                # merge other keys
                for key in resp:
                    if key not in return_dict:
                        return_dict[key] = resp[key]

            return return_dict  # return the inventory data

        # get the user's inventory data
        ret = await get_steam_inventory_data(
            url=f"https://steamcommunity.com/inventory/{steam_id_64}/{app_id}/{context_id}"
        )
        if not ret:  # if the inventory data is None, return an empty dict
            return dict()
        else:
            return ret

    async def close(self) -> None:
        await self.inventory_session.aclose() if self.inventory_session else None
