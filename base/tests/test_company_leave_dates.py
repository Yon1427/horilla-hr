from datetime import date

from django.test import TestCase

from base.methods import (
    get_company_leave_dates,
    is_company_leave,
    month_week_index,
)
from base.models import CompanyLeaves


class CompanyLeaveWeekIndexTest(TestCase):
    def test_week_starts_on_sunday(self):
        # 2024-09-01 is a Sunday and opens week 0; the Monday belongs to it.
        self.assertEqual(month_week_index(date(2024, 9, 1)), 0)
        self.assertEqual(month_week_index(date(2024, 9, 2)), 0)
        self.assertEqual(month_week_index(date(2024, 9, 8)), 1)


class CompanyLeaveDatesTest(TestCase):
    def test_empty_week_means_every_week(self):
        CompanyLeaves.objects.create(based_on_week="", based_on_week_day="0")
        self.assertIn(date(2026, 1, 5), get_company_leave_dates(2026))

    def test_fifth_week_in_a_four_row_month_does_not_raise(self):
        CompanyLeaves.objects.create(based_on_week="4", based_on_week_day="0")
        dates = get_company_leave_dates(2026)  # Feb 2026 is 4 Sunday-first rows
        self.assertIsInstance(dates, list)

    def test_payroll_and_attendance_agree_on_week_number(self):
        CompanyLeaves.objects.create(based_on_week="0", based_on_week_day="0")
        day = date(2024, 9, 2)  # first Monday, inside Sunday-first week 0
        self.assertIn(day, get_company_leave_dates(2024))
        self.assertTrue(is_company_leave(day))
