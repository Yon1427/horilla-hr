from decimal import Decimal

from django.test import SimpleTestCase, TestCase

from payroll.methods.methods import money
from payroll.models.models import Payslip


class PayslipMoneyTypeTest(TestCase):
    def test_payslip_money_columns_are_decimal(self):
        for name in ("contract_wage", "basic_pay", "gross_pay", "deduction", "net_pay"):
            field = Payslip._meta.get_field(name)
            self.assertEqual(field.get_internal_type(), "DecimalField", name)
            self.assertEqual(field.decimal_places, 2, name)


class MoneyHelperTest(SimpleTestCase):
    def test_rounds_half_up(self):
        self.assertEqual(money("0.105"), Decimal("0.11"))
        self.assertEqual(money(0.105), Decimal("0.11"))

    def test_none_is_zero(self):
        self.assertEqual(money(None), Decimal("0.00"))
