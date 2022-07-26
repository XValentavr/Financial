function toggle_general(source) {
    let checkboxes = document.querySelectorAll('input[about="forgeneral"]');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] !== source)
            checkboxes[i].checked = source.checked;
    }
}

function toggle_public(source) {
    let checkboxes = document.querySelectorAll('input[about="forpublic"]');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] !== source)
            checkboxes[i].checked = source.checked;
    }
}