$(function() {
    function checkIfLoggedIn() {
        // Just check localStorage - don't call backend
        var adminId = localStorage.getItem('admin_id');
        
        if (adminId) {
            // Already logged in, redirect to dashboard
            window.location.href = "index.html";
        }
    }
    
    // Handle signup form submission
    $("#signupForm").on("submit", function(e) {
        e.preventDefault();
        
        var username = $("#username").val().trim();
        var email = $("#email").val().trim();
        var password = $("#password").val();
        var confirmPassword = $("#confirmPassword").val();
        
        // Validation
        if (!username) {
            showAlert("Please enter username", "danger");
            return;
        }
        
        if (username.length < 3) {
            showAlert("Username must be at least 3 characters", "danger");
            return;
        }
        
        if (!email) {
            showAlert("Please enter email", "danger");
            return;
        }
        
        // Basic email validation
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showAlert("Please enter a valid email address", "danger");
            return;
        }
        
        if (!password) {
            showAlert("Please enter password", "danger");
            return;
        }
        
        if (password.length < 6) {
            showAlert("Password must be at least 6 characters", "danger");
            return;
        }
        
        if (password !== confirmPassword) {
            showAlert("Passwords do not match", "danger");
            return;
        }
        
        // Show loader
        $("#loader").show();
        $("#signupBtn").prop("disabled", true);
        
        // Make signup request
        $.ajax({
            method: "POST",
            url: signupApiUrl,
            data: {
                'data': JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            }
        }).done(function(response) {
            if (response.success) {
                showAlert("Account created successfully! Redirecting to login...", "success");
                // Redirect to login page
                setTimeout(function() {
                    window.location.href = "login.html";
                }, 2000);
            } else {
                showAlert(response.message || "Signup failed", "danger");
                $("#loader").hide();
                $("#signupBtn").prop("disabled", false);
            }
        }).fail(function(error) {
            var errorMessage = "Signup failed. Please try again.";
            if (error.responseJSON && error.responseJSON.error) {
                errorMessage = error.responseJSON.error;
            }
            showAlert(errorMessage, "danger");
            $("#loader").hide();
            $("#signupBtn").prop("disabled", false);
        });
    });
});

function showAlert(message, type) {
    var alertBox = $("#alertBox");
    alertBox.removeClass("alert-danger alert-success");
    alertBox.addClass("alert-" + type);
    alertBox.text(message);
    alertBox.show();
    
    // Auto-hide success alerts
    if (type === "success") {
        setTimeout(function() {
            alertBox.hide();
        }, 3000);
    }
}

function checkIfLoggedIn() {
    $.get(checkAuthApiUrl, function(response) {
        if (response.authenticated) {
            // Already logged in, redirect to dashboard
            window.location.href = "index.html";
        }
    }).fail(function() {
        // Not authenticated, stay on signup page
    });
}
