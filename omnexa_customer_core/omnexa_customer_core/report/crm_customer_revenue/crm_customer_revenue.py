# Copyright (c) 2026, Omnexa and contributors
# License: See license.txt

import frappe
from frappe import _
from omnexa_core.omnexa_core.branch_access import get_allowed_branches


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.get("company"):
		frappe.throw(_("Company filter is required."), title=_("Filters"))

	conditions = ["cp.company = %(company)s"]
	if filters.get("branch"):
		conditions.append("cp.branch = %(branch)s")

	allowed = get_allowed_branches(company=filters.company)
	if allowed is not None:
		if not allowed:
			return _columns(), []
		filters.allowed_branches = tuple(allowed)
		conditions.append("cp.branch in %(allowed_branches)s")

	data = frappe.db.sql(
		f"""
		SELECT
			cp.name AS customer_profile,
			cp.customer_name,
			cp.branch,
			COALESCE(SUM(si.grand_total), 0) AS total_revenue,
			COALESCE(SUM(si.outstanding_amount), 0) AS outstanding_balance
		FROM `tabCustomer Profile` cp
		LEFT JOIN `tabSales Invoice` si
			ON si.customer = cp.linked_customer AND si.company = cp.company AND si.docstatus = 1
		WHERE {' AND '.join(conditions)}
		GROUP BY cp.name, cp.customer_name, cp.branch
		ORDER BY total_revenue DESC
		""",
		filters,
		as_dict=True,
	)
	return _columns(), data


def _columns():
	return [
		{"label": _("Customer Profile"), "fieldname": "customer_profile", "fieldtype": "Link", "options": "Customer Profile", "width": 150},
		{"label": _("Customer Name"), "fieldname": "customer_name", "fieldtype": "Data", "width": 180},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 120},
		{"label": _("Total Revenue"), "fieldname": "total_revenue", "fieldtype": "Currency", "width": 140},
		{"label": _("Outstanding"), "fieldname": "outstanding_balance", "fieldtype": "Currency", "width": 130},
	]

