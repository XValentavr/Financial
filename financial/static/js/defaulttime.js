let now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
document.getElementById('date').max = now.toISOString().slice(0, 16);
document.getElementById('date').value = now.toISOString().slice(0, 16);