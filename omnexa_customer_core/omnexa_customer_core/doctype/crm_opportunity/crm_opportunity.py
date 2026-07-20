# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CRMOpportunity(Document):
	def validate(self):
		self._validate_branch_company_match()
		self._validate_probability()
		self._sync_status_from_stage()

	def _validate_branch_company_match(self):
		branch_company = frappe.db.get_value("Branch", self.branch, "company")
		if not branch_company:
			frappe.throw(_("Branch does not exist."), title=_("Branch"))
		if branch_company != self.company:
			frappe.throw(_("Branch belongs to another company."), title=_("Branch"))

	def _validate_probability(self):
		if flt(self.probability_percent) < 0 or flt(self.probability_percent) > 100:
			frappe.throw(_("Probability must be between 0 and 100."), title=_("Probability"))

	def _sync_status_from_stage(self):
		if self.stage == "Won":
			self.status = "Won"
			self.probability_percent = 100
		elif self.stage == "Lost":
			self.status = "Lost"
			self.probability_percent = 0
		elif self.status not in ("Won", "Lost"):
			self.status = "Open"

