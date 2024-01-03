const total_price_span = document.getElementById('total_price')

async function get_total_price(auth) {
    await fetch('http://127.0.0.1:8000/cart/api/cart/')
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            let total_price = 0
            for (elem of data) {
                if (auth === 'True') {
                    total_price += elem.product_seller.price * elem.count
                } else {
                    total_price += elem.price * elem.cart_count
                }
            }
            total_price_span.innerHTML = total_price + '$'
        })
}

async function remove_product(pk) {
    await fetch('http://127.0.0.1:8000/cart/api/cart/'+ pk +'/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
        .then(() => {
            cart_amt()
        })
    document.getElementById('product_cart_'+ pk).style.display = 'none'
    get_total_price()
}

async function changing_product_amt(pk, term, auth) {
    console.log(auth)
    let value = Number(document.getElementById('input_'+pk).value) + term
    if (value === 0) {
        remove_product(pk)
        return
    }
    await fetch('http://127.0.0.1:8000/cart/api/cart/'+ pk +'/', {
        method: 'PATCH',
        body: JSON.stringify({'count': value}),
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken,
        }
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (auth === 'True') {
                var product_price = data.count * data.product_seller.price
            } else {
                var product_price = data.count * data.price
            }
            document.getElementById('product_price_'+ pk).innerHTML = product_price + '$'
            get_total_price(auth)
        })
}

async function changing_product_seller() {

}