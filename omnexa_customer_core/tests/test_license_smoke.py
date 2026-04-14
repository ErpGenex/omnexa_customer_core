from frappe.tests.utils import FrappeTestCase

from omnexa_customer_core import hooks, license_gate


class TestCustomerCoreLicenseSmoke(FrappeTestCase):
	def test_license_gate_is_wired(self):
		self.assertEqual(hooks.before_request, ["omnexa_customer_core.license_gate.before_request"])
		self.assertEqual(license_gate._APP, "omnexa_customer_core")
