from typing import Optional


class Restaurant(object):
    def __init__(self, restaurant: dict):
        self.name = restaurant.get('name')
        self.address = restaurant.get('address')
        self.city = restaurant.get('city')
        self.state = restaurant.get('state')
        self.country = restaurant.get('country')
