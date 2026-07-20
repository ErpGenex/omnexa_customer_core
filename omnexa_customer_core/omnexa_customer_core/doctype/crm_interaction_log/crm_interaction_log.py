# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CRMInteractionLog(Document):
	def validate(self):
		self._validate_branch_company_match()
		self._validate_references()

	def _validate_branch_company_match(self):
		branch_company = frappe.db.get_value("Branch", self.branch, "company")
		if not branch_company:
			frappe.throw(_("Branch does not exist."), title=_("Branch"))
		if branch_company != self.company:
			frappe.throw(_("Branch belongs to another company."), title=_("Branch"))

	def _validate_references(self):
		if not any([self.customer_profile, self.lead, self.opportunity]):
			frappe.throw(_("At least one reference is required: Customer, Lead, or Opportunity."), title=_("Reference"))

