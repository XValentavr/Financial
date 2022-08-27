fetch("/api/currency")
    .then((response) => response.json())
    .then((data) => {
        DisplayGotData(data);
    })
    .catch((error) => console.log(error))


function DisplayGotData(data) {
    if (data.length === 0) {
        let empty = document.getElementById("empty");
        let text = document.createTextNode("No currency found");
        empty.appendChild(text);
    } else {
        CreateTable(GetData(data));
    }
}


function GetData(data) {
    let information = []
    for (let i = 0; i < data.length; i++) {
        let current_cur = data[i];
        let json_currency = {
            'identifier': current_cur['identifier'],
            'currency': current_cur['name']
        }
        information.push(json_currency)
    }
    return information
}

function CreateTable(data) {
    let table = document.querySelector("table");
    let keys = Object.keys(data[0])
    for (let i = 0; i < data.length; i++) {
        let element = data[i];
        let row = table.insertRow();
        for (let j = 1; j < keys.length; j++) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[keys[j]]);
            cell.appendChild(text);
        }
        let cell = row.insertCell();
        let a = document.createElement("a");
        a.setAttribute("href", `/currency/edit/${element['identifier']}`);
        let text = document.createTextNode("Изменить");
        a.appendChild(text);
        cell.appendChild(a);
        cell = row.insertCell();
        a = document.createElement("a");
        a.setAttribute("onclick", `api_delete(${element['identifier']})`)
        text = document.createTextNode("Удалить");
        a.appendChild(text);
        cell.appendChild(a);
    }
}

function api_delete(identifier) {
    if (confirm("Вы уверенны, что хотите удалить валюту?")) {
        fetch(`/api/currency/${identifier}`, {
            method: 'DELETE'
        })
            .then((response) => response.json())
            .then(() => {
                window.location.href = `/currency`;
            })
            .catch(() => {
                window.location = document.URL;
            })
    } else window.location.href = document.URL

}