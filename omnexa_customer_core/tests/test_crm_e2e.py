# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import random_string

from omnexa_core.tests.test_helpers import clear_privileged_view_context


class TestCRME2E(FrappeTestCase):
	def setUp(self):
		super().setUp()
		clear_privileged_view_context()
		self.company = frappe.db.get_value("Company", {}, "name", order_by="creation asc")
		if not self.company:
			self.skipTest("No company")
		self.branch = frappe.db.get_value(
			"Branch", {"company": self.company, "status": "Active"}, "name", order_by="creation asc"
		)
		if not self.branch:
			self.skipTest("No branch")

	def test_crm_lead_create_and_validate_score(self):
		lead = frappe.new_doc("CRM Lead")
		lead.company = self.company
		lead.branch = self.branch
		lead.lead_name = f"Lead {random_string(5)}"
		lead.lead_score = 75
		lead.insert(ignore_permissions=True)
		self.assertTrue(frappe.db.exists("CRM Lead", lead.name))

	def test_crm_lead_rejects_invalid_score(self):
		lead = frappe.new_doc("CRM Lead")
		lead.company = self.company
		lead.branch = self.branch
		lead.lead_name = f"Bad {random_string(4)}"
		lead.lead_score = 150
		with self.assertRaises(frappe.ValidationError):
			lead.insert(ignore_permissions=True)

	def test_crm_pipeline_report_runs(self):
		from omnexa_customer_core.omnexa_customer_core.report.crm_pipeline_value.crm_pipeline_value import (
			execute,
		)

		out = execute({"company": self.company})
		cols, data = out[0], out[1]
		self.assertTrue(cols)
		self.assertIsInstance(data, list)

	def test_preview_sector_kpi_api(self):
		from omnexa_customer_core.api import preview_sector_kpi

		frappe.set_user("Administrator")
		out = preview_sector_kpi()
		self.assertIsInstance(out, dict)
