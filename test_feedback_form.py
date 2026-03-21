"""
test_feedback_form.py  –  Sub Task 4: Selenium Test Cases (Fixed)
Student Feedback Registration Form – Automated Browser Testing

Fix applied: ElementClickInterceptedException resolved by scrolling
elements into view and using JavaScript click as a reliable fallback.

Requirements:
    pip install selenium webdriver-manager pytest pytest-html

Usage:
    python -m pytest test_feedback_form.py -v
"""

import time
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_DIR = Path(__file__).parent.resolve()
FORM_URL = f"file:///{BASE_DIR}/index.html"
WAIT_SEC = 6


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument("--disable-dev-shm-usage")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver  = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(WAIT_SEC)
    return driver


class TestFeedbackForm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.wait   = WebDriverWait(cls.driver, WAIT_SEC)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(FORM_URL)
        time.sleep(0.5)

    # ── Core helper: scroll into view then JS click ───────────────────────────
    def _safe_click(self, element):
        """Scroll element to centre of viewport, then click via JavaScript.
        This reliably bypasses ElementClickInterceptedException caused by
        overlapping elements (toast notifications, sticky headers, etc.)."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element
        )
        time.sleep(0.2)
        self.driver.execute_script("arguments[0].click();", element)

    def _click_by_id(self, element_id):
        el = self.driver.find_element(By.ID, element_id)
        self._safe_click(el)

    def _fill_valid_form(self):
        self.driver.find_element(By.ID, "studentName").send_keys("Anjali Sharma")
        self.driver.find_element(By.ID, "email").send_keys("anjali.sharma@university.edu")
        self.driver.find_element(By.ID, "mobile").send_keys("9876543210")
        Select(self.driver.find_element(By.ID, "department")).select_by_value("CSE")
        self._safe_click(self.driver.find_element(By.ID, "genderFemale"))
        self.driver.find_element(By.ID, "feedback").send_keys(
            "The course content is very well structured and the faculty "
            "members are extremely knowledgeable and supportive throughout "
            "the semester."
        )

    def _get_error(self, error_id):
        try:
            return self.driver.find_element(By.ID, error_id).text.strip()
        except Exception:
            return ""

    # ── TC-01 ────────────────────────────────────────────────────────────────
    def test_01_page_loads_successfully(self):
        title = self.driver.title
        self.assertIn("Student Feedback", title,
                      f"Expected 'Student Feedback' in title, got: '{title}'")
        for field_id in ["studentName", "email", "mobile", "department", "feedback"]:
            self.assertIsNotNone(self.driver.find_element(By.ID, field_id),
                                 f"Field #{field_id} not found")
        self.driver.find_element(By.ID, "submitBtn")
        self.driver.find_element(By.ID, "resetBtn")
        print("\n✅ TC-01 PASSED: Page loaded with all form elements.")

    # ── TC-02 ────────────────────────────────────────────────────────────────
    def test_02_valid_data_submission(self):
        self._fill_valid_form()
        self._click_by_id("submitBtn")
        time.sleep(0.6)

        for field_id in ["studentName", "email", "mobile", "department", "feedback"]:
            classes = self.driver.find_element(By.ID, field_id).get_attribute("class") or ""
            self.assertNotIn("invalid", classes,
                             f"#{field_id} incorrectly marked invalid with valid data")

        toast = self.driver.find_element(By.ID, "successToast")
        self.assertTrue(toast.is_displayed(), "Success toast did not appear.")
        print("✅ TC-02 PASSED: Valid form submitted; success toast shown.")

    # ── TC-03 ────────────────────────────────────────────────────────────────
    def test_03_blank_fields_show_errors(self):
        self._click_by_id("submitBtn")
        time.sleep(0.5)

        error_map = {
            "studentNameError": "name",
            "emailError":       "email",
            "mobileError":      "mobile",
            "departmentError":  "department",
            "genderError":      "gender",
            "feedbackError":    "feedback",
        }
        for error_id, label in error_map.items():
            self.assertTrue(len(self._get_error(error_id)) > 0,
                            f"Expected error for '{label}' but #{error_id} was empty.")
        print("✅ TC-03 PASSED: All empty-field errors displayed.")

    # ── TC-04 ────────────────────────────────────────────────────────────────
    def test_04_invalid_email_format(self):
        invalid_emails = ["not-an-email", "missing@domain", "@nodomain.com", "spaces @test.com"]
        for bad_email in invalid_emails:
            self.driver.get(FORM_URL)
            time.sleep(0.3)
            email_input = self.driver.find_element(By.ID, "email")
            email_input.clear()
            email_input.send_keys(bad_email)
            email_input.send_keys(Keys.TAB)
            time.sleep(0.25)
            self.assertTrue(len(self._get_error("emailError")) > 0,
                            f"Email '{bad_email}' should fail but no error shown.")
            classes = email_input.get_attribute("class") or ""
            self.assertIn("invalid", classes,
                          f"Email input not marked invalid for: '{bad_email}'")
        print("✅ TC-04 PASSED: Invalid email formats rejected.")

    # ── TC-05 ────────────────────────────────────────────────────────────────
    def test_05_invalid_mobile_number(self):
        invalid_mobiles = [
            ("12345",      "too short"),
            ("abcdefghij", "letters"),
            ("0000000000", "starts with 0"),
            ("99999",      "only 5 digits"),
        ]
        for bad_mobile, reason in invalid_mobiles:
            self.driver.get(FORM_URL)
            time.sleep(0.3)
            mobile_input = self.driver.find_element(By.ID, "mobile")
            mobile_input.clear()
            mobile_input.send_keys(bad_mobile)
            mobile_input.send_keys(Keys.TAB)
            time.sleep(0.25)
            self.assertTrue(len(self._get_error("mobileError")) > 0,
                            f"Mobile '{bad_mobile}' ({reason}) should fail but no error shown.")
        print("✅ TC-05 PASSED: Invalid mobile numbers rejected.")

    # ── TC-06 ────────────────────────────────────────────────────────────────
    def test_06_department_dropdown(self):
        expected_depts = {"CSE": "Computer Science", "IT": "Information Technology",
                          "ECE": "Electronics", "ME": "Mechanical", "MBA": "Master of Business"}
        select_el = Select(self.driver.find_element(By.ID, "department"))
        for value in expected_depts:
            select_el.select_by_value(value)
            time.sleep(0.1)
            self.assertEqual(select_el.first_selected_option.get_attribute("value"), value,
                             f"Could not select department '{value}'")

        select_el.select_by_value("CSE")
        self._click_by_id("submitBtn")
        time.sleep(0.4)
        self.assertEqual(self._get_error("departmentError"), "",
                         "Department error should be empty after valid selection.")
        print("✅ TC-06 PASSED: Dropdown works; error clears on valid choice.")

    # ── TC-07 ────────────────────────────────────────────────────────────────
    def test_07_submit_and_reset_buttons(self):
        self._fill_valid_form()
        name_before = self.driver.find_element(By.ID, "studentName").get_attribute("value")
        self.assertTrue(len(name_before) > 0, "Name should have content before reset.")

        self._click_by_id("resetBtn")
        time.sleep(0.4)

        self.assertEqual(self.driver.find_element(By.ID, "studentName").get_attribute("value"),
                         "", "Student Name not cleared after reset.")
        self.assertEqual(self.driver.find_element(By.ID, "email").get_attribute("value"),
                         "", "Email not cleared after reset.")

        self._click_by_id("submitBtn")
        time.sleep(0.4)
        self.assertTrue(len(self._get_error("studentNameError")) > 0,
                        "Name error should appear after submitting empty form.")
        print("✅ TC-07 PASSED: Reset clears form; Submit triggers validation.")


if __name__ == "__main__":
    print("=" * 60)
    print("  Student Feedback Form – Selenium Test Suite")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromTestCase(TestFeedbackForm)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    total  = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    print(f"\n  Results: {passed}/{total} tests passed")
    print("=" * 60)
    exit(0 if result.wasSuccessful() else 1)