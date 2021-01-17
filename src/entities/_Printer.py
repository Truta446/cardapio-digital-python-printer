class Printer(object):
    def __init__(self, printer: dict):
        self.name = printer.get('name')
        self.address_ip = printer.get('address_ip')
