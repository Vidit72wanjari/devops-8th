# Student Feedback Registration Form
### Full-Stack Web Project with Selenium Testing & Jenkins CI/CD

---

## Project Structure

```
student-feedback/
├── index.html              ← Sub Task 1 & 2: HTML form + Internal CSS
├── style.css               ← Sub Task 2: External CSS
├── validate.js             ← Sub Task 3: JavaScript validation
├── test_feedback_form.py   ← Sub Task 4: Selenium test cases
├── Jenkinsfile             ← Sub Task 5: Jenkins pipeline
└── README.md               ← This file
```

---

## Sub Task 1 & 2 – Running the Form

Simply open `index.html` in any modern web browser:
```bash
# macOS/Linux
open index.html

# Windows
start index.html
```
The form uses **External CSS** (`style.css`) and **Internal CSS** (the `<style>` block inside `index.html`).

---

## Sub Task 3 – JavaScript Validation

All validations run automatically on form interaction via `validate.js`:

| Field            | Rule                                           |
|------------------|------------------------------------------------|
| Student Name     | Not empty, letters only, min 2 chars          |
| Email ID         | Matches `name@domain.tld` pattern             |
| Mobile Number    | 10 digits, starts with 6–9 (Indian standard)  |
| Department       | A valid option must be selected               |
| Gender           | One radio button must be selected             |
| Feedback         | Not empty, minimum **10 words**               |

---

## Sub Task 4 – Running Selenium Tests

### Prerequisites
```bash
pip install selenium webdriver-manager pytest pytest-html
```
Google Chrome must be installed (ChromeDriver is auto-managed).

### Run Tests
```bash
# Run all 7 test cases with verbose output
pytest test_feedback_form.py -v

# Run with HTML report
pytest test_feedback_form.py -v --html=report.html --self-contained-html
```

### Test Cases

| TC   | Test Name                              | What It Checks                                    |
|------|----------------------------------------|---------------------------------------------------|
| TC-01| `test_01_page_loads_successfully`      | Page opens, all fields & buttons present          |
| TC-02| `test_02_valid_data_submission`        | Valid data submits without errors, toast shown    |
| TC-03| `test_03_blank_fields_show_errors`     | All empty-field error messages fire               |
| TC-04| `test_04_invalid_email_format`         | Bad email formats are rejected                    |
| TC-05| `test_05_invalid_mobile_number`        | Short/non-numeric mobiles are rejected            |
| TC-06| `test_06_department_dropdown`          | All dropdown options can be selected              |
| TC-07| `test_07_submit_and_reset_buttons`     | Submit triggers validation; Reset clears form     |

---

## Sub Task 5 – Jenkins Setup Guide

### Step 1: Install Jenkins
```bash
# macOS (via Homebrew)
brew install jenkins-lts
brew services start jenkins-lts

# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo apt-add-repository "deb https://pkg.jenkins.io/debian binary/"
sudo apt update && sudo apt install jenkins -y
sudo systemctl start jenkins
```
Access Jenkins at: **http://localhost:8080**

### Step 2: Install Required Jenkins Plugins
Go to `Manage Jenkins → Plugins → Available`:
- ✅ Git Plugin
- ✅ Pipeline
- ✅ HTML Publisher Plugin
- ✅ JUnit Plugin
- ✅ AnsiColor Plugin

### Step 3: Create a New Pipeline Job
1. Click **New Item**
2. Enter name: `Student-Feedback-Selenium`
3. Choose **Pipeline** → Click **OK**

### Step 4: Configure the Job

**Option A – From GitHub:**
- Under *Pipeline*, select **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/<your-username>/student-feedback-form.git`
- Branch: `*/main`
- Script Path: `Jenkinsfile`

**Option B – Local Folder:**
- Under *Pipeline*, select **Pipeline script**
- Paste the contents of `Jenkinsfile` directly

### Step 5: Execute the Job
1. Click **Build Now**
2. Watch the **Console Output** for live logs
3. After build: view the **Selenium Test Report** under *Build Artifacts*

### Step 6: Interpret Results
| Console Shows          | Meaning                                |
|------------------------|----------------------------------------|
| `BUILD SUCCESS`        | All 7 Selenium tests passed ✅         |
| `BUILD FAILURE`        | One or more tests failed ❌            |
| `BUILD UNSTABLE`       | Tests ran but with warnings ⚠️         |

---

## Technologies Used

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Structure   | HTML5 (Semantic)                  |
| Styling     | CSS3 (Internal + External)        |
| Validation  | Vanilla JavaScript (ES6+)         |
| Testing     | Python 3, Selenium 4, pytest      |
| CI/CD       | Jenkins (Declarative Pipeline)    |
| Fonts       | Google Fonts (Playfair + DM Sans) |
