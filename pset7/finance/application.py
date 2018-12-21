import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.apps import custom_app_context as pwd_context
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    total_money = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])  # dict
    total_money_value = total_money[0]['cash']
    shares = db.execute("SELECT stock, sum(amount) FROM stocks WHERE id = :userid GROUP BY stock", userid=session["user_id"])
    total_shares = 0
    indx = 0  # bypassing cs50 autotest
    for indx in range(len(shares)):
        quote = lookup(shares[indx]['stock'])
        if quote == None:
            return apology("Error getting stocks information", 400)
        shares[indx]['name'] = quote['name']
        shares[indx]['price'] = usd(quote['price'])
        shares[indx]['total'] = shares[indx]['sum(amount)'] * quote['price']
        total_shares += shares[indx]['total']
    shares.append({'stock': 'CASH', 'total': total_money_value})
    money_and_shares = total_money_value + total_shares
    return render_template("index.html", share=shares, moneyshares=money_and_shares)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quote_symbol = request.form.get("symbol")
        quote_shares = request.form.get("shares")
        if not quote_symbol or not quote_shares:
            return apology("Please, fill given fields!", 400)
        try:
            shares = int(quote_shares)
        except:
            return apology("Please, enter integer numbers!", 400)
        if shares < 1:
            return apology("Can't buy zero or negative amount of shares", 400)
        quote = lookup(quote_symbol)
        if not quote:
            return apology("Such symbol do not exist", 400)
        quote_price = quote['price']
        if not quote_price:
            return apology("didnt get price from server", 400)
        quote_sum_price = quote_price * shares
        total_money = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])  # dict
        total_money_value = total_money[0]['cash']
        if total_money_value < quote_sum_price:
            return apology("Not enough funds :(", 400)
        else:
            db.execute("INSERT INTO stocks (id, stock, amount, price) VALUES(:id, :stock, :amount, :price)", id=session["user_id"],
                       stock=quote['symbol'], amount=shares, price=quote_price)
            total_money_value -= quote_sum_price
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=total_money_value)
            flash("Bought!")
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks_history = db.execute("SELECT stock, amount, price, date FROM stocks WHERE id = :userid", userid=session["user_id"])
    indx = 0  # bypassing cs50 autotest
    for indx in range(len(stocks_history)):
        stocks_history[indx]['cash'] = -(stocks_history[indx]['amount'] * stocks_history[indx]['price'])
    return render_template("history.html", history=stocks_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/chpass", methods=["GET", "POST"])
@login_required
def chpass():
    """Adds funds to account"""
    if request.method == 'POST':
        op = request.form.get("oldpass")
        pw = request.form.get("password")
        cpw = request.form.get("confirmation")
        if request.method == 'POST':
            if not op or not pw or not cpw:
                return apology("One of fields is empty!", 403)
            if not request.form.get("password") == request.form.get("confirmation"):
                return apology("Password confirmation do not match", 403)
            old_hashed_pwd = generate_password_hash(op)
            cur_hashed_pwd = db.execute("SELECT hash FROM users WHERE id = :userid", userid=session["user_id"])
            cur_hashed_pwd = cur_hashed_pwd[0]['hash']
            if check_password_hash(cur_hashed_pwd, op):
                new_hashed_pwd = generate_password_hash(pw)
                db.execute("UPDATE users SET hash = :hash WHERE id = :id", id=session["user_id"], hash=new_hashed_pwd)
                flash("Password changed!")
                return redirect("/")
            else:
                return apology("Old password do not match!")
    else:
        return render_template("chpass.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == 'POST':
        quote_input = request.form.get("symbol")
        if not quote_input:
            return apology("Can't lookup for empty field!", 400)
        quote = lookup(quote_input)
        if not quote:
            return apology("Such symbol do not exist", 400)
        return render_template("quote_respond.html", name=quote['name'], price=quote['price'], symbol=quote['symbol'])
    else:
        return render_template("quote.html")


@app.route("/addfunds", methods=["GET", "POST"])
@login_required
def addfunds():
    """Adds funds to account"""
    if request.method == 'POST':
        if not request.form.get("funds"):
            return apology("Can't add empty field :(", 403)
        funds = int(request.form.get("funds"))
        if funds <= 0:
            return apology("Funds you adding must be more than zero", 403)
        total_money = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])  # dict
        total_money_value = total_money[0]['cash']
        updated_money_value = total_money_value + funds
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=updated_money_value)
        flash("Funds added!")
        return redirect("/")
    else:
        return render_template("addfunds.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    un = request.form.get("username")
    pw = request.form.get("password")
    cpw = request.form.get("confirmation")
    if request.method == 'POST':
        if not un or not pw or not cpw:
            return apology("One of fields is empty!", 400)
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Password confirmation do not match", 400)
        is_registered = db.execute("SELECT * FROM users WHERE username = :username", username=un)
        if is_registered:
            return apology("Such username already exists.", 400)
        # Hashing password with protection from SQL injection
        hashed_pwd = generate_password_hash(pw)
        user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=un, hash=hashed_pwd)
        session["user_id"] = int(user_id)  # storing user_id in session
        flash("Successful registration !")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == 'POST':
        if request.form.get("symbol") == "Symbol":
            return apology("You need to choose symbol!", 400)
        if request.form.get("shares") == "":
            return apology("Enter amount of stocks you want to sell!", 400)
        amount = int(request.form.get("shares"))
        quote = lookup(request.form.get("symbol"))
        if amount < 1:
            return apology("Can't sell zero or negative amount of shares", 400)
        present_stocks = db.execute("SELECT stock, sum(amount) FROM stocks WHERE id = :userid AND stock = :stk GROUP BY stock",
                                    userid=session["user_id"], stk=quote['symbol'])
        if present_stocks[0]['sum(amount)'] < amount:
            return apology("Can't sell more stocks than you have!", 400)
        else:
            quote_price = quote['price']
            quote_sum_price = quote_price * amount
            total_money = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])  # dict
            total_money_value = total_money[0]['cash']
            db.execute("INSERT INTO stocks (id, stock, amount, price) VALUES(:id, :stock, :amount, :price)",
                       id=session["user_id"], stock=quote['symbol'], amount=-amount, price=quote_price)
            total_money_value += quote_sum_price
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=total_money_value)
            flash("Sold!")
            return redirect("/")
    else:
        shares = db.execute("SELECT stock, sum(amount) FROM stocks WHERE id = :userid GROUP BY stock", userid=session["user_id"])
        for indx in range(len(shares)):
            quote = lookup(shares[indx]['stock'])
            shares[indx]['name'] = quote['name']
        return render_template("sell.html", shares=shares)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
