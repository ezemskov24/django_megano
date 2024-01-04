//Маска ввода номера телефона при оформлении заказа

const phone = document.querySelector('.mask_phone')
const mask_phone = new Inputmask("+7 (999) 999-99-99")

mask_phone.mask(phone);
