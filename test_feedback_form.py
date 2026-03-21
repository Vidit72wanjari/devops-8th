"""
test_feedback_form.py  –  Sub Task 4: Selenium Test Cases
Student Feedback Registration Form

Flow:
  TC-01  Verify blank form opens correctly
  TC-02  Type all fields once → click Submit → success banner stays visible
  TC-03  Clear fields → Submit → all errors appear
  TC-04  Invalid email values tested in-place
  TC-05  Invalid mobile values tested in-place
  TC-06  Department dropdown cycled
  TC-07  Reset button clears form, Submit on blank triggers errors

Usage:
    python -m pytest test_feedback_form.py -v
"""

import time
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_DIR = Path(__file__).parent.resolve()
FORM_URL  = f"file:///{BASE_DIR}/index.html"
WAIT_SEC  = 6


def get_driver():
    import os
    chrome_options = Options()
    if os.environ.get("CI") or os.environ.get("JENKINS_URL"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1280,900")
    else:
        chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
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
        """Open browser and load the blank form ONCE for all tests."""
        cls.driver = get_driver()
        cls.wait   = WebDriverWait(cls.driver, WAIT_SEC)
        cls.driver.get(FORM_URL)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

    # ── No setUp() — page is never reloaded between tests ────────────────

    # ══════════════════════════════════════════════════════════════════════
    #  Helpers
    # ══════════════════════════════════════════════════════════════════════

    def _safe_click(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'center'});",
            element)
        time.sleep(0.2)
        self.driver.execute_script("arguments[0].click();", element)

    def _click_by_id(self, eid):
        self._safe_click(self.driver.find_element(By.ID, eid))

    def _set_value(self, field_id, text):
        el = self.driver.find_element(By.ID, field_id)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input',  {bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            el, text)

    def _blur(self, field_id):
        el = self.driver.find_element(By.ID, field_id)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('blur',{bubbles:true}));", el)

    def _get_error(self, error_id):
        try:
            return self.driver.find_element(By.ID, error_id).text.strip()
        except Exception:
            return ""

    def _clear_all_fields(self):
        """Wipe every field via JS without reloading the page."""
        for fid in ["studentName", "email", "mobile", "feedback"]:
            self._set_value(fid, "")
        dept = self.driver.find_element(By.ID, "department")
        self.driver.execute_script(
            "arguments[0].value = '';"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
            dept)
        self.driver.execute_script(
            "document.querySelectorAll('input[name=\"gender\"]')"
            ".forEach(r => r.checked = false);"
            "document.querySelectorAll('.radio-label')"
            ".forEach(l => l.classList.remove('selected'));"
            "var ge = document.getElementById('genderError');"
            "if(ge){ ge.textContent=''; ge.classList.remove('visible'); }")
        # Hide success banner / toast from previous test
        self.driver.execute_script(
            "var b = document.getElementById('successBanner');"
            "if(b) b.style.display='none';"
            "var t = document.getElementById('successToast');"
            "if(t) t.style.display='none';")
        # Remove valid/invalid classes
        self.driver.execute_script(
            "['studentName','email','mobile','department','feedback'].forEach(id => {"
            "  var el = document.getElementById(id);"
            "  if(el){ el.classList.remove('valid','invalid'); }"
            "});")

    # ══════════════════════════════════════════════════════════════════════
    #  TC-01  Blank form opens
    # ══════════════════════════════════════════════════════════════════════
    def test_01_page_loads_successfully(self):
        """Form opens blank — all fields empty, all elements present."""
        self.assertIn("Student Feedback", self.driver.title)

        for fid in ["studentName", "email", "mobile", "department", "feedback"]:
            el  = self.driver.find_element(By.ID, fid)
            val = el.get_attribute("value") or ""
            self.assertEqual(val, "", f"Field #{fid} should be blank on load, got '{val}'")

        self.driver.find_element(By.ID, "submitBtn")
        self.driver.find_element(By.ID, "resetBtn")
        time.sleep(1.5)   # viewer sees the blank form
        print("\n✅ TC-01 PASSED: Blank form opened successfully.")

    # ══════════════════════════════════════════════════════════════════════
    #  TC-02  Fill form once and submit
    # ══════════════════════════════════════════════════════════════════════
    def test_02_valid_data_submission(self):
        """
        Type all fields with Vidit's details ONCE, click Submit.
        Success banner appears. Form stays open (not closed/reset).
        """
        # — Type each field with a small pause so it's visible —
        self._set_value("studentName", "Vidit Wanjari")
        time.sleep(0.4)

        self._set_value("email", "viditwanjari12345@gmail.com")
        time.sleep(0.4)

        self._set_value("mobile", "7888043526")
        time.sleep(0.4)

        Select(self.driver.find_element(By.ID, "department")).select_by_value("CSE")
        time.sleep(0.4)

        self._safe_click(self.driver.find_element(By.ID, "genderMale"))
        time.sleep(0.4)

        self._set_value("feedback",
            "The teaching methodology is excellent and the faculty members are "
            "very supportive and knowledgeable. The lab infrastructure is well "
            "equipped and the course content is up to date with industry standards.")
        time.sleep(0.6)   # viewer sees fully filled form

        # Click Submit
        self._click_by_id("submitBtn")
        time.sleep(2)     # viewer sees the success banner clearly

        # Assertions
        for fid in ["studentName", "email", "mobile", "department", "feedback"]:
            classes = self.driver.find_element(By.ID, fid).get_attribute("class") or ""
            self.assertNotIn("invalid", classes,
                             f"#{fid} incorrectly marked invalid with valid data")

        toast = self.driver.find_element(By.ID, "successToast")
        self.assertTrue(toast.is_displayed(), "Success toast did not appear.")
        print("✅ TC-02 PASSED: Form filled once and submitted. Success banner visible.")

    # ══════════════════════════════════════════════════════════════════════
    #  TC-03  Blank submission shows errors
    # ══════════════════════════════════════════════════════════════════════
    def test_03_blank_fields_show_errors(self):
        """Clear all fields in-place, submit, verify all 6 errors appear."""
        self._clear_all_fields()
        time.sleep(0.8)   # viewer sees blank form

        self._click_by_id("submitBtn")
        time.sleep(1)     # viewer sees all error messages

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

    # ══════════════════════════════════════════════════════════════════════
    #  TC-04  Invalid email
    # ══════════════════════════════════════════════════════════════════════
    def test_04_invalid_email_format(self):
        """Test 4 invalid email values in-place — no reload."""
        invalid_emails = [
            "not-an-email",
            "missing@domain",
            "@nodomain.com",
            "spaces @test.com",
        ]
        for bad_email in invalid_emails:
            self._set_value("email", bad_email)
            self._blur("email")
            time.sleep(0.6)
            self.assertTrue(len(self._get_error("emailError")) > 0,
                            f"Email '{bad_email}' should fail.")
            classes = self.driver.find_element(By.ID, "email").get_attribute("class") or ""
            self.assertIn("invalid", classes)

        self._set_value("email", "")
        print("✅ TC-04 PASSED: Invalid email formats rejected.")

    # ══════════════════════════════════════════════════════════════════════
    #  TC-05  Invalid mobile
    # ══════════════════════════════════════════════════════════════════════
    def test_05_invalid_mobile_number(self):
        """Test 4 invalid mobile values in-place — no reload."""
        invalid_mobiles = [
            ("12345",      "too short"),
            ("abcdefghij", "letters"),
            ("0000000000", "starts with 0"),
            ("99999",      "only 5 digits"),
        ]
        for bad_mobile, reason in invalid_mobiles:
            self._set_value("mobile", bad_mobile)
            self._blur("mobile")
            time.sleep(0.6)
            self.assertTrue(len(self._get_error("mobileError")) > 0,
                            f"Mobile '{bad_mobile}' ({reason}) should fail.")

        self._set_value("mobile", "")
        print("✅ TC-05 PASSED: Invalid mobile numbers rejected.")

    # ══════════════════════════════════════════════════════════════════════
    #  TC-06  Department dropdown
    # ══════════════════════════════════════════════════════════════════════
    def test_06_department_dropdown(self):
        """Cycle through all departments, verify each selection works."""
        depts = ["CSE", "IT", "ECE", "ME", "MBA"]
        select_el = Select(self.driver.find_element(By.ID, "department"))
        for value in depts:
            select_el.select_by_value(value)
            time.sleep(0.5)
            self.assertEqual(
                select_el.first_selected_option.get_attribute("value"), value)

        select_el.select_by_value("CSE")
        self._click_by_id("submitBtn")
        time.sleep(0.4)
        self.assertEqual(self._get_error("departmentError"), "")
        print("✅ TC-06 PASSED: Dropdown selections work correctly.")

    # ══════════════════════════════════════════════════════════════════════
    #  TC-07  Reset and Submit buttons
    # ══════════════════════════════════════════════════════════════════════
    def test_07_submit_and_reset_buttons(self):
        """Fill form → Reset clears it → Submit on blank shows errors."""
        # Fill
        self._set_value("studentName", "Anjali Sharma")
        self._set_value("email",       "anjali.sharma@university.edu")
        self._set_value("mobile",      "9876543210")
        Select(self.driver.find_element(By.ID, "department")).select_by_value("IT")
        self._safe_click(self.driver.find_element(By.ID, "genderFemale"))
        self._set_value("feedback",
            "The course content is very well structured and the faculty "
            "members are extremely knowledgeable and supportive throughout "
            "the entire semester.")
        time.sleep(0.8)   # viewer sees filled form

        name_before = self.driver.find_element(By.ID, "studentName").get_attribute("value")
        self.assertTrue(len(name_before) > 0)

        # Reset
        self._click_by_id("resetBtn")
        time.sleep(1)     # viewer sees cleared form

        self.assertEqual(
            self.driver.find_element(By.ID, "studentName").get_attribute("value"), "")
        self.assertEqual(
            self.driver.find_element(By.ID, "email").get_attribute("value"), "")

        # Submit blank → errors
        self._click_by_id("submitBtn")
        time.sleep(1)     # viewer sees errors
        self.assertTrue(len(self._get_error("studentNameError")) > 0)
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