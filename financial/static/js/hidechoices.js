function get_value_hiber1() {
    let valuetoshowall = document.getElementById('valuetoshowall')
    if (valuetoshowall.value === 'Нет') {
        document.getElementById('hider1').style.display = 'none'
    } else if (valuetoshowall.value === 'Да') {
        document.getElementById('hider1').style.display = 'block'
    }
}

function get_value_hiber2() {
    let valuetoshowall = document.getElementById('valuetoshowall')
    if (valuetoshowall.value === 'Нет') {
        document.getElementById('hider2').style.display = 'none'
    } else if (valuetoshowall.value === 'Да') {
        document.getElementById('hider2').style.display = 'block'
    }
}