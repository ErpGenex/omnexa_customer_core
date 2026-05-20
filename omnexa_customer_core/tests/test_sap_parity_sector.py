# Copyright (c) 2026, ErpGenEx
from frappe.tests.utils import FrappeTestCase

from omnexa_core.omnexa_core.vertical_parity import preview_for_vertical


class TestSapParitySector(FrappeTestCase):
	def test_vertical_kpi_preview(self):
		out = preview_for_vertical("customer_core", stages=[{'amount': 1000, 'probability': 0.5}])
		self.assertEqual(out["vertical"], "customer_core")
		self.assertIn("kpi", out)
		self.assertIn("sap_module", out)
