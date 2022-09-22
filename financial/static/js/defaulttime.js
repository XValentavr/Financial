let now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
document.getElementById('date').max = now.toISOString().slice(0, 16);
document.getElementById('date').value = now.toISOString().slice(0, 16);

let global_date = document.getElementById('date').value

function more_then_now() {
    let current = document.getElementById('date').value
    if (current.slice(11, 16) > global_date.slice(11, 16) && current.slice(0, 10) === global_date.slice(0, 10)) {
        document.getElementById('date').value = global_date;
    }
}
