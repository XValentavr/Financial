const USERID = document.getElementById("session").textContent
let where = document.URL
if (where.includes('walletinfo')) {
    let page = decodeURI(document.URL.substring(document.URL.lastIndexOf('/')))
    fetch('/api/wallet/' + page)
        .then((response) => response.json())
        .then((data) => {
            if (data.length > 0) {
                displaydata(getter(data))
            } else {
                alert("Ничего не найдено, проверьте данные")
            }
        })
} else {
    fetch("/api/comments")
        .then((response) => response.json())
        .then((comments) => {
            displaydata(getter(comments))
        })
        .catch((error) => console.log(error))
}

function getter(data) {
    let com = []
    for (let i = 0; i < data.length; i++) {
        let comments = data[i];
        let json_comments = {
            'identifier': comments['id'],
            "date": comments['date'],
            "comment": comments['comment'],
            "addedsumma": comments['addedsumma'],
            "deletedsumma": comments['deletedsumma'],
            "user": comments['user'],
            "wallet": comments['wallet'],
            "UUID": comments['UUID'],
            'visibility': comments['visibility'],
            'number': comments['number'],
            'moved': comments['moved'],
            'exchanged': comments['exchanged'],
            'pair': comments['pairs'],
            'modified': comments['modified'],
            'superuser': comments['superuser']
        }
        com.push(json_comments)
    }

    return com
}


function displaydata(data) {
    let tb = document.getElementById('userstory')
    for (let i = 0; i < data.length; i++) {
        let element = data[i];
        if (element['visibility'] === 'Общий') {
            printer(element, tb, element['visibility'])
        } else if (element['visibility'] !== 'Общий') {
            if (element['UUID'] === USERID.trim()) {
                printer(element, tb, element['visibility'])
            }
        }
    }
}

function printer(element, tb, visibility) {
    let string
    if (element['exchanged'] === true && element['deletedsumma'] != null) {
        string = (element['user'] + ' обменял ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['exchanged'] === true && element['deletedsumma'] === null) {
        string = (element['user'] + ' получил ' + element['addedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['moved'] === true && element['deletedsumma'] != null) {
        string = (element['user'] + ' перевел ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['number'] != null) {
        string = (element['user'] + ' оплатил ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['addedsumma'] != null) {
        string = (element['user'] + ' добавил ' + element['addedsumma'] + ' в кошелек \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['addedsumma'] === null) {
        string = (element['user'] + ' вывел ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    }
    let row = tb.insertRow();
    let cell = row.insertCell();
    let text;
    if (visibility === 'Общий') {
        if (element['superuser'] === true) {
            add_buttons(element, string.italics(), cell, visibility)
        } else if (element['UUID'] === USERID.trim()) {
            add_buttons(element, string.italics(), cell, visibility)
        } else {
            if (element['modified'] !== null) {
                text = document.createElement('div');
                let changed = (' Изменено:' + element['modified']).italics()
                string = string.italics() + ' ' + changed
                text.innerHTML = string
                cell.appendChild(text);
            } else {
                text = document.createElement('div');
                text.innerHTML = string.italics()
                cell.appendChild(text);
            }
        }
    } else {
        add_buttons(element, string, cell, visibility)
    }

}

function add_buttons(element, string, cell, visibility) {
    let a = document.createElement("a");
    a.setAttribute("href", `/comments/edit/${element['pair']}`);
    let text1 = document.createTextNode("Изменить / ");
    a.appendChild(text1);
    let adel = document.createElement("a");
    adel.setAttribute("onclick", `api_delete(${element['identifier']})`)
    let text = document.createTextNode("Отменить");
    adel.appendChild(text);
    if (visibility === 'Общий') {
        if (element['modified'] !== null) {
            text = document.createElement('div');
            let changed = (' Изменено:' + element['modified']).italics()
            string = string + ' ' + changed
            text.innerHTML = string
        } else {
            text = document.createElement('div');
            text.innerHTML = string
        }

    } else {
        if (element['modified'] !== null) {
            text = document.createElement('div');
            let changed = (' Изменено:' + element['modified']).italics()
            string.replace(/(<([^>]+)>)/ig, '');
            string = string + ' ' + changed
            text.innerHTML = string
        } else {
            text = document.createElement('div');
            text.innerHTML = string.replace(/(<([^>]+)>)/ig, '');
        }
    }
    cell.appendChild(text);
    cell.appendChild(a);
    cell.appendChild(adel);
}

function api_delete(identifier) {
    if (confirm("Вы уверенны, что хотите отменить транзацию?")) {
        fetch(`/api/reset/${identifier}`, {
            method: 'DELETE'
        })
            .then((response) => response.json())
            .then(() => {
                window.location.href = `/income`;
            })
            .catch(() => {
                window.location = document.URL;
            })
    } else window.location.href = document.URL

}

function get_story_date() {
    let table = document.getElementById("userstory");
    let rowCount = table.rows.length;
    for (let i = rowCount - 1; i >= 0; i--) {
        table.deleteRow(i);
    }
    let start_date = document.getElementById('start_date').value
    let finish_date = document.getElementById('finish_date').value
    let page = decodeURI(document.URL.substring(document.URL.lastIndexOf('/')))
    fetch('/api/wallet/' + page + '?start_date=' + start_date + "&end_date=" + finish_date)
        .then((response) => response.json())
        .then((data) => {
            if (data.length > 0) {
                displaydata(getter(data))
            } else {
                alert("Ничего не найдено, проверьте данные")
            }
        })

}