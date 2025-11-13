document.addEventListener("DOMContentLoaded", function () {
    'use strict';

    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');

            // Asegurar la validación del input de contraseña manualmente
            const passwordInput = document.querySelector("#inputChoosePassword");
            if (passwordInput && passwordInput.value.trim() === "") {
                passwordInput.classList.add("is-invalid");
                passwordInput.closest(".col-12").querySelector(".invalid-feedback").style.display = "block";
            } else {
                passwordInput.classList.remove("is-invalid");
                passwordInput.closest(".col-12").querySelector(".invalid-feedback").style.display = "none";
            }
        }, false);
    });
});

// Password show & hide js

$(document).ready(function () {
    $("#togglePassword").on('click', function (event) {
        event.preventDefault();
        
        let passwordInput = $("#inputChoosePassword");
        let icon = $(this).find("i");

        if (passwordInput.attr("type") === "text") {
            passwordInput.attr("type", "password");
            icon.addClass("bx-hide").removeClass("bx-show");
        } else {
            passwordInput.attr("type", "text");
            icon.removeClass("bx-hide").addClass("bx-show");
        }
    });
});

