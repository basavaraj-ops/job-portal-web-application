document.addEventListener("DOMContentLoaded", function () {
    // Show flash message if exists
    const flashMessage = "{{ get_flashed_messages()[0] if get_flashed_messages() else '' }}";

    if (flashMessage) {
        showPopup(flashMessage);
    }

    function showPopup(message) {
        const popup = document.getElementById("popup");
        const popupMessage = document.getElementById("popup-message");

        if (popup && popupMessage) {
            popupMessage.innerText = message;
            popup.style.display = "block";

            setTimeout(() => {
                popup.style.display = "none";
            }, 2000);
        }
    }

    window.closePopup = function () {
        const popup = document.getElementById("popup");
        if (popup) {
            popup.style.display = "none";
        }
    };
});
