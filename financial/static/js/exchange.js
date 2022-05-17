function exchanged() {
    let currencies_sold = document.getElementById("currencies_sold").value;
    let url = "https://v6.exchangerate-api.com/v6/727a8cafbfa682e3187bc8ab/latest/" + currencies_sold.toString()
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            get_data(data)
        })
        .catch((error) => console.log(error))
}

function get_data(data) {
    let rate = data['conversion_rates']
    let summa = document.getElementById('changedsumma').value
    let currencies_buy = document.getElementById("currencies_buy").value;
    let currency = document.getElementById("valuta").value = rate[currencies_buy];
    document.getElementById("newsumma").value = summa * currency.toFixed(2);
}
