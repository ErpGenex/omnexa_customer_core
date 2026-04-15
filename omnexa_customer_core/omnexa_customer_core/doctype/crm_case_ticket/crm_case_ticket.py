# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime


class CRMCaseTicket(Document):
	def validate(self):
		self._validate_branch_company_match()
		self._sync_sla_breach()

	def _validate_branch_company_match(self):
		branch_company = frappe.db.get_value("Branch", self.branch, "company")
		if not branch_company:
			frappe.throw(_("Branch does not exist."), title=_("Branch"))
		if branch_company != self.company:
			frappe.throw(_("Branch belongs to another company."), title=_("Branch"))

	def _sync_sla_breach(self):
		if not self.sla_due_date:
			self.is_sla_breached = 0
			return
		now_dt = get_datetime()
		due_dt = get_datetime(self.sla_due_date)
		self.is_sla_breached = 1 if self.status not in ("Resolved", "Closed") and now_dt > due_dt else 0

