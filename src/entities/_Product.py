class Product(object):
    def __init__(self, product: dict):
        self.id = product.get('id')
        self.name = product.get('name')
        self.category = product.get('category')
