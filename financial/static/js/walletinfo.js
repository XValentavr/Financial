let comments = document.getElementById('setcomments')

function where_checker() {
    let search = document.getElementById('search').value
    let by_date = document.getElementById('by_date')
    let by_sum = document.getElementById('by_sum')
    let by_comm = document.getElementById('by_comment')
    if (search === 'По дате') {
        get_if_not_select()
        by_comm.style.display = 'none';
        by_sum.style.display = 'none';
        if (by_date.style.display === 'none') {
            by_date.style.display = 'block';
            comments.style.display = 'block'
        }

    } else if (search === 'По комментарию') {
        get_if_not_select()
        by_date.style.display = 'none';
        by_sum.style.display = 'none';
        if (by_comm.style.display === 'none') {
            by_comm.style.display = 'block';
            comments.style.display = 'block'
        }
    } else if (search === 'По сумме') {
        get_if_not_select()
        by_date.style.display = 'none';
        by_comm.style.display = 'none';
        if (by_comm.style.display === 'none') {
            by_sum.style.display = 'block';
            comments.style.display = 'block'
        }
        let summ_down = document.getElementById('search_sum').value
        if (summ_down === 'Точная сумма') {
            document.getElementById('to_sum_value').value = null
            document.getElementById('from_sum_value').value = null
            document.getElementById('div_between_sum').style.display = 'none'
            document.getElementById('div_current_sum').style.display = 'block'
        } else if (summ_down === 'В диапазоне') {
            document.getElementById('current_sum_value').value = null
            document.getElementById('div_current_sum').style.display = 'none'
            document.getElementById('div_between_sum').style.display = 'block'

        }
    }


}

function get_if_not_select() {
    var tableHeaderRowCount = 0;
    var table = document.getElementById('userstory');
    var rowCount = table.rows.length;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
        table.deleteRow(tableHeaderRowCount);
    }
    const USERID = document.getElementById("session").textContent
    let where = document.URL
    if (where.includes('walletinfo')) {
        let page = decodeURI(document.URL.substring(document.URL.lastIndexOf('/')))
        fetch('/api/comments/' + page)
            .then((response) => response.json())
            .then((data) => {
                if (data.length > 0) {
                    let flag = false
                    displaydata(getter(data), flag)
                } else {
                    alert("Ничего не найдено, проверьте данные")
                }
            })
    } else {
        fetch("/api/comments")
            .then((response) => response.json())
            .then((comments) => {
                let flag = true
                displaydata(getter(comments), flag)
            })
            .catch((error) => console.log(error))
    }
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
            'deleted': comments['deleted'],
            'superuser': comments['superuser'],
            'datedelete': comments['datedelete'],
            'datechange': comments['datechange'],
            'percent': comments['percent']

        }
        com.push(json_comments)
    }

    return com
}


function displaydata(data, flag) {
    let tb = document.getElementById('userstory')
    for (let i = 0; i < data.length; i++) {
        let element = data[i];
        let unique_pair = element['pair']
        let count = 0
        for (let j = 0; j < data.length; j++) {
            let element_check = data[j];
            if (unique_pair === element_check['pair']) {
                if (count >= 1) {
                    if (element_check['moved'] === true) {
                        if (element['addedsumma'] != null) {
                            let string = (element['user'] + ' перевел ' + element_check['deletedsumma'] + ' с кошелька \"' + element_check['wallet'] + '\" в кошелек \"' + element['wallet'] + '\" и получил ' + element['addedsumma'] + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')
                            printer(element, tb, element['visibility'], string, flag)
                        }
                    } else if (element_check['exchanged'] === true) {
                        if (element['addedsumma'] != null) {
                            let string = (element['user'] + ' обменял ' + element_check['deletedsumma'] + ' с кошелька \"' + element_check['wallet'] + '\" в кошелек \"' + element['wallet'] + '\" и получил ' + element['addedsumma'] + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')
                            printer(element, tb, element['visibility'], string, flag)
                        }
                    }
                }
                count++;
            }
        }
        if (count <= 1) {
            if (element['superuser'] === true) {
                printer(element, tb, element['visibility'], 'undefined', flag)
            } else if (element['visibility'] === 'Общий') {
                printer(element, tb, element['visibility'], 'undefined', flag)
            } else if (element['visibility'] !== 'Общий') {
                if (element['UUID'] === USERID.trim()) {
                    printer(element, tb, element['visibility'], 'undefined', flag)
                }
            }
        }
    }
}

function printer(element, tb, visibility, str, flag) {
    let string
    if (str === 'undefined') {
        if (element['exchanged'] === true && element['deletedsumma'] != null) {
            string = (element['user'] + ' обменял ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

        } else if (element['exchanged'] === true && element['deletedsumma'] === null) {
            string = (element['user'] + ' получил ' + element['addedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

        } else if (element['moved'] === true && element['deletedsumma'] != null) {
            string = (element['user'] + ' перевел ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

        } else if (element['number'] != null) {
            let summa = element['addedsumma'].split(' ')[0]
            summa = (summa * 100 / (100 - element['percent'])).toFixed(1)
            string = (element['user'] + ' оплатил ' + element['addedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Номер счета: ' + element['number'] + '. Начальная сумма: ' + summa + '. Процент: ' + element['percent'] + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

        } else if (element['addedsumma'] != null) {
            string = (element['user'] + ' добавил ' + element['addedsumma'] + ' в кошелек \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

        } else if (element['addedsumma'] === null) {
            string = (element['user'] + ' вывел ' + element['deletedsumma'] + ' с кошелька \"' + element['wallet'] + '\"' + '. Дата: ' + element['date'] + '. ' + element['comment'] + '. ')

        }
    } else {
        string = str
    }
    let row = tb.insertRow();
    let cell = row.insertCell();
    let text;
    if (element['superuser'] === true) {
        if (element['deleted'] !== '0') {
            text = document.createElement('div');
            let changed = (' Отменено: ' + element['modified'] + '. ' + element['datedelete']).italics()
            string = string.italics() + ' ' + changed
            text.innerHTML = string
            cell.appendChild(text);
        } else
            add_buttons(element, string, cell, visibility, flag)
    } else if (visibility === 'Общий') {
        if (element['deleted'] !== '0') {
            text = document.createElement('div');
            let changed = (' Отменено: ' + element['modified'] + '. ' + element['datedelete']).italics()
            string = string.italics() + ' ' + changed
            text.innerHTML = string
            cell.appendChild(text)
        } else if (element['UUID'] === USERID.trim()) {
            add_buttons(element, string.italics(), cell, visibility, flag)
        } else {
            if (element['modified'] !== null) {
                text = document.createElement('div');
                let changed = (' Изменено:' + element['modified'] + '. ' + element['datechange']).italics()
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
        if (element['deleted'] !== '0') {
            text = document.createElement('div');
            let changed = (' Отменено: ' + element['modified'] + '. ' + element['datedelete']).italics()
            string = string.italics() + ' ' + changed
            text.innerHTML = string
            cell.appendChild(text);
        } else
            add_buttons(element, string, cell, visibility, flag)
    }

}