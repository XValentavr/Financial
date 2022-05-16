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
            'usd': parseFloat(banker['USD']).toFixed(1),
            'eur': parseFloat(banker['EUR']).toFixed(1),
            'rub': parseFloat(banker['RUB']).toFixed(1),
            'uah': parseFloat(banker['UAH']).toFixed(1),
            'pln': parseFloat(banker['PLN']).toFixed(1),
        }
        information.push(json_departments)
    }
    return information
}

function DisplayGotData(data) {
    CreateTable(GetData(data));
}

function CreateTable(data) {
    let table = document.querySelector("table");
    let keys = Object.keys(data[0])
    for (let i = 0; i < data.length; i++) {
        let element = data[i];
        let row = table.insertRow();
        for (let j = 0; j < keys.length; j++) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[keys[j]]);
            cell.appendChild(text);
        }
    }
}