function exchanged() {
    let rate = document.getElementById('rate').value
    let summa = document.getElementById('changedsumma').value
    document.getElementById("valuta").value = rate;
    let to = document.getElementById('currencies_buy').value
    let from = document.getElementById('currencies_sold').value
    exchanger(summa, rate, to, from)
}

function exchanger(summa, rate, to, from) {
    let valuta_dict = {
        'USD': {
            'EUR': summa * (1 / rate),
            'UAH': summa * rate,
            'PLN': summa * rate,
        },
        'EUR': {
            'USD': summa * rate,
            'UAH': summa * rate,
            'PLN': summa * rate
        },
        'UAH': {
            'USD': summa * (1 / rate),
            'EUR': summa * (1 / rate),
            'PLN': summa * (1 / rate)
        },
        'PLN': {
            'USD': summa * (1 / rate),
            'EUR': summa * (1 / rate),
            'UAH': summa * rate
        }

    }
    document.getElementById("newsumma").value = valuta_dict[from][to].toFixed(2);
}