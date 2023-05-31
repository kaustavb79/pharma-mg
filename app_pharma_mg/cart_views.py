from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app_account.models import Profile
from app_pharma_mg.models import Item, Order


@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Item.objects.get(pk=id)
    cart.add(product=product)
    return redirect("pharmamg:patient_home")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Item.objects.get(pk=id)
    cart.remove(product)
    return redirect("pharmamg:cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Item.objects.get(pk=id)
    cart.add(product=product)
    return redirect("pharmamg:cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Item.objects.get(pk=id)
    cart.decrement(product=product)
    return redirect("pharmamg:cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("pharmamg:cart_detail")


@login_required
def cart_detail(request):
    profile_get_qs = Profile.objects.get(user=request.user)
    total_amt = 0
    for id, item in request.session['cart'].items():
        total_amt += int(item['quantity']) * float(item['price'])
    return render(request, 'app_pharma_mg/customer/cart_detail.html', {'profile_get_qs':profile_get_qs,'total': total_amt + 19.47 + 20})


@login_required
def checkout(request):
    profile_get_qs = Profile.objects.get(user=request.user)
    total_amt = 0
    for id, item in request.session['cart'].items():
        total_amt += int(item['quantity']) * float(item['price'])
    return render(request, 'app_pharma_mg/customer/checkout.html', {'profile_get_qs':profile_get_qs,'total': total_amt + 19.47 + 20})


def order_detail(request):
    profile_get_qs = Profile.objects.get(user=request.user)
    order_filter_qs = Order.objects.filter(placed_by=profile_get_qs)
    return render(request, 'app_pharma_mg/customer/order_detail.html', {'profile_get_qs':profile_get_qs,"order_filter_qs":order_filter_qs})
