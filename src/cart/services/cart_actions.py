# from django.db.models import F
#
# from cart.models import Cart
# from products.models import Product, SellerProduct
#
#
# def add_product_to_cart(user, slug, product_seller):
#     '''метод добавляет товар в корзину'''
#     cart_product = Cart.objects.filter(profile=user)
#
#     if not product_seller:
#         product_seller = SellerProduct.objects.get(product__slug=slug, price=Product.objects.get(slug=slug).min_price)
#     else:
#         product_seller = SellerProduct.objects.get(pk=product_seller)
#
#     if cart_product.filter(product_name=slug, product_seller=product_seller):
#         change_cart_product_amt(user, slug, 1, product_seller.pk)
#         return
#
#     cart_product = Cart(
#         profile=user,
#         product_seller=product_seller,
#         product_name=slug,
#     )
#     cart_product.save()
#
#
# def remove_product_from_cart(user, slug, product_seller):
#     '''метод удаляет определённый товар из корзины'''
#     Cart.objects.filter(profile=user).filter(product_name=slug, product_seller__pk=product_seller).delete()
#
#
# def change_cart_product_amt(user, slug, change, product_seller):
#     '''метод изменяет количество определенного товара в корзине'''
#     cart_product = Cart.objects.filter(profile=user)
#     if cart_product.get(product_name=slug, product_seller__pk=product_seller).count == 1 and change == -1:
#         remove_product_from_cart(user, slug, product_seller)
#         return
#     cart_product.filter(product_name=slug, product_seller__pk=product_seller).update(count=F('count') + change)
#
#
# def get_cart_product_list(user):
#     '''метод возвращает список товаров в корзине'''
#     return Cart.objects.filter(profile=user)
#
#
# def get_cart_product_amt(user):
#     '''метод возвращает кол-во товаров вв корзине'''
#     return len(get_cart_product_list(user))
#
#
# def get_total_price(user):
#     total_price = 0
#     for cart_product in get_cart_product_list(user):
#         total_price += cart_product.product_seller.price * cart_product.count
#     return total_price
#
#
# def change_seller(user, product_seller):
#     Cart.objects.filter(profile=user).update(product_seller__pk=product_seller)
#     return
