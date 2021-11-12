let updateBtns = document.getElementsByClassName('update-cart');
console.log(user);

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        console.log('USER:', user);
        if (user === "AnonymousUser") {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    })
}

function addCookieItem(productId, action) {
    console.log("User is not logged in..");
    console.log(cart)

    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = {
                'quantity': 1
            };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log("Remove Item");
            delete cart[productId];
        }
    }
    // Update the cookie
    console.log("Cart:", cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

    location.reload();
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data..');

    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    }).then(response =>
        response.json()
    ).then(data => {
        console.log('data:', data);
        location.reload()
    })

}


