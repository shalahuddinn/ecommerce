import json
from .models import *


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
    }


def cookieCart(request):
    # Try catch prevent null cookie
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    # print("Cart: {}".format(cart))
    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'shipping': False
    }
    cartItems = order['get_cart_items']

    for x in cart:
        # Try catch prevent an error if the item in the database has been deleted
        # but a user has add that item to the cart
        try:
            cartItems += cart[x]['quantity']

            product = Product.objects.get(id=x)
            total = product.price * cart[x]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[x]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[x]['quantity'],
                'get_total': total
            }

            items.append(item)

            if not product.digital:
                order['shipping'] = True
        except:
            pass
    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
    }


def guestOrder(request, data):
    print('User is not logged in')

    print("Cookies: {}".format(request.COOKIES))

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
