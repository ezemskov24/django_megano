const compare_amt = document.getElementById('compare_amt')

function compare_length() {
    fetch('http://127.0.0.1:8000/catalog/compare/length/').
    then((response) => {
        return response.json()
    }).then((data) => {if (data.len === 0) {
        compare_amt.style.display = 'none'
    } else {
        compare_amt.style.display = 'flex'
        compare_amt.innerHTML = data.len
    }
    return data
    })
}

compare_length()