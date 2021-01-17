class Caster(object):
    def __init__(self, caster: dict):
        self.sale_price = caster.get('sale_price')
        self.quantity = caster.get('quantity')
        self.products = caster.get('products')
