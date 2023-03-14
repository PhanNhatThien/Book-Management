function addToCart(id, name, price){
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type':'application/json'
        }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)

        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function(err){
        console.error(err)
    })
}

function pay(){
    if(confirm('Bạn chắc chắn muốn thanh toán không?') == true){
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
               location.reload()
        }).catch(err => console.error(err))
    }
}

function updateCart(id, obj) {
    fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type':'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity

        let amount = document.getElementById('total-amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}

function deleteCart(id){
    if (confirm("Bạn chắc chắn xóa sản phẩm này không?") == true){
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Content-Type':'application/json'
            }
        }).then(res => res.json()).then(data => {
            let counter = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity

            let amount = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let e = document.getElementById("product" + id)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }
}

function addComment(productId) {
    let content = document.getElementById('commentContent')
    fetch('/api/comments',{
        method: 'post',
        body: JSON.stringify({
            'product_id': productId,
            'content': content.value
        }),
        headers:{
            'Content-Type':'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        if(data.status == 201){
            let comments = document.getElementById('comments')
            comments.innerHTML = getHtmlComment(data.comment) + comments.innerHTML
            content.value =""
        }else
            alert("Thêm bình luận thất bại!!!")
    }).catch(err => console.error(err))
}


function loadComments(productId, page=1 ){
    fetch(`/api/products/${productId}/comments?page=${page}`).then(res => res.json()).then(data => {
        console.info(data)

        let comments = document.getElementById('comments')
//        comment.innerHTML = ""
//        for (let i = 0; i < data.length; i++)
//            comment.innerHTML += getHtmlComment(data[i])
    })
}

function getHtmlComment(comment){
    let image = comment.user.avatar
    if (image === null || !image.startsWidth('https'))
        image = '/static/images/logo-sach.jpg'


    return `
        <div class="row">
            <div class="col-md-1 col-xs-4">
                <img src="${image}"
                class="img-fluid rounded-circle" alt="${comment.user.username}"/>
            </div>
            <div class="col-md-11 col-xs-8">
                <p>${comment.content}</p>
                <p><em>${comment.created_date}</em></p>
            </div>
        </div>
    `
}