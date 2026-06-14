document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function () {
        const button = form.querySelector("button[type='submit']");
        button.innerText = "Predicting...";
        button.disabled = true;
    });
});