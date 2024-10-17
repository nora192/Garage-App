console.log("auth");
form.addEventListener("submit", e => {
    if (!validateInput()) {
        e.preventDefault(); 
    }
});

const validateInput = () => {
    let isValid = true;

    const firstNameValue = firstName.value.trim();
    const lastNameValue = lastName.value.trim();
    const emailValue = email.value.trim();
    const password1Value = password1.value.trim();
    const password2Value = password2.value.trim();

    if (firstNameValue === '') {
        setError(firstName, 'First name field is required');
        isValid = false;
    } else {
        setSuccess(firstName);
    }

    if (lastNameValue === '') {
        setError(lastName, 'Last name field is required');
        isValid = false;
    } else {
        setSuccess(lastName);
    }

    if (emailValue === '') {
        setError(email, 'Email is required');
        isValid = false;
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
        isValid = false;
    } else {
        setSuccess(email);
    }

    if (password1Value === '') {
        setError(password1, 'Password is required');
        isValid = false;
    } else if (password1Value.length < 8) {
        setError(password1, 'Password must be at least 8 characters.');
        isValid = false;
    } else {
        setSuccess(password1);
    }

    if (password2Value === '') {
        setError(password2, 'Please confirm your password');
        isValid = false;
    } else if (password2Value !== password1Value) {
        setError(password2, "Passwords don't match");
        isValid = false;
    } else {
        setSuccess(password2);
    }

    return isValid;  
};
