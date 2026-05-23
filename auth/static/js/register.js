const usernameField = document.getElementById('username');
const passwordField = document.getElementById('password');
const confirmPasswordField = document.getElementById('confirm_password');
const submitButton = document.getElementById('submit-button');

// username availability checking
let debounceTimer;
usernameField.addEventListener('input', function () {
    clearTimeout(debounceTimer)

    const username = usernameField.value;
    // guards
    if (username === '') return
    if (username.length < 3 || username.length > 20) return;

    // check username if user stopped typing
    debounceTimer = setTimeout(function () {
        fetch(`/auth/check-username?username=${username}`)
            .then(response => response.json())
            .then(data => {
                if (data['available']) {
                    usernameField.classList.add('is-valid');
                    usernameField.classList.remove('is-invalid');
                } else {
                    usernameField.classList.add('is-invalid');
                    usernameField.classList.remove('is-valid');
                }
            })
    }, 1000);
})

// handle password field.
passwordField.addEventListener('blur', function () {
    const password = passwordField.value;

    if (password.length > 8) {
        passwordField.classList.add('is-valid');
        passwordField.classList.remove('is-invalid');
    } else {
        passwordField.classList.add('is-invalid');
        passwordField.classList.remove('is-valid');
    }
})

// handle confirm password field.
confirmPasswordField.addEventListener('blur', function() {
    if (passwordField.classList.contains('is-valid')) {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;

        if (confirmPassword === password) {
            confirmPasswordField.classList.add('is-valid');
            confirmPasswordField.classList.remove('is-invalid');
        } else {
            confirmPasswordField.classList.add('is-invalid');
            confirmPasswordField.classList.remove('is-valid');
        }
    }
})
confirmPasswordField.addEventListener('input', function () {
    if (confirmPasswordField.classList.contains('is-invalid')) {
        confirmPasswordField.classList.remove('is-invalid')
    }
    if (passwordField.classList.contains('is-valid')) {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;

        if (confirmPassword === password) {
            confirmPasswordField.classList.add('is-valid')
        } else {
            confirmPasswordField.classList.remove('is-valid')
        }
    }
})

// enable/disable submit button based on if the forms are filled
const forms = document.querySelectorAll('form input');
document.addEventListener('input', function() {
    const isFilled = Array.from(forms).every(input => input.value.trim() !== '');
    if (isFilled) {
        submitButton.classList.remove('disabled');
    } else {
        submitButton.classList.add('disabled');
    }
})