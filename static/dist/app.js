var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
import { validateName, validateEmail, validatePassword, validateTextInput, validateDate } from "./validation.js";
// SIGNUP VALIDATION
const signupForm = document.getElementById("form_signup");
if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
        e.preventDefault();
        validateName(document.getElementById("user_first_name").value, "First name", "error_first_name", 2, 20);
        validateName(document.getElementById("user_last_name").value, "Last name", "error_last_name", 2, 20);
        validateEmail(document.getElementById("user_email").value, "error_email");
        validatePassword(document.getElementById("user_password").value, "error_password", 8, 50);
    });
    // Input event listeners for each field that clear the error when the user types
    (_a = document.getElementById("user_first_name")) === null || _a === void 0 ? void 0 : _a.addEventListener("input", () => { document.getElementById("error_first_name").textContent = ""; });
    (_b = document.getElementById("user_last_name")) === null || _b === void 0 ? void 0 : _b.addEventListener("input", () => { document.getElementById("error_last_name").textContent = ""; });
    (_c = document.getElementById("user_email")) === null || _c === void 0 ? void 0 : _c.addEventListener("input", () => { document.getElementById("error_email").textContent = ""; });
    (_d = document.getElementById("user_password")) === null || _d === void 0 ? void 0 : _d.addEventListener("input", () => { document.getElementById("error_password").textContent = ""; });
}
;
// LOGIN VALIDATION
const loginForm = document.getElementById("form_login");
if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        validateEmail(document.getElementById("user_email").value, "error_email");
        validatePassword(document.getElementById("user_password").value, "error_password", 8, 50);
    });
    (_e = document.getElementById("user_email")) === null || _e === void 0 ? void 0 : _e.addEventListener("input", () => { document.getElementById("error_email").textContent = ""; });
    (_f = document.getElementById("user_password")) === null || _f === void 0 ? void 0 : _f.addEventListener("input", () => { document.getElementById("error_password").textContent = ""; });
}
;
// TRAVEL VALIDATION
const travelForm = document.getElementById("form_travel");
if (travelForm) {
    travelForm.addEventListener("submit", (e) => {
        e.preventDefault();
        validateTextInput(document.getElementById("travel_location").value, "Location", "error_travel_location", 2, 50);
        validateTextInput(document.getElementById("travel_title").value, "Title", "error_travel_title", 2, 50);
        validateDate(document.getElementById("travel_arrival_date").value, "Arrival", "error_travel_arrival_date");
        validateDate(document.getElementById("travel_departure_date").value, "Departure", "error_travel_departure_date");
    });
    (_g = document.getElementById("travel_location")) === null || _g === void 0 ? void 0 : _g.addEventListener("input", () => { document.getElementById("error_travel_location").textContent = ""; });
    (_h = document.getElementById("travel_title")) === null || _h === void 0 ? void 0 : _h.addEventListener("input", () => { document.getElementById("error_travel_title").textContent = ""; });
    (_j = document.getElementById("travel_arrival_date")) === null || _j === void 0 ? void 0 : _j.addEventListener("input", () => { document.getElementById("error_travel_arrival_date").textContent = ""; });
    (_k = document.getElementById("travel_departure_date")) === null || _k === void 0 ? void 0 : _k.addEventListener("input", () => { document.getElementById("error_travel_departure_date").textContent = ""; });
}
;
// CONFIRM DELETE BOX
document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("overlay");
    // SHOW confirm box when delete icon is clicked
    document.querySelectorAll(".delete_icon").forEach((deleteBtn) => {
        deleteBtn.addEventListener("click", () => {
            const travelCard = deleteBtn.closest(".travel_card"); // Finds a parent with the class travel_card with .closest()
            const confirmBox = travelCard === null || travelCard === void 0 ? void 0 : travelCard.querySelector(".confirm_delete_box"); // Finds the confirm_delete_box with querySelector() inside the travelCard (? = only do this if it exists).
            confirmBox === null || confirmBox === void 0 ? void 0 : confirmBox.classList.remove("hidden"); // Removes the hidden class from the confirmBox to make it visible
            overlay === null || overlay === void 0 ? void 0 : overlay.classList.remove("hidden"); // Adds an overlay to the background of the page
        });
    });
    // CANCEL - hide the confirm box
    document.querySelectorAll(".cancel_button").forEach((cancelBtn) => {
        cancelBtn.addEventListener("click", () => {
            const confirmBox = cancelBtn.closest(".confirm_delete_box");
            confirmBox === null || confirmBox === void 0 ? void 0 : confirmBox.classList.add("hidden");
            overlay === null || overlay === void 0 ? void 0 : overlay.classList.add("hidden");
        });
    });
    // Remove the overlay when deleting a travel
    document.querySelectorAll(".confirm_delete_button").forEach((confirmBtn) => {
        confirmBtn.addEventListener("click", () => {
            const travelCard = confirmBtn.closest(".travel_card");
            overlay === null || overlay === void 0 ? void 0 : overlay.classList.add("hidden");
        });
    });
});
//# sourceMappingURL=app.js.map