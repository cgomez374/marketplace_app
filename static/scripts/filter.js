/**
THIS SECTION WILL ALLOW TO FILTER THE PRODUCTS BY CATEGORIES
AND TO SORT BY VARIOUS OPTIONS SUCH AS PRICE
**/

const categoryDropdown = document.getElementById('categories')
const sortDropdown = document.getElementById('sort')

const products = document.querySelectorAll('#products li')

const swapItems = (start, next) => {
    let temp = products[next].innerHTML
    products[next].innerHTML = products[start].innerHTML
    products[start].innerHTML = temp
}

const sortByPrice = (comparisonOp) => {
    let start = 0
    let next = start + 1
    while (start < products.length - 1) {
        if (products[start].style.display !== 'none' &&  products[next].style.display !== 'none'){
            let priceStart = Number(products[start].querySelector('#price').innerText.slice(1))
            let priceNext =  Number(products[next].querySelector('#price').innerText.slice(1))
            if (comparisonOp === '>'){
                if (priceNext > priceStart){
                    swapItems(start, next)
                }
            } else if (comparisonOp === '<'){
                if (priceNext < priceStart){
                    swapItems(start, next)
                }
            }

        }

        next++
        if (next >= products.length){
            start++
            next = start + 1
        }
    }
 }

const categoryFilterEventFunction = () => {
    let category = categoryDropdown.value.toLowerCase()
    products.forEach(product => {
        if (category){
            if (!product.innerHTML.includes(category)){
                product.style.display = 'none'
            } else {
                product.style.display = 'block'
            }
        } else if (!category){
            product.style.display = 'block'
        }
    })
    sortByEventFunction()
}

const sortByEventFunction = () => {
    let sortBy = sortDropdown.value.toLowerCase()
    if (sortBy === 'price_high'){
        sortByPrice('>')
    } else if (sortBy === 'price_low') {
        sortByPrice('<')
    }
}

categoryDropdown.addEventListener('change', categoryFilterEventFunction)
sortDropdown.addEventListener('change', sortByEventFunction)
