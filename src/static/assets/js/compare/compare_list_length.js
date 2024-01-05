const compare_amt = document.getElementById('compare_amt')

function compare_length() {
    fetch('http://127.0.0.1:8000/catalog/compare/amt/').
    then((response) => {
        return response.json()
    }).then((data) => {
        if (data === 0) {
        compare_amt.style.display = 'none'
    } else {
        compare_amt.style.display = 'flex'
        compare_amt.innerHTML = data
    }
    return data
    })
}

compare_length()