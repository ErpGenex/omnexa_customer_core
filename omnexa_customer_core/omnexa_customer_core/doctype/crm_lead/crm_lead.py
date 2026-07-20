# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CRMLead(Document):
	def validate(self):
		self._validate_branch_company_match()
		self._validate_score()

	def _validate_branch_company_match(self):
		branch_company = frappe.db.get_value("Branch", self.branch, "company")
		if not branch_company:
			frappe.throw(_("Branch does not exist."), title=_("Branch"))
		if branch_company != self.company:
			frappe.throw(_("Branch belongs to another company."), title=_("Branch"))

	def _validate_score(self):
		if flt(self.lead_score) < 0 or flt(self.lead_score) > 100:
			frappe.throw(_("Lead Score must be between 0 and 100."), title=_("Lead Score"))

