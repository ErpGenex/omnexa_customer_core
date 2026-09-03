# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `opportunity_title`, `company`, `branch`, `stage`, `deal_value`
		FROM `tabCRM Opportunity`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Opportunity Title"), "fieldname": "opportunity_title", "fieldtype": "Data", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120},
		{"label": _("Stage"), "fieldname": "stage", "fieldtype": "Select", "width": 120},
		{"label": _("Deal Value"), "fieldname": "deal_value", "fieldtype": "Currency", "width": 120}
	]
	return columns, data
