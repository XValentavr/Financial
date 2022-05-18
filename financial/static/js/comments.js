const USERID = document.getElementById("session").textContent
fetch("/api/comments")
    .then((response) => response.json())
    .then((comments) => {
        displaydata(getter(comments))
    })
    .catch((error) => console.log(error))

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
            'exchanged': comments['exchanged']
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
                printer(element, tb)
            }
        }
    }
}

function printer(element, tb, visibility) {
    let string
    if (element['exchanged'] === true && element['deletedsumma'] != null) {
        string = ('Пользователь ' + element['user'] + ' обменял ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['exchanged'] === true && element['deletedsumma'] === null) {
        string = ('Пользователь ' + element['user'] + ' получил ' + element['addedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['moved'] === true && element['deletedsumma'] != null) {
        string = ('Пользователь ' + element['user'] + ' перевел ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['number'] != null) {
        string = ('Пользователь ' + element['user'] + ' оплатил ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['addedsumma'] != null) {
        string = ('Пользователь ' + element['user'] + ' добавил ' + element['addedsumma'] + ' в кошелек \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    } else if (element['addedsumma'] === null) {
        string = ('Пользователь ' + element['user'] + ' вывел ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

    }
    let row = tb.insertRow();
    let cell = row.insertCell();
    let text;
    if (visibility === 'Общий') {
        text = document.createTextNode(string.italics());
        if (element['UUID'] === USERID.trim()) {
            add_buttons(element, string, cell)
        } else {
            cell.appendChild(text);
        }
    } else {
        add_buttons(element, string, cell)
    }

}

function add_buttons(element, string, cell) {
    let a = document.createElement("a");
    a.setAttribute("href", `/users/edit/${element['UUID']}`);
    let text1 = document.createTextNode("Изменить / ");
    a.appendChild(text1);
    let adel = document.createElement("a");
    adel.setAttribute("onclick", `api_delete(${element['identifier']})`)
    let text = document.createTextNode("Отменить");
    adel.appendChild(text);
    text = document.createTextNode(string);
    cell.appendChild(text);
    cell.appendChild(a);
    cell.appendChild(adel);
}

function api_delete(identifier) {
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
}