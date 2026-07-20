# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate


class CRMCampaign(Document):
	def validate(self):
		self._validate_branch_company_match()
		self._validate_dates()
		self._set_roi()

	def _validate_branch_company_match(self):
		branch_company = frappe.db.get_value("Branch", self.branch, "company")
		if not branch_company:
			frappe.throw(_("Branch does not exist."), title=_("Branch"))
		if branch_company != self.company:
			frappe.throw(_("Branch belongs to another company."), title=_("Branch"))

	def _validate_dates(self):
		if getdate(self.end_date) < getdate(self.start_date):
			frappe.throw(_("End Date cannot be before Start Date."), title=_("Campaign"))

	def _set_roi(self):
		cost = flt(self.campaign_cost)
		revenue = flt(self.generated_revenue)
		self.roi_percent = flt(((revenue - cost) / cost) * 100.0, 2) if cost > 0 else 0

