class Item(object):
    def __init__(self, item: dict):
        self.id = item.get('id')
        self.order_id = item.get('order_id')
        self.quantity = item.get('quantity')
        self.sale_price = item.get('sale_price')
        self.complements = item.get('complements')
        self.product = item.get('product')
