/**
    THIS SCRIPT WILL HANDLE THE SAVING AND ACCESSING OF THE CART
    USING LOCALSTORAGE
**/

productDiv = document.getElementById('productDetails')
emptyCart = {
    'subtotal': 0,
    'tax': 0,
    'total': 0
}

const checkOutButton = () => {
    if (Object.keys(JSON.parse(localStorage.getItem('cart'))).length <= 3){
        document.getElementById('checkOutButton').disabled = 'False'
    } else if (Object.keys(JSON.parse(localStorage.getItem('cart'))).length > 3){
        document.getElementById('checkOutButton').disabled = 'True'
    }
}

const showCartItems = () => {
    const productsInCartUl = document.getElementById('productsInCart')
    const localCart = JSON.parse(localStorage.getItem('cart'))

    if (!localCart) {
        localStorage.setItem('cart', JSON.stringify(emptyCart))
    }

    if (Object.keys(localCart).length <= 3){
        const newLi = document.createElement('li')
        newLi.setAttribute('class', 'sub-container row')

        const newH3 = document.createElement('h3')
        newH3.textContent = '- Empty Cart -'

        newLi.appendChild(newH3)
        productsInCartUl.appendChild(newLi)
    } else {
        for(const product in localCart){
            if (product !== 'subtotal' && product !== 'tax' && product !== 'total') {
                let name = localCart[product]['name']

                let price = parseFloat(localCart[product]['price'])
                let image_url = localCart[product]['image_url']

                // NEW LI
                const newLi = document.createElement('li')
                newLi.setAttribute('class', 'row')

                // NEW IMG
                const newImgEl = document.createElement('img')
                newImgEl.setAttribute('src', image_url)
                newImgEl.setAttribute('alt', 'product image')

                // NEW DIV WITH CLASS COL
                const newDiv = document.createElement('div')
                newDiv.setAttribute('class', 'col')

                // H4 FOR NAME
                const newH4 = document.createElement('h4')
                newH4.textContent = name

                // P FOR PRICE
                const newPEl = document.createElement('p')
                let formattedPrice = price.toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                });
                newPEl.textContent = 'price: $' + formattedPrice

                // DELETE BUTTON
                const buttonEle = document.createElement('button')
                buttonEle.setAttribute('id', 'deleteButton')
                buttonEle.setAttribute('data-customdata', product)
                buttonEle.setAttribute('onclick', 'deleteFromCart(event)')
                buttonEle.textContent = 'delete'

                // APPEND THEM ALL TOGETHER
                newLi.appendChild(newImgEl)
                newLi.appendChild(newDiv)
                newDiv.appendChild(newH4)
                newDiv.appendChild(newPEl)
                newDiv.appendChild(buttonEle)

                //APPEND TO THE DOM
                productsInCartUl.appendChild(newLi)
            }
        }

        document.getElementById('itemsInCart').classList.remove('hidden')
    }

    showCartTotals()
    // checkOutButton()
}

const addToCart = () => {
    let name = productDiv.querySelector('#product_name').innerText
    let description = productDiv.querySelector('#product_desc').innerText
    let price = productDiv.querySelector('#product_price').innerText.replace(/[\$,]/g, '')
    let seller = productDiv.querySelector('#product_seller').innerText
    let image_url = document.getElementById('productImg').src
    let itemsInCartEl = document.getElementById('itemsInCart')

    if (!JSON.parse(localStorage.getItem('cart'))) {
        localStorage.setItem('cart', JSON.stringify({}))
    }
    const localCart = JSON.parse(localStorage.getItem('cart'))
    let id = Object.keys(localCart).length + 1

    if (localCart[id]) {
        id++
    }

    itemsInCartEl.classList.remove('hidden')

    localCart[id] = {
        'name': name,
        'description': description,
        'price': price,
        'seller': seller,
        'image_url': image_url
    }

    localStorage.setItem('cart', JSON.stringify(localCart))
    setTotal()
}

const deleteFromCart = (event) => {
    const localCart = JSON.parse(localStorage.getItem('cart'))
    let itemToRemove = event.target.getAttribute('data-customdata')

    for (const product in localCart){
        if (product === itemToRemove){
            delete localCart[product]
        }
    }
    localStorage.setItem('cart', JSON.stringify(localCart))
    setTotal()
    location.reload()
}

const setTotal = () => {
    const localCart = JSON.parse(localStorage.getItem('cart'))
    let total = 0
    let tax = 0
    for (let item in localCart){
        if (item !== 'subtotal' && item !== 'tax' && item !== 'total'){
            total += parseInt(localCart[item]['price'])
        }
    }

    tax = Math.round(total * 0.08)

    localCart['subtotal'] = total
    localCart['tax'] = tax
    localCart['total'] = total + tax

    localStorage.setItem('cart', JSON.stringify(localCart))
}

const showCartTotals = () => {
    const localCart = JSON.parse(localStorage.getItem('cart'))
    let subTotalEl = document.getElementById('subTotal')
    let taxEl = document.getElementById('tax')
    let totalEl = document.getElementById('total')

    subTotalEl.innerText = parseInt(localCart['subtotal']).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                });
    taxEl.innerText = parseInt(localCart['tax']).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                });
    totalEl.innerText = parseInt(localCart['total']).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                });
}

// EVENT LISTENERS
document.addEventListener('DOMContentLoaded', showCartItems)

if (Object.keys(JSON.parse(localStorage.getItem('cart'))).length <= 3){
    document.getElementById('checkOutButton').disabled = true
} else if (Object.keys(JSON.parse(localStorage.getItem('cart'))).length > 3){
    document.getElementById('checkOutButton').disabled = false
}

