# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from omnexa_core.omnexa_core.branch_access import get_allowed_branches


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.get("company"):
		frappe.throw(_("Company filter is required."), title=_("Filters"))

	conditions = ["company = %(company)s"]
	if filters.get("branch"):
		conditions.append("branch = %(branch)s")

	allowed = get_allowed_branches(company=filters.company)
	if allowed is not None:
		if not allowed:
			return _columns(), []
		filters.allowed_branches = tuple(allowed)
		conditions.append("branch in %(allowed_branches)s")

	data = frappe.db.sql(
		f"""
		SELECT
			stage,
			COUNT(*) AS opportunities,
			SUM(deal_value) AS pipeline_value
		FROM `tabCRM Opportunity`
		WHERE {' AND '.join(conditions)}
		GROUP BY stage
		ORDER BY pipeline_value DESC
		""",
		filters,
		as_dict=True,
	)
	return _columns(), data


def _columns():
	return [
		{"label": _("Stage"), "fieldname": "stage", "fieldtype": "Data", "width": 140},
		{"label": _("Opportunities"), "fieldname": "opportunities", "fieldtype": "Int", "width": 120},
		{"label": _("Pipeline Value"), "fieldname": "pipeline_value", "fieldtype": "Currency", "width": 140},
	]

