/**
    THIS SCRIPT WILL HANDLE THE SAVING AND ACCESSING OF THE CART
    USING LOCALSTORAGE
**/

productDiv = document.getElementById('product')

const showCartItems = () => {
    const productsInCartUl = document.getElementById('productsInCart')
    const localCart = JSON.parse(localStorage.getItem('cart'))

    if (!Object.keys(localCart).length){
        const newLi = document.createElement('li')
        newLi.setAttribute('class', 'sub-container row')

        const newH3 = document.createElement('h3')
        newH3.textContent = '- Empty Cart -'

        newLi.appendChild(newH3)
        productsInCartUl.appendChild(newLi)
    } else {
        for(const product in localCart){
            let name = localCart[product]['name']
            let price = localCart[product]['price']
            let image_url = localCart[product]['image_url']

            // NEW LI
            const newLi = document.createElement('li')
            newLi.setAttribute('class', 'sub-container row')

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
            newPEl.textContent = 'price: $' + price

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

    showCartTotals()
}

const addToCart = () => {
    let name = productDiv.querySelector('#product_name').innerText
    let description = productDiv.querySelector('#product_desc').innerText
    let price = productDiv.querySelector('#product_price').innerText
    let seller = productDiv.querySelector('#product_seller').innerText
    let image_url = document.getElementById('productImg').src

    if (!JSON.parse(localStorage.getItem('cart'))) {
        localStorage.setItem('cart', JSON.stringify({}))
    }
    const localCart = JSON.parse(localStorage.getItem('cart'))
    let id = Object.keys(localCart).length + 1

    localCart[id] = {
        'name': name,
        'description': description,
        'price': price,
        'seller': seller,
        'image_url': image_url
    }
    localStorage.setItem('cart', JSON.stringify(localCart))
}

const deleteFromCart = (event) => {
    const localCart = JSON.parse(localStorage.getItem('cart'))
    // GET THE PARENT ELEMENT SOMEHOW
    let itemToRemove = event.target.getAttribute('data-customdata')

    for (const product in localCart){
        if (product === itemToRemove){
            delete localCart[product]
        }
    }
    localStorage.setItem('cart', JSON.stringify(localCart))
    location.reload()
}

const showCartTotals = () => {
    const localCart = JSON.parse(localStorage.getItem('cart'))
    let total = 0
    let tax = 0
    for (let item in localCart){
        total += parseInt(localCart[item]['price'])
    }
    tax = total * 0.08

    let subTotalEl = document.getElementById('subTotal')
    let taxEl = document.getElementById('tax')
    let totalEl = document.getElementById('total')

    subTotalEl.innerText = total.toString()
    taxEl.innerText = tax.toString()
    totalEl.innerText = (total + tax).toString()
}

// EVENT LISTENERS
document.addEventListener('DOMContentLoaded', showCartItems)

