from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    melons = model.get_melons()
    return render_template("all_melons.html", melon_list=melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html", display_melon=melon)

@app.route("/cart")
def shopping_cart():
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart={}, total=0)
    else:
        items = session["cart"]
        dict_of_melons = {}

        total_price = 0
        for item in items:
            melon = model.get_melon_by_id(item)
            total_price += melon.price
            if melon.id in dict_of_melons:
                dict_of_melons[melon.id]["qty"] += 1
            else:
                dict_of_melons[melon.id] = {"qty": 1, "name": melon.common_name, "price": melon.price}

        return render_template("cart.html", display_cart=dict_of_melons, total=total_price)

@app.route("/remove/<int:id>")
def remove(id):
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return redirect("/cart")

    if id in session["cart"]:
        session["cart"].remove(id)
        flash("Item removed from the cart!")
    else:
        flash("Item not found in the cart.")

    return redirect("/cart")

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    session["logged_in"] = False
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("email")
        givenname = request.form.get("givenname")
        surname = request.form.get("surname")
        password = request.form.get("password")
        customer = model.get_customer_by_email(email)

        if customer:
            flash("That email is already in use.")
            return render_template("register.html")
        else:
            model.add_customer(email, givenname, surname, password)
            flash("You have successfully registered!")
            return redirect("/melons")

        

@app.route("/login", methods=["POST"])
def process_login():
    session["logged_in"] = False
    email = request.form.get("email")
    customer = model.get_customer_by_email(email)

    if customer:
        flash("Hoşgeldiniz, %s %s" % (customer.givenname, customer.surname))
        if "user" in session:
            session["logged_in"] = True
        else:
            session["user"] = email
            session["logged_in"] = True
        return redirect("/melons")
    else:
        flash("That is an invalid login.")
        session["logged_in"] = False
        return render_template("login.html")

@app.route("/checkout")
def checkout():
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port)
