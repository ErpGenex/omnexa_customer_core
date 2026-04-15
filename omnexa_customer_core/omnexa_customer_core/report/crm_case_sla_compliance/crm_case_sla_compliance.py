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
			status,
			COUNT(*) AS total_cases,
			SUM(CASE WHEN is_sla_breached = 1 THEN 1 ELSE 0 END) AS breached_cases
		FROM `tabCRM Case Ticket`
		WHERE {' AND '.join(conditions)}
		GROUP BY status
		ORDER BY total_cases DESC
		""",
		filters,
		as_dict=True,
	)
	for row in data:
		row.compliance_percent = ((row.total_cases - row.breached_cases) / row.total_cases * 100.0) if row.total_cases else 0
	return _columns(), data


def _columns():
	return [
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Total Cases"), "fieldname": "total_cases", "fieldtype": "Int", "width": 110},
		{"label": _("Breached"), "fieldname": "breached_cases", "fieldtype": "Int", "width": 100},
		{"label": _("SLA Compliance %"), "fieldname": "compliance_percent", "fieldtype": "Percent", "width": 130},
	]

