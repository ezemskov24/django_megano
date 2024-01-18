//Маска ввода номера телефона при оформлении заказа

const phone = document.querySelector('.mask_phone')
const mask_phone = new Inputmask("+7 (999) 999-99-99")

mask_phone.mask(phone);


// Функция для заполнения последней страницы заказа

function makeDataOrderCreate() {
    let delivery_type = '';
    let payment_type = '';

    let user_name = document.getElementById('fio').value;
    let user_phone = document.getElementById('phone').value;
    let user_email = document.getElementById('mail').value;

    let delivery_type_1 = document.getElementById('delivery_type_1');
    let delivery_type_2 = document.getElementById('delivery_type_2');
    if (delivery_type_1.checked) {
        delivery_type = delivery_type_1.value;
    } else {
        delivery_type = delivery_type_2.value;
    }

    let city = document.getElementById('city').value;
    let delivery_address = document.getElementById('address').value;

    let payment_type_1 = document.getElementById('type_1');
    let payment_type_2 = document.getElementById('type_2');
    if (payment_type_1.checked) {
        payment_type = payment_type_1.value;
    } else {
        payment_type = payment_type_2.value;
    }

    document.getElementById('user_fio').innerText = user_name;
    document.getElementById('user_phone').innerText = user_phone;
    document.getElementById('user_email').innerText = user_email;
    document.getElementById('user_delivery_type').innerText = delivery_type;
    document.getElementById('user_city').innerText = city;
    document.getElementById('user_delivery_address').innerText = delivery_address;
    document.getElementById('user_payment_type').innerText = payment_type;
}


// Перемещение по страницам создания заказа

const create_order = document.querySelector('.Order');
const next = create_order.querySelectorAll('.Order-next'); // кнопка "Далее"
const menu_item = create_order.querySelectorAll('.menu-item'); // элементы меню в разделе создания заказа
const order_page = create_order.querySelectorAll('.Order-block'); // страницы в разделе создания заказа


menu_item.forEach(function(element) {
    element.addEventListener('click', function(elem) {
        const path = elem.currentTarget.querySelector('.menu-link').dataset.path;

        menu_item.forEach(function (btn) {btn.classList.remove('menu-item_ACTIVE')});
        elem.currentTarget.classList.add('menu-item_ACTIVE');

        order_page.forEach(function (page) {page.classList.remove('Order-block_OPEN')})
        create_order.querySelectorAll(`[data-target="${path}"]`).forEach(function(page) {
            page.classList.add('Order-block_OPEN');
        });

        element.classList.add('menu-item_ACTIVE');

        if (path === "four") makeDataOrderCreate();
    });
});


// Обработчик кнопок "Далее" на страницах создания заказа

const order_next = create_order.querySelectorAll('.Order-next');


order_next.forEach(function (btn_next) {
    btn_next.addEventListener('click', function(elem) {
        const path = elem.currentTarget.dataset.path;

        menu_item.forEach(function (btn) {btn.classList.remove('menu-item_ACTIVE')});
        create_order.querySelector('.Section-column').querySelector(`[data-path="${path}"]`)
            .parentNode.classList.add('menu-item_ACTIVE')

        order_page.forEach(function (page) {page.classList.remove('Order-block_OPEN')})
        create_order.querySelector(`[data-target="${path}"]`).classList.add('Order-block_OPEN');

        if (path === "four") makeDataOrderCreate();
    });
});

