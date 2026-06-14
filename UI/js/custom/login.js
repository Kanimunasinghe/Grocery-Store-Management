$(function() {
    function checkIfLoggedIn() {
        // Just check localStorage - don't call backend
        var adminId = localStorage.getItem('admin_id');
        
        if (adminId) {
            // Already logged in, redirect to dashboard
            window.location.href = "index.html";
        }
    }
    
    // Handle login form submission
    $("#loginForm").on("submit", function(e) {
        e.preventDefault();
        
        var username = $("#username").val().trim();
        var password = $("#password").val();
        
        // Validation
        if (!username) {
            showAlert("Please enter username or email", "danger");
            return;
        }
        
        if (!password) {
            showAlert("Please enter password", "danger");
            return;
        }
        
        // Show loader
        $("#loader").show();
        $("#loginBtn").prop("disabled", true);
        
        // Make login request
        $.ajax({
            method: "POST",
            url: signinApiUrl,
            data: {
                'data': JSON.stringify({
                    username: username,
                    password: password
                })
            }
        }).done(function(response) {
            if (response.success) {
                showAlert("Login successful! Redirecting...", "success");
                // Store admin info in localStorage
                localStorage.setItem('admin_id', response.admin_id);
                localStorage.setItem('username', response.username);
                localStorage.setItem('email', response.email);
                
                // Redirect to dashboard
                setTimeout(function() {
                    window.location.href = "index.html";
                }, 1500);
            } else {
                showAlert(response.message || "Login failed", "danger");
                $("#loader").hide();
                $("#loginBtn").prop("disabled", false);
            }
        }).fail(function(error) {
            var errorMessage = "Login failed. Please try again.";
            if (error.responseJSON && error.responseJSON.error) {
                errorMessage = error.responseJSON.error;
            }
            showAlert(errorMessage, "danger");
            $("#loader").hide();
            $("#loginBtn").prop("disabled", false);
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
        // Not authenticated, stay on login page
    });
}
