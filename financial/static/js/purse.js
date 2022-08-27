let session = document.getElementById("session").textContent
fetch(`/api/purse/${session}`)
    .then((response) => response.json())
    .then((data) => {
        DisplayGotData(data);
    })
    .catch((error) => console.log(error))


function get_currency(data) {
    let cur = []
    for (let i = 0; i < data.length; i++) {
        let currency = data[i]['name']
        cur.push(currency)
    }
    return cur
}

function GetData(data) {
    return fetch(`/api/currency`)
        .then((response) => response.json())
        .then((currency) => {
            let information = []
            for (let i = 0; i < data.length; i++) {
                let banker = data[i];
                let res_dict = {}
                let local = get_currency(currency)
                res_dict['account'] = banker['account']
                for (let j = 0; j <= local.length; j++) {
                    res_dict[local[j]] = banker[local[j]] + ' ' + local[j]
                }
                information.push(res_dict)
            }
            return information
        })

}

function DisplayGotData(data) {
    CreateTable(GetData(data));
}

function CreateTable(data) {
    let table = document.querySelector("table");
    const creator = () => {
        data.then((dat) => {
            let keys = Object.keys(dat[0])
            for (let i = 0; i < dat.length; i++) {
                let element = dat[i];
                let row = table.insertRow();
                let cell = row.insertCell();
                cell.classList.add('place')
                let cell1 = row.insertCell();
                cell1.classList.add('amount')
                let a = document.createElement("a");
                a.setAttribute("href", `/walletinfo/${element[keys[0]]}`);
                let text = document.createTextNode(element[keys[0]]);
                a.appendChild(text);
                cell.appendChild(a);
                for (let j = 1; j < keys.length; j++) {
                    if (keys[j] !== 'undefined' && !element[keys[j]].includes('undefined')) {
                        let amount = document.createElement("div");
                        if (!element[keys[j]].includes('NaN')) {
                            amount.innerText = element[keys[j]]
                            cell1.appendChild(amount)
                        }
                    }
                }
            }
        });
    };
    creator()

}
