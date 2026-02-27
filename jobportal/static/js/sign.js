document.addEventListener("DOMContentLoaded", function () {

    // TOGGLE PANEL 
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });

    // CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // ELEMENTS 
    const form = document.getElementById("signupForm");
    const otpBox = document.getElementById("otp-box");
    const submitBtn = document.getElementById("submitBtn");
    const resendBtn = document.getElementById("resendOtpBtn");
    const timerSpan = document.getElementById("timer");
    const verifyBtn = document.getElementById("verifyOtpBtn");

    let storedEmail = "";   // store email globally
    let countdown;
    let timeLeft = 60;

    // SIGNUP SUBMIT
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch("/sign/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrftoken
            }
        })
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                alert(data.error);
                return;
            }

            if (data.status === "send_otp") {

                storedEmail = data.email;   // save email
                // Send OTP
                fetch("/send-otp/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: `email=${encodeURIComponent(storedEmail)}`
                });
                
                otpBox.style.display = "block";
                submitBtn.style.display = "none";
                startResendTimer();
            }
        });
    });

    //VERIFY OTP
    verifyBtn.addEventListener("click", function () {

        const otp = document.querySelector('[name="otp"]').value;

        fetch("/verify-otp/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `otp=${encodeURIComponent(otp)}&email=${encodeURIComponent(storedEmail)}`
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                alert(data.error);
            }
        });
    });

    //RESEND OTP
    resendBtn.addEventListener("click", function () {

        fetch("/send-otp/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `email=${encodeURIComponent(storedEmail)}`
        });

        startResendTimer();
    });

    //TIMER FUNCTION 
    function startResendTimer() {
        timeLeft = 60;
        timerSpan.textContent = timeLeft;
        resendBtn.disabled = true;

        countdown = setInterval(() => {
            timeLeft--;
            timerSpan.textContent = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(countdown);
                resendBtn.disabled = false;
                resendBtn.textContent = "Resend OTP";
            }
        }, 1000);
    }
});