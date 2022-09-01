# This file contains all the core logic of the Exante client while specific
# functions are kept in the get.py and post.py files.

import jwt # This is a buildin package to not try to 'pip install' it.
import time
import pytz
import datetime as dt
import requests as rq

class JWTAuth():
    def __init__(self, app_id: str, client_id: str, shared_key: str, ttl: int, scopes: list):
        self.app_id = app_id
        self.client_id = client_id
        self.shared_key = shared_key
        self.ttl = ttl
        self.scopes = scopes
        self.token = self.make_token()

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

    def make_token(self) -> str:
        now = int(dt.datetime.now(dt.timezone.utc).timestamp())
        token = jwt.encode(
            payload = {
                "iss": self.client_id,
                "sub": self.app_id,
                "iat": now,
                "exp": now + self.ttl,
                "aud": self.scopes
            },
            key = self.shared_key,
            algorithm = "HS256"
            )
        return token

class Exante_Client:
    """
    An Exante Client can collect information from all exante product offerings 
    and send orders to that exchange. The client is built to interact with this
    documentation, https://api-live.exante.eu/api-docs/.
    """
    from get import (
        get_order, get_orders, get_orders_active, get_account, get_book, 
        get_symbol, get_hours, get_specifications, get_ticks, get_candles, 
        get_history
    )
    from post import place_order, cancel_order
    
    def __init__(
        self, 
        account: str, 
        app_id: str, 
        client_id: str, 
        shared_key: str, 
        end_point: str,
        scopes: list = ["symbols", "feed", "change", "ohlc", "crossrates", "summary", "orders", "transactions", "accounts"], 
        ttl: int = 3660, 
        version: str = "3.0") -> None:
        """
        Inputs:
            -> end_point: str, https://api-demo.exante.eu/" for demo accounts
               and "https://api-live.exante.eu/" for live accounts.
            -> scopes: list, defines what the client is allowed to do. Possible
               scopes are 'symbols', 'feed', 'change', 'ohlc', 'crossrates',
               'summary', 'orders', 'transactions' and 'accounts'. By default
               the client will have permission to do everything.
            -> ttl: str, number of seconds that a token is valid for. By default
               tokens will need to be refreshed hourly. This can be done by 
               calling the refresh funciton.
        """
        self.session = rq.Session()
        self.end_point = end_point

        self.app_id = app_id
        self.client_id = client_id
        self.shared_key = shared_key
        self.ttl = ttl
        self.scopes = scopes
        self.auth = JWTAuth(app_id, client_id, shared_key, ttl, scopes)
        
        self.version = version
        self.account = account

    def _get(self, path: str, params: dict = None):
        return self._request("GET", path, auth = self.auth, params = params)

    def _post(self, path: str, params: dict = None):
        return self._request("POST", path, auth = self.auth, json = params)

    def _delete(self, path: str, params: dict = None):
        return self._request("DELETE", path, auth = self.auth, params = params)
    
    def _request(self, method: str, path: str, **kwargs):
        request = rq.Request(method, self.end_point + path, **kwargs)
        try:
            response = self.session.send(request.prepare())
            return self._process_response(response)
        except Exante_Error_Incorrect_Credentials:
            # We'll refresh our credentials and try again, just encase that's 
            # the problem.
            self.refresh()
            kwargs['auth'] = self.auth
            request = rq.Request(method, self.end_point + path, **kwargs)
            response = self.session.send(request.prepare())
            return self._process_response(response)

    def _process_response(self, response: rq.Response):
        if response.status_code == 401 and response.reason == "Unauthorized":
            raise Exante_Error_Incorrect_Credentials("401: Unauthorized")
        elif response.status_code == 429 and "Too Many Requests" in response.reason:
            raise Exante_Error_Rate_Limit(f"429: {response.reason}")
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            return data
    
    def refresh(self):
        """
        Creates a new authentication token encase the previous one (which gets
        over-written) has expired. The new token will be valid for self.ttl 
        seconds.
        """
        self.auth = JWTAuth(
            self.app_id, self.client_id, self.shared_key, self.ttl, self.scopes)

class Exante_Error(Exception):
    pass

class Exante_Error_Incorrect_Credentials(Exante_Error):
    """
    Incorrect credentials:
        -> This can happen because your jwt token as expired. Remember to have
           your client call the refresh funciton once an hour.
    """
    pass

class Exante_Error_Rate_Limit(Exante_Error):
    """
    You have inserted too many requests over too short a period of time and 
    Exante is cutting you off so you don't excessively burden their system.
    """
    pass