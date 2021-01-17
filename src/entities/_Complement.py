class Complement(object):
    def __init__(self, complement: dict):
        self.complement = complement.get('complement')
        self.quantity = complement.get('quantity')
        self.sale_price = complement.get('sale_price')
