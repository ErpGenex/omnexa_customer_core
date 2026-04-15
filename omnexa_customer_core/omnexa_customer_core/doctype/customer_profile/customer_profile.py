# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CustomerProfile(Document):
	def validate(self):
		self._validate_branch_company_match()
		self._validate_unique_code()
		self._sync_outstanding_balance()
		self._validate_credit_risk_bounds()

	def _validate_branch_company_match(self):
		branch_company = frappe.db.get_value("Branch", self.branch, "company")
		if not branch_company:
			frappe.throw(_("Branch does not exist."), title=_("Branch"))
		if branch_company != self.company:
			frappe.throw(_("Branch belongs to another company."), title=_("Branch"))

	def _validate_unique_code(self):
		existing = frappe.db.get_value(
			"Customer Profile",
			{"company": self.company, "customer_code": self.customer_code},
			"name",
		)
		if existing and existing != self.name:
			frappe.throw(_("Customer Code must be unique per company."), title=_("Duplicate"))

	def _sync_outstanding_balance(self):
		if not self.linked_customer:
			self.outstanding_balance = 0
			return
		outstanding = frappe.db.sql(
			"""
			SELECT COALESCE(SUM(outstanding_amount), 0)
			FROM `tabSales Invoice`
			WHERE customer = %s AND company = %s AND docstatus = 1
			""",
			(self.linked_customer, self.company),
		)[0][0]
		self.outstanding_balance = flt(outstanding, 2)

	def _validate_credit_risk_bounds(self):
		if flt(self.risk_score) < 0 or flt(self.risk_score) > 100:
			frappe.throw(_("Risk Score must be between 0 and 100."), title=_("Risk Score"))

