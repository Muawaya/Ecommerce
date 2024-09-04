from django.shortcuts import render,get_object_or_404
from.cart import Cart
from store.models import Product
from django.http import JsonResponse,HttpResponse



def cart_summary(request):
    cart = Cart(request)
    total_products = cart.get_total_product()
    return render(request, 'cart/cart_summary.html', {'cart': cart, 'total_products': total_products})



def cart_add(request):
     #get the cart
    cart = Cart(request)
     #test for POST
    if request.POST.get("action")=="post":
        #get  stuff
        product_id = int(request.post.get("product_id"))
        # lookup product in db
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product)
        
         #Get cart quantity

        cart_quantity = cart.__len__()


        #return  response
        response = JsonResponse({ 'qty' :  cart_quantity })
        return response
       
       
        
   



def cart_delete(recuest):
    pass

def cart_update(recuest):
    pass