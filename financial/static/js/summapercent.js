function summa_counter() {
    let percent = document.getElementById("percent").value;
    let summa = document.getElementById("number").value;
    if (percent > 0) {
        document.getElementById("changedsumma").value = summa * (percent / 100);

    } else {
        document.getElementById("changedsumma").value = summa;
    }
}