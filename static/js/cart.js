var updatebtns=document.getElementsByClassName('update-cart')
	
for(i=0;i<updatebtns.length;i++){
	updatebtns[i].addEventListener('click',function(){
		var productID=this.dataset.product
		var action =this.dataset.action
		console.log('productID',productID,'action',action)


		console.log('USER:',user)
		if(user=='AnonymousUser'){
			console.log('user is not authenticated')
		}else{
			updateUserOrder(productID,action)
		}
	})
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function updateUserOrder(productID,action){
	console.log('user is logged in')

	var url="/update_item/"

	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productID':productID,'action':action})
	})

	.then((response)=>{
		return response.json()
	})

	.then((data)=>{
		console.log('Data',data)
		location.reload()
	})
}