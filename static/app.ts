import { validateName, validateEmail, validatePassword, validateTextInput, validateDate } from "./validation.js";

// SIGNUP VALIDATION
const signupForm = document.getElementById("form_signup");

if (signupForm) { 
  signupForm.addEventListener("submit", (e: Event) => {
  e.preventDefault();

  validateName((document.getElementById("user_first_name") as HTMLInputElement).value, "First name", "error_first_name", 2, 20);
  validateName((document.getElementById("user_last_name") as HTMLInputElement).value, "Last name", "error_last_name", 2, 20);
  validateEmail((document.getElementById("user_email") as HTMLInputElement).value, "error_email");
  validatePassword((document.getElementById("user_password") as HTMLInputElement).value, "error_password", 8, 50);
})
  // Input event listeners for each field that clear the error when the user types
  document.getElementById("user_first_name")?.addEventListener("input", () => { document.getElementById("error_first_name").textContent = ""; });
  document.getElementById("user_last_name")?.addEventListener("input", () => { document.getElementById("error_last_name").textContent = ""; });
  document.getElementById("user_email")?.addEventListener("input", () => { document.getElementById("error_email").textContent = ""; });
  document.getElementById("user_password")?.addEventListener("input", () => { document.getElementById("error_password").textContent = ""; });
};

// LOGIN VALIDATION
const loginForm = document.getElementById("form_login");

if (loginForm) { 
  loginForm.addEventListener("submit", (e: Event) => {
  e.preventDefault();

  validateEmail((document.getElementById("user_email") as HTMLInputElement).value, "error_email");
  validatePassword((document.getElementById("user_password") as HTMLInputElement).value, "error_password", 8, 50);
})

  document.getElementById("user_email")?.addEventListener("input", () => { document.getElementById("error_email").textContent = ""; });
  document.getElementById("user_password")?.addEventListener("input", () => { document.getElementById("error_password").textContent = ""; });
};

// TRAVEL VALIDATION
const travelForm = document.getElementById("form_travel");

if (travelForm) { 
  travelForm.addEventListener("submit", (e: Event) => {
  e.preventDefault();

  validateTextInput((document.getElementById("travel_location") as HTMLInputElement).value, "Location", "error_travel_location", 2, 50);
  validateTextInput((document.getElementById("travel_title") as HTMLInputElement).value, "Title", "error_travel_title", 2, 50);
  validateDate((document.getElementById("travel_arrival_date") as HTMLInputElement).value, "Arrival", "error_travel_arrival_date");
  validateDate((document.getElementById("travel_departure_date") as HTMLInputElement).value, "Departure", "error_travel_departure_date");
})
  
  document.getElementById("travel_location")?.addEventListener("input", () => { document.getElementById("error_travel_location").textContent = ""; });
  document.getElementById("travel_title")?.addEventListener("input", () => { document.getElementById("error_travel_title").textContent = ""; });
  document.getElementById("travel_arrival_date")?.addEventListener("input", () => { document.getElementById("error_travel_arrival_date").textContent = ""; });
  document.getElementById("travel_departure_date")?.addEventListener("input", () => { document.getElementById("error_travel_departure_date").textContent = ""; });
};

