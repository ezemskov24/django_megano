const type_properties = document.getElementById('type_properties')

async function delete_all() {
    await fetch('delete_all/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    document.getElementById('all_products').style.display = 'none'
    compare_length()
}

async function delete_product(slug) {
    document.getElementById(slug).style.display = 'none'
    await fetch('delete/' + slug + '/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    compare_length()
}

function change_properties() {
    console.log(type_properties.checked)
    if (type_properties.checked) {
        console.log(1)
        $('.table-diff').css('display', 'flex')
        $('.table-no-diff').css('display', 'none')
    } else {
        console.log(2)
        $('.table-diff').css('display', 'none')
        $('.table-no-diff').css('display', 'flex')
    }
}