class Customer(object):
    def __init__(self, customer: dict):
        self.name = customer.get('name')
