

"use strict";

// ── Utility: show / hide error messages ──────────────────────────────────────
function showError(fieldId, message) {
  const field = document.getElementById(fieldId);
  const errorEl = document.getElementById(fieldId + "Error");
  if (field)  field.classList.add("invalid"),   field.classList.remove("valid");
  if (errorEl) errorEl.textContent = message, errorEl.classList.add("visible");
}

function clearError(fieldId) {
  const field = document.getElementById(fieldId);
  const errorEl = document.getElementById(fieldId + "Error");
  if (field)  field.classList.remove("invalid");
  if (errorEl) errorEl.textContent = "", errorEl.classList.remove("visible");
}

function markValid(fieldId) {
  const field = document.getElementById(fieldId);
  if (field) field.classList.add("valid"), field.classList.remove("invalid");
  clearError(fieldId);
}

// ── Individual field validators ──────────────────────────────────────────────

function validateName() {
  const val = document.getElementById("studentName").value.trim();
  if (val === "") {
    showError("studentName", "Student name cannot be empty.");
    return false;
  }
  if (val.length < 2) {
    showError("studentName", "Name must be at least 2 characters.");
    return false;
  }
  if (!/^[A-Za-z\s'-]+$/.test(val)) {
    showError("studentName", "Name should contain letters only.");
    return false;
  }
  markValid("studentName");
  return true;
}

function validateEmail() {
  const val = document.getElementById("email").value.trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (val === "") {
    showError("email", "Email ID cannot be empty.");
    return false;
  }
  if (!emailRegex.test(val)) {
    showError("email", "Enter a valid email address (e.g. name@domain.com).");
    return false;
  }
  markValid("email");
  return true;
}

function validateMobile() {
  const val = document.getElementById("mobile").value.trim();
  const mobileRegex = /^[6-9]\d{9}$/;   // Indian mobile: starts 6-9, 10 digits
  if (val === "") {
    showError("mobile", "Mobile number cannot be empty.");
    return false;
  }
  if (!/^\d+$/.test(val)) {
    showError("mobile", "Mobile number must contain digits only.");
    return false;
  }
  if (!mobileRegex.test(val)) {
    showError("mobile", "Enter a valid 10-digit mobile number.");
    return false;
  }
  markValid("mobile");
  return true;
}

function validateDepartment() {
  const val = document.getElementById("department").value;
  if (!val || val === "") {
    showError("department", "Please select a department.");
    return false;
  }
  markValid("department");
  return true;
}

function validateGender() {
  const selected = document.querySelector('input[name="gender"]:checked');
  const errorEl  = document.getElementById("genderError");
  if (!selected) {
    if (errorEl) errorEl.textContent = "Please select a gender option.", errorEl.classList.add("visible");
    return false;
  }
  if (errorEl) errorEl.textContent = "", errorEl.classList.remove("visible");
  return true;
}

function validateFeedback() {
  const val   = document.getElementById("feedback").value.trim();
  const words = val.split(/\s+/).filter(w => w.length > 0);
  if (val === "") {
    showError("feedback", "Feedback comments cannot be blank.");
    return false;
  }
  if (words.length < 10) {
    showError("feedback", `Please enter at least 10 words. (${words.length}/10 words written)`);
    return false;
  }
  markValid("feedback");
  return true;
}

// ── Live word counter for feedback textarea ───────────────────────────────────
function updateWordCount() {
  const val   = document.getElementById("feedback").value.trim();
  const words = val === "" ? 0 : val.split(/\s+/).filter(w => w.length > 0).length;
  const hint  = document.getElementById("wordCount");
  if (hint) {
    hint.textContent = `${words} word${words !== 1 ? "s" : ""} (min. 10 required)`;
    hint.style.color = words >= 10 ? "var(--success)" : "var(--text-muted)";
  }
}

// ── Radio pill highlight ──────────────────────────────────────────────────────
function setupRadioHighlight() {
  document.querySelectorAll('input[name="gender"]').forEach(radio => {
    radio.addEventListener("change", function () {
      document.querySelectorAll(".radio-label").forEach(l => l.classList.remove("selected"));
      if (this.checked) this.closest(".radio-label").classList.add("selected");
      validateGender();
    });
  });
}

// ── Full form validation ──────────────────────────────────────────────────────
function validateForm(event) {
  event.preventDefault();

  const checks = [
    validateName(),
    validateEmail(),
    validateMobile(),
    validateDepartment(),
    validateGender(),
    validateFeedback()
  ];

  if (checks.every(Boolean)) {
    showSuccessToast();
    return true;   // allow programmatic submission in tests
  }

  // Scroll to first error
  const firstInvalid = document.querySelector(".invalid, .error-msg.visible");
  if (firstInvalid) firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
  return false;
}

// ── Reset handler ─────────────────────────────────────────────────────────────
function resetForm() {
  ["studentName", "email", "mobile", "department", "feedback"].forEach(id => {
    clearError(id);
    const el = document.getElementById(id);
    if (el) el.classList.remove("valid", "invalid");
  });
  document.getElementById("genderError").textContent = "";
  document.getElementById("genderError").classList.remove("visible");
  document.querySelectorAll(".radio-label").forEach(l => l.classList.remove("selected"));
  updateWordCount();
}

// ── Success Banner (permanent, inside form, form stays open) ─────────────────
function showSuccessToast() {
  const name  = document.getElementById("studentName").value.trim();
  const email = document.getElementById("email").value.trim();

  // Show the fixed bottom toast briefly
  const toast = document.getElementById("successToast");
  if (toast) {
    toast.innerHTML = `✅ <strong>Feedback Submitted!</strong><br><span style="font-size:12px;opacity:.85">Thank you, ${name.split(" ")[0]}. Your response has been recorded.</span>`;
    toast.style.display = "block";
    // Do NOT auto-hide — keep it visible
  }

  // Show the in-form success banner
  const banner = document.getElementById("successBanner");
  if (banner) {
    banner.innerHTML = `
      <div class="success-icon">✓</div>
      <div class="success-text">
        <strong>Feedback Submitted Successfully!</strong>
        <p>Thank you, <em>${name}</em>. Your feedback has been recorded and sent to <em>${email}</em>. The form remains open — you may update and resubmit anytime.</p>
      </div>`;
    banner.style.display = "flex";
    banner.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

// ── Progress indicator (optional visual feedback) ─────────────────────────────
function updateProgress() {
  const fields   = ["studentName", "email", "mobile", "department", "feedback"];
  const total    = fields.length + 1;   // +1 for gender
  let   filled   = 0;
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el && el.value.trim() !== "") filled++;
  });
  if (document.querySelector('input[name="gender"]:checked')) filled++;

  document.querySelectorAll(".p-dot").forEach((dot, i) => {
    dot.classList.toggle("active", i < Math.round((filled / total) * 5));
  });
}

// ── Attach live listeners after DOM load ──────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  // Inline blur-validation
  document.getElementById("studentName")?.addEventListener("blur",   validateName);
  document.getElementById("email")      ?.addEventListener("blur",   validateEmail);
  document.getElementById("mobile")     ?.addEventListener("blur",   validateMobile);
  document.getElementById("department") ?.addEventListener("change", validateDepartment);
  document.getElementById("feedback")   ?.addEventListener("blur",   validateFeedback);
  document.getElementById("feedback")   ?.addEventListener("input",  () => { updateWordCount(); updateProgress(); });

  // Live input listeners for progress
  ["studentName","email","mobile"].forEach(id =>
    document.getElementById(id)?.addEventListener("input", updateProgress)
  );

  setupRadioHighlight();
  updateWordCount();
  updateProgress();

  // Form submit & reset
  document.getElementById("feedbackForm") ?.addEventListener("submit", validateForm);
  document.getElementById("resetBtn")     ?.addEventListener("click",  resetForm);
});