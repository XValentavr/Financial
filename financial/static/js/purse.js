let rate = []
let session = document.getElementById("session").textContent
fetch(`/api/purse/${session}`)
    .then((response) => response.json())
    .then((data) => {
        DisplayGotData(data);
    })
    .catch((error) => console.log(error))

function GetData(data) {
    let information = []
    for (let i = 0; i < data.length; i++) {
        let banker = data[i];
        let json_departments = {
            'bank': banker['account'],
            'money': banker['money'],
        }
        information.push(json_departments)
    }
    return information
}

function DisplayGotData(data) {
    Insert(GetData(data));
}

function currency(currency_value) {
    if (currency_value === '$') {
        rate[0] = 34.2
    }
    if (currency_value === '€') {
        rate[0] = 36.2
    }
    if (currency_value === '₽') {
        rate[0] = 0.02
    }
    if (currency_value === '₴') {
        rate[0] = 1
    }
    let session = document.getElementById("session").textContent
    fetch(`/api/purse/${session}`)
        .then((response) => response.json())
        .then((data) => {
            DisplayGotData(data);
        })
        .catch((error) => console.log(error))
    Insert(GetData(data));
}

function Insert(data) {
    if (rate.length === 1) {
        document.getElementById("seif").innerHTML = data[0].bank + ': ' + parseFloat(data[0].money / rate[0]).toFixed(2)
        document.getElementById("wallet").innerHTML = data[1].bank + ': ' + parseFloat(data[1].money / rate[0]).toFixed(2)
        document.getElementById("bank").innerHTML = data[2].bank + ': ' + parseFloat(data[2].money / rate[0]).toFixed(2)
        document.getElementById("crypto").innerHTML = data[3].bank + ': ' + parseFloat(data[3].money / rate[0]).toFixed(2)
    } else {
        document.getElementById("seif").innerHTML = data[0].bank + ': ' + data[0].money
        document.getElementById("wallet").innerHTML = data[1].bank + ': ' + data[1].money
        document.getElementById("bank").innerHTML = data[2].bank + ': ' + data[2].money
        document.getElementById("crypto").innerHTML = data[3].bank + ': ' + data[3].money
    }
}