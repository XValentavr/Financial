let form = document.getElementById('movingform');
let submitButton = document.getElementById('submitID');
form.addEventListener('submit', function () {
    submitButton.setAttribute('disabled', 'disabled');

    submitButton.value = 'Please wait...';

}, false);

document.querySelector(".openChatBtn").addEventListener("click", openForm);
document.querySelector(".close").addEventListener("click", closeForm);
