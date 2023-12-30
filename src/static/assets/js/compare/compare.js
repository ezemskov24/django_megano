async function delete_all() {
    await fetch('delete_all/')
    document.getElementById('all_products').style.display = 'none'
    compare_length()
}

async function delete_product(slug) {
    document.getElementById(slug).style.display = 'none'
    await fetch('delete/' + slug + '/')
    compare_length()
}

function change_properties() {
    console.log(1)
}