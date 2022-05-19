fetch("/api/users")
    .then((response) => response.json())
    .then((data) => {
        DisplayGotData(data);
    })
    .catch((error) => console.log(error))


function DisplayGotData(data) {
    if (data.length === 0) {
        let empty = document.getElementById("empty");
        let text = document.createTextNode("No users were found");
        empty.appendChild(text);
    } else {
        CreateTable(GetData(data));
    }
}


function GetData(data) {
    let information = []
    for (let i = 0; i < data.length; i++) {
        let current_user = data[i];
        let json_users = {
            'identifier': current_user['id'],
            'Name': current_user['user'],
            'password': current_user['password'],
            'UUID': current_user['UUID']
        }
        information.push(json_users)
    }
    return information
}

function CreateTable(data) {
    let table = document.querySelector("table");
    let keys = Object.keys(data[0])
    for (let i = 0; i < data.length; i++) {
        let element = data[i];
        let row = table.insertRow();
        for (let j = 1; j < keys.length - 1; j++) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[keys[j]]);
            cell.appendChild(text);
        }
        let cell = row.insertCell();
        let a = document.createElement("a");
        a.setAttribute("href", `/users/edit/${element['UUID']}`);
        let text = document.createTextNode("Изменить");
        a.appendChild(text);
        cell.appendChild(a);
        cell = row.insertCell();
        //create delete request
        a = document.createElement("a");
        a.setAttribute("onclick", `api_delete(${element['identifier']})`)
        text = document.createTextNode("Удалить");
        a.appendChild(text);
        cell.appendChild(a);
    }
}

function api_delete(identifier) {
    if (confirm("Вы уверенны, что хотите удалить пользователя?")) {
        fetch(`/api/users/${identifier}`, {
            method: 'DELETE'
        })
            .then((response) => response.json())
            .then(() => {
                window.location.href = `/change`;
            })
            .catch(() => {
                window.location = document.URL;
            })
    } else window.location.href = document.URL

}
