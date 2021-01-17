from datetime import datetime
from typing import List, Optional

from escpos.printer import Network

from entities import Item, Customer, Restaurant, Order, Table
from exceptions import PrinterException


class SalePrinter(object):
    def __init__(
        self,
        restaurant: Restaurant,
        amount: float,
        discount_amount: float,
        tax_amount: float,
        items: List[Item],
        table: Table,
        customer: Optional[Customer],
        ip_printer: str
    ):
        self.restaurant = restaurant
        self.amount = amount
        self.discount_amount = discount_amount
        self.tax_amount = tax_amount
        self.items = items
        self.table = table
        self.customer = customer
        self.ip_printer = ip_printer

    def template_us(self) -> None:
        date = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

        try:
            p = Network(self.ip_printer)

            # Header
            p.set(align="center")
            p.charcode('USA')
            p.text(f'\n\n\n\n{self.restaurant.name}\n\n')
            p.text(f'Address: {self.restaurant.address}\n')
            p.text(f'{self.restaurant.city} - {self.restaurant.state}\n')

            # Body
            p.set(align="left")
            p.text('QTY ITEM (V. UNIT)                          TOTAL')
            qty_items = 0
            for item in self.items:
                sub_total = int(item.get('quantity')) * float(item.get('sale_price'))
                qty_items += int(item.get('quantity'))
                p.text(f'{item.get("quantity")} {item.get("product").get("name")} ({self._currency_us(float(item.get("sale_price")))}) {self._currency_us(float(sub_total))}     \n')

                if item.get('complements') is not None:
                    for complement in item.get('complements'):
                        sub_total_complement = int(complement.get("quantity")) * float(complement.get('complement').get('sale_price'))
                        p.text(f'+ {complement.get("complement").get("description")} ({complement.get("quantity")})               {self._currency_us(float(complement.get("complement").get("sale_price")))}     |     {self._currency_us(float(sub_total_complement))}     \n')

            
            p.text('------------------------------------------------\n')
            p.text(f'QTY OF ITEMS                                  {qty_items}\n')
            p.text(f'SUBTOTAL                                {self._currency_us(float(self.amount))}\n')
            p.text(f'DISCOUNTS                                {self._currency_us(float(self.discount_amount))}\n')
            p.text(f'ADDITIONS                                {self._currency_us(float(self.tax_amount))}\n')
            total = self.amount + self.tax_amount - self.discount_amount
            p.text(f'TOTAL VALUE                              {self._currency_us(float(total))}\n\n')

            # Pos Body
            p.text('------------------------------------------------\n')
            p.set(align="center")
            p.text('CLIENT:\n')
            p.set(align="center")
            customer = self.customer.name if self.customer and self.customer.name else 'Unreported Customer'
            p.text(f'{customer}\n')
            p.text('------------------------------------------------\n')
            p.text('WITHOUT TAX VALUE\n')
            p.text('------------------------------------------------\n')

            # Footer
            p.text(f'{date}\n')
            p.text(f'Flag Techs\n')
            p.set(align="center")
            p.text('(67) 9 9947-3474\n')
            p.text('www.flagtechs.com.br\n')

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
            p.text(f'Endereco: {self.restaurant.address}\n')
            p.text(f'{self.restaurant.city} - {self.restaurant.state}\n')

            # Body
            p.set(align="right")
            p.text('________________________________________________\n')
            p.text('  #  |  COD  |  DESC  |  QTD  | VL. UNIT | TOTAL\n')
            p.text('________________________________________________\n')
            qty_items = 0
            count = 0
            for item in self.items:
                count += 1
                sale_price_formatted = self._currency_pt(float(item.get('sale_price')))
                sub_total = int(item.get('quantity')) * float(item.get('sale_price'))
                qty_items += int(item.get('quantity'))
                p.text(f'  {count}  |  {item.get("id")}  |  {item.get("product").get("name")}  |  {item.get("quantity")}  |  {sale_price_formatted}  |  {self._currency_pt(float(sub_total))}\n')
                p.text('------------------------------------------------\n')
            p.text(f'QTD DE ITENS                                  {qty_items}\n')
            p.text(f'SUBTOTAL                               {self._currency_pt(float(self.amount))}\n')
            p.text(f'DESCONTOS                                {self._currency_pt(float(self.discount_amount))}\n')
            p.text(f'ADICIONAIS                               {self._currency_pt(float(self.tax_amount))}\n')
            total = self.amount + self.tax_amount - self.discount_amount
            p.set(align="right", type="b")
            p.text(f'VALOR TOTAL                        {self._currency_pt(float(total))}\n\n')

            # Pos Body
            p.text('------------------------------------------------\n')
            p.set(align="center")
            p.text('CLIENTE:\n')
            p.set(align="center")
            customer = self.customer.name if self.customer and self.customer.name else 'Cliente não Informado'
            p.text(f'{customer}\n')
            p.text('------------------------------------------------\n')
            p.text('SEM VALOR FISCAL\n')
            p.text('------------------------------------------------\n')

            # Footer
            p.text(f'{date}\n')
            p.text(f'Flag Techs\n')
            p.set(align="center")
            p.text('(67) 9 9947-3474\n')
            p.text('www.flagtechs.com.br\n')

            # Finish
            p.cut()
        except Exception as ex:
            raise PrinterException(f'An error ocurred when trying to print: {ex}')

    def _currency_us(self, value: float) -> str:
        value = '%.2f' % value
        return f'$ {str(value)}'

    def _currency_pt(self, value: float) -> str:
        value = '%.2f' % value
        value = str(value)
        return f'R$ {value.replace(".", ",")}'
