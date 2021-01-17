from datetime import datetime
from typing import List, Optional

from escpos.printer import Network

from entities import Item, Customer, Restaurant, Order, Table
from exceptions import PrinterException


class CookPrinter(object):
    def __init__(
        self,
        order_id: int,
        restaurant: Restaurant,
        items: List[Item],
        table: Table,
        customer: Optional[Customer],
        ip_printer: str
    ):
        self.order_id = order_id
        self.restaurant = restaurant
        self.items = items
        self.table = table
        self.customer = customer
        self.ip_printer = ip_printer

    def template_us(self) -> None:
        date = datetime.now().strftime('%A, %d of %B %Y %I:%M:%S %p')

        try:
            p = Network(self.ip_printer)

            # Header
            p.charcode('USA')
            p.set(align="center")
            p.text(f'\n\n\n\n{self.restaurant.name}\n\n')
            p.text(f'Table: {str(self.table.table_number)}\n')
            p.text(f'Order: {self.order_id}\n')
            customer = self.customer.name if self.customer and self.customer.name else 'Unreported Customer'
            p.text(f'Client: {customer}\n\n')

            # Body
            p.set(align="center")
            p.text('\n\n------------------------------------------------\n\n')

            for item in self.items:
                if item.get('combo_quantity') is not None:
                    p.text(f'{item.get("combo_quantity")}X {item.get("combo_name")}\n')
                    p.text(f'{item.get("quantity")}X{item.get("combo_quantity")} ({item.get("quantity") * item.get("combo_quantity")}) {item.get("product").get("name")}\n')
                elif item.get('caster_quantity') is not None:
                    p.text(f'{item.get("caster_quantity")}X {item.get("caster_name")}\n')
                    p.text(f'{item.get("quantity")}X{item.get("caster_quantity")} ({item.get("quantity") * item.get("caster_quantity")}) {item.get("product").get("name")}\n')
                else:
                    p.text(f'{item.get("quantity")}X {item.get("product").get("name")}\n')

                if item.get('complements') is not None:
                    p.set(align="left")
                    for complement in item.get('complements'):
                        p.text(f'+{complement.get("quantity")} {complement.get("complement").get("description")}\n')

                p.set(align="center")
                p.text('\n\n------------------------------------------------\n\n')

            # Footer
            p.text(f'\n\n{str(date)}')

            # Finish
            p.cut()
        except Exception as ex:
            raise PrinterException(f'An error ocurred when trying to print: {ex}')

    def template_pt(self) -> None:
        date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        try:
            p = Network(self.ip_printer)

            # Header
            p.set(align="center")
            p.text(f'\n\n\n\n{self.restaurant.name}\n\n')
            p.text(f'Mesa: {str(self.table.table_number)}\n')
            p.text(f'Pedido: {self.order_id}\n')
            customer = self.customer.name if self.customer and self.customer.name else 'Cliente não Informado'
            p.text(f'Cliente: {customer}\n\n')

            # Body
            p.set(align="center")
            p.text('\n\n------------------------------------------------\n\n')

            for item in self.items:
                p.text(f'{item.get("quantity")}X {item.get("product").get("name")}\n')

                if item.get('complements') is not None:
                    p.set(align="left")
                    for complement in item.get('complements'):
                        p.text(f'+{complement.get("quantity")} {complement.get("complement").get("description")}\n')

                p.set(align="center")
                p.text('\n\n------------------------------------------------\n\n')

            # Footer
            p.text(f'\n\n{str(date)}')

            # Finish
            p.cut()
        except Exception as ex:
            raise PrinterException(f'An error ocurred when trying to print: {ex}')
