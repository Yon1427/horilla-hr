"""Approval must lock the balance and never approve without deducting it.

Two approvals racing on the same AvailableLeave both used to pass the
sufficiency check, and the "no approval required" path swallowed a balance
save failure after the leave had already been saved as approved.
"""

from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext, skipIf

from horilla.testkit import make_company, make_employee, make_user
from leave.models import AvailableLeave, LeaveRequest, LeaveType


class _LeaveFixture(TestCase):
    def setUp(self):
        company = make_company("Approval Atomic Co")
        self.leave_type = LeaveType.objects.create(
            name="Atomic Leave", total_days=20
        )
        self.employee = make_employee(company=company, email="atomic@test.horilla")

    def _request(self, days=3, persist=False):
        today = date.today()
        req = LeaveRequest(
            employee_id=self.employee,
            leave_type_id=self.leave_type,
            start_date=today + timedelta(days=3),
            end_date=today + timedelta(days=3),
            start_date_breakdown="full_day",
            end_date_breakdown="full_day",
            requested_days=days,
            description="approval atomic test",
            status="requested",
            approved_available_days=0,
            approved_carryforward_days=0,
        )
        if persist:
            req.save()
        return req


class NoApprovalBalanceTests(_LeaveFixture):
    def test_no_approval_deducts_available_then_carryforward(self):
        avail = AvailableLeave.objects.create(
            employee_id=self.employee,
            leave_type_id=self.leave_type,
            available_days=1,
            carryforward_days=4,
            total_leave_days=5,
        )
        req = self._request(days=3)
        req.no_approval()
        avail.refresh_from_db()
        self.assertEqual(avail.available_days, 0)
        self.assertEqual(avail.carryforward_days, 2)
        self.assertEqual(req.approved_available_days, 1)
        self.assertEqual(req.approved_carryforward_days, 2)
        self.assertEqual(req.status, "approved")


class BalanceFailureRollsBackTest(_LeaveFixture):
    def test_failed_balance_save_does_not_mark_approved(self):
        AvailableLeave.objects.create(
            employee_id=self.employee,
            leave_type_id=self.leave_type,
            available_days=5,
            carryforward_days=0,
            total_leave_days=5,
        )
        req = self._request(days=3, persist=True)

        with patch.object(AvailableLeave, "save", side_effect=Exception("boom")):
            with self.assertRaises(Exception):
                req.no_approval()

        self.assertNotEqual(req.status, "approved")
        self.assertEqual(
            LeaveRequest.objects.get(pk=req.pk).status,
            "requested",
        )


@skipIf(connection.vendor == "sqlite", "select_for_update is a no-op on SQLite")
class ApprovalLocksBalanceTest(_LeaveFixture):
    def test_approval_locks_the_balance(self):
        AvailableLeave.objects.create(
            employee_id=self.employee,
            leave_type_id=self.leave_type,
            available_days=5,
            carryforward_days=0,
            total_leave_days=5,
        )
        req = self._request(days=3, persist=True)

        approver_user = make_user("atomic_approver", password="secret123")
        approver_user.user_permissions.add(
            Permission.objects.get(codename="change_leaverequest")
        )
        # Permission caching is per-instance, so refetch after granting.
        approver_user = type(approver_user).objects.get(pk=approver_user.pk)
        make_employee(
            company=make_company("Approver Co"),
            email="atomic_approver@test.horilla",
            user=approver_user,
        )
        self.client.force_login(approver_user)

        with CaptureQueriesContext(connection) as queries:
            self.client.post(f"/leave/request-approve/{req.id}/")

        self.assertTrue(
            any("FOR UPDATE" in q["sql"] for q in queries.captured_queries),
            "leave approval must lock AvailableLeave",
        )
