class Category(object):
    def __init__(self, category: dict):
        self.name = category.get('name')
        self.printer = category.get('printer')
