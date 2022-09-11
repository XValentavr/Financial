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

function onchange_summa() {
    let newsumma = document.getElementById('newsumma').value
    let summa = document.getElementById('changedsumma').value
    let to = document.getElementById('currencies_buy').value
    let from = document.getElementById('currencies_sold').value

    let valuta_dict = {
        'USD': {
            'EUR': summa * (1 / newsumma),
            'UAH': newsumma / summa,
            'PLN': newsumma / summa,
        },
        'EUR': {
            'USD': newsumma / summa,
            'UAH': newsumma / summa,
            'PLN': newsumma / summa
        },
        'UAH': {
            'USD': summa * (1 / newsumma),
            'EUR': summa * (1 / newsumma),
            'PLN': summa * (1 / newsumma)
        },
        'PLN': {
            'USD': summa * (1 / newsumma),
            'EUR': summa * (1 / newsumma),
            'UAH': newsumma / summa
        }

    }
    document.getElementById("valuta").value = valuta_dict[from][to].toFixed(2);

}
