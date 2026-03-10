export const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const nameRegex = /^[a-zA-ZÀ-ÖØ-öø-ÿ\s'-]+$/;
export function addError(errorMessage, elementId) {
    const li = document.createElement("li");
    li.textContent = errorMessage;
    document.getElementById(elementId).appendChild(li);
}
export function validateName(value, label, errorId, min, max) {
    document.getElementById(errorId).textContent = "";
    const trimmed = value.trim();
    if (trimmed === "") {
        addError(`${label} must be filled out`, errorId);
    }
    else if (trimmed.length < min) {
        addError(`${label} must be more than ${min} characters`, errorId);
    }
    else if (trimmed.length > max) {
        addError(`${label} must be less than ${max} characters`, errorId);
    }
    else if (!nameRegex.test(trimmed)) {
        addError(`${label} can only contain letters`, errorId);
    }
}
export function validateEmail(value, errorId) {
    document.getElementById(errorId).textContent = "";
    const trimmed = value.trim();
    if (trimmed === "") {
        addError("Email must be filled out", errorId);
    }
    else if (!emailRegex.test(trimmed)) {
        addError("Email must be valid", errorId);
    }
}
export function validatePassword(value, errorId, min, max) {
    document.getElementById(errorId).textContent = "";
    const trimmed = value.trim();
    if (trimmed === "") {
        addError("Password must be filled out", errorId);
    }
    else if (trimmed.length < min) {
        addError(`Password must be more than ${min} characters`, errorId);
    }
    else if (trimmed.length > max) {
        addError(`Password must be less than ${max} characters`, errorId);
    }
}
export function validateTextInput(value, label, errorId, min, max) {
    document.getElementById(errorId).textContent = "";
    const trimmed = value.trim();
    if (trimmed === "") {
        addError(`${label} must be filled out`, errorId);
    }
    else if (trimmed.length < min) {
        addError(`${label} must be more than ${min} characters`, errorId);
    }
    else if (trimmed.length > max) {
        addError(`${label} must be less than ${max} characters`, errorId);
    }
}
export function validateDate(value, label, errorId) {
    document.getElementById(errorId).textContent = "";
    if (!value) {
        addError(`${label} date must be filled out`, errorId);
    }
}
//# sourceMappingURL=validation.js.map