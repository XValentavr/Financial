function changer(id) {
    document.getElementById(id).value = document.getElementById(id).value.replace(/[^\w\s]/gi, '.')
}
