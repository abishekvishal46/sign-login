from flask import Blueprint,render_template,request
from flask_login import login_required,current_user
views=Blueprint('views',__name__)
from .models import Cart


@views.route('/',methods=["POST","GET"])
@login_required
def home():
    if request.method == 'POST':
        products = request.form.getlist('products[]')
        prices = request.form.getlist('prices[]')

        # Now you have lists of products and prices
        for product, price in zip(products, prices):
            cart_items=Cart(data=product,price=price,user_id=current_user)


    return render_template("home.html", user=current_user)

@views.route('/')
@login_required
def shopping():
    return render_template("shop.html")
