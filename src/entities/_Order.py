from typing import List, Optional

from ._Restaurant import Restaurant
from ._Item import Item
from ._Customer import Customer
from ._Table import Table


class Order(object):
    def __init__(
        self,
        restaurant: Restaurant,
        table: Table,
        items: List[Item],
        customer: Optional[Customer]
    ):
        self.restaurant = restaurant
        self.table = table
        self.items = items
        self.customer = customer
