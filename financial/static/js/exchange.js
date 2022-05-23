function exchanged() {
    let rate = document.getElementById('rate').value
    let summa = document.getElementById('changedsumma').value
    let currency = document.getElementById("valuta").value = rate;
    document.getElementById("newsumma").value = (summa * currency).toFixed(2);
}
