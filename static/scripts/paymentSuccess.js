/*

REMOVE ALL ITEMS IN THE CART ONCE THIS PAGE LOADS

*/

emptyCart = {
    'subtotal': 0,
    'tax': 0,
    'total': 0
}

const clearCart = () => {
    localStorage.setItem('cart', JSON.stringify(emptyCart))
}

// EVENT LISTENERS
document.addEventListener('DOMContentLoaded', clearCart)