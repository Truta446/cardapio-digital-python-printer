from typing import List, Dict

from flask_restful import Resource, reqparse

from entities import Customer, Restaurant, Order, Table, Item, Printer, Combo, Caster
from services import CookPrinter, SalePrinter


class Printing(Resource):
    def post(self) -> Dict:
        try:
            args = reqparse.RequestParser()

            args.add_argument('id', type=int)
            args.add_argument('restaurant', type=Restaurant)
            args.add_argument('amount', type=float)
            args.add_argument('discount_amount', type=float)
            args.add_argument('tax_amount', type=float)
            args.add_argument('items', type=list, location='json')
            args.add_argument('combos', type=list, location='json')
            args.add_argument('casters', type=list, location='json')
            args.add_argument('table', type=Table)
            args.add_argument('customer', type=Customer)
            args.add_argument('printer', type=Printer)

            data = args.parse_args()

            items = self._filter_properties(data.get('items'), data.get('combos'), data.get('casters'))

            for item in items:
                cook_printer = CookPrinter(
                    order_id=data.id,
                    restaurant=data.restaurant,
                    items=items[item],
                    table=data.table,
                    customer=data.customer,
                    ip_printer=item
                )

                if data.restaurant.country == 'BR':
                    cook_printer.template_pt()
                else:
                    cook_printer.template_us()

            """ sale_printer = SalePrinter(
                restaurant=data.restaurant,
                amount=data.amount,
                discount_amount=data.discount_amount,
                tax_amount=data.tax_amount,
                items=data.get('items'),
                table=data.table,
                customer=data.customer,
                ip_printer=data.printer.address_ip
            )

            if data.restaurant.country == 'BR':
                sale_printer.template_pt()
            else:
                sale_printer.template_us() """

            return {'message': 'Print Successfully!'}, 200
        except Exception as ex:
            return {'message': f'An error ocurred when mount request: {ex}'}, 500

    def _filter_properties(
        self,
        items: List[Item],
        combos: List[Combo],
        casters: List[Caster]
    ) -> Dict:
        ret = {}

        for item in items:
            address_ip = item.get('product').get('category').get('printer').get('address_ip')

            if ret != {} and address_ip in ret:
                ret[address_ip].append(item)
            else:
                ret[address_ip] = []
                ret[address_ip].append(item)

        for combo in combos:
            for product_combo in combo.get('combo').get('products'):
                address_ip = product_combo.get('product').get('category').get('printer').get('address_ip')
                product_combo.update({'combo_quantity': combo.get('quantity'), 'combo_name': combo.get('combo').get('name')})
                if ret != {} and address_ip in ret:
                    ret[address_ip].append(product_combo)
                else:
                    ret[address_ip] = []
                    ret[address_ip].append(product_combo)

        for caster in casters:
            for product_caster in caster.get('products'):
                address_ip = product_caster.get('product').get('category').get('printer').get('address_ip')
                product_caster.update({'caster_quantity': caster.get('quantity'), 'caster_name': caster.get('caster').get('name')})
                if ret != {} and address_ip in ret:
                    ret[address_ip].append(product_caster)
                else:
                    ret[address_ip] = []
                    ret[address_ip].append(product_caster)

        return ret
