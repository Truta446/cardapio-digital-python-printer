class Combo(object):
    def __init__(self, combo: dict):
        self.sale_price = combo.get('sale_price')
        self.quantity = combo.get('quantity')
        self.combo = combo.get('combo')
