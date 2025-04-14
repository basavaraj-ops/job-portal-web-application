document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");

    if (form) {
        form.addEventListener("submit", function (event) {
            
        });
    }

    function showPopup(message, redirectUrl) {
        const popup = document.getElementById("popup");
        const popupMessage = document.getElementById("popup-message");

        if (popup && popupMessage) {
            popupMessage.innerText = message;
            popup.style.display = "block";

            setTimeout(() => {
                popup.style.display = "none";
                if (redirectUrl) {
                    window.location.href = redirectUrl;
                }
            }, 2000);
        }
    }

    // If you ever need to manually close the popup
    window.closePopup = function () {
        const popup = document.getElementById("popup");
        if (popup) {
            popup.style.display = "none";
        }
    }
});
