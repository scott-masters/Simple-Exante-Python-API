def place_order(
    self, market: str, side: str, price: str, size: str,
    type: str = 'limit', duration: str = "good_till_cancel") -> dict:
    """
    Enters an order to Exante, either to a live or demo account.

    Inputs:
        -> side: str, either 'buy' or 'sell'.
        -> type: str, options are 'market', 'limit', 'stop', 'stop_limit', 
           'twap', 'trailing_stop' and 'iceberg'. Not all orders are valid on 
           all exante products.
        -> duration: str, options are 'good_till_cancel', 'good_till_time', 
           'day', 'fill_or_kill', 'immediate_or_cancel', 'at_the_opening' and 
           'at_the_close'.
        
    Returns:
        -> dict: containing details on the order you just placed. You should
           save the order id, you'll need it to cancel the order.
    """
    trade = self._post(f"trade/{self.version}/orders", {
        'accountId': self.account,
        'symbolId': market,
        'side': side,
        'quantity': size,
        'orderType': type,
        'limitPrice': price,
        'duration': duration,
    })[0]

    return trade

def cancel_order(self, id: int) -> dict: 
    return self._post(f"trade/{self.version}/orders/{id}", {
        'action': "cancel"})