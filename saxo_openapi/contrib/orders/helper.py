# -*- coding: utf-8 -*-

import saxo_openapi.definitions.orders as OD


def direction_from_amount(Amount):
    """direction_from_amount - determine direction from the sign of the amount.

    if Amount > 0 : Buy
    if Amount < 0 : Sell
    """
    return OD.Direction.Buy if Amount > 0 else OD.Direction.Sell


def direction_invert(direction):
    """direction_invert - Buy  becomes Sell, Sell becomes Buy."""
    if direction not in [OD.Direction.Buy, OD.Direction.Sell]:
        raise ValueError("wrong value for direction: {}".format(direction))

    return OD.Direction.Buy if direction == OD.Direction.Sell \
        else OD.Direction.Sell


def tie_account_to_order(AccountKey, order):
    """tie_account_to_order - inject the AccountKey in the orderbody.

    An order specification is 'anonymous'. To apply it to an account it needs
    the AccountKey of the account.

    Parameters
    ----------
    AccountKey: string (required)
        the accountkey

    order: dict representing an orderbody or <...>Order instance
        the details of the order.
    """
    _r = order.copy() if isinstance(order, dict) else order.data.copy()

    # add the key to the orderbody
    _r.update({'AccountKey': AccountKey})

    # and add it to related orders in Orders (if any)
    if 'Orders' in _r:
        for o in _r['Orders']:
            o.update({'AccountKey': AccountKey})

    return _r
