# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `lead_name`, `company`, `branch`, `lead_source`, `lead_status`
		FROM `tabCRM Lead`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Lead Name"), "fieldname": "lead_name", "fieldtype": "Data", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120},
		{"label": _("Lead Source"), "fieldname": "lead_source", "fieldtype": "Select", "width": 120},
		{"label": _("Lead Status"), "fieldname": "lead_status", "fieldtype": "Select", "width": 120}
	]
	return columns, data
