# citing https://www.w3resource.com/ for help (especially in password conditions)
# citing working with Victoria Shirriff on /check

# Stock buying an selling web app
import os
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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


# # Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


# @app.route("/")
# @login_required
# def index():
#     """Show portfolio of stocks"""

#     # Collect user id
#     id = session["user_id"]

#     # Lookup information about user's stock shares
#     table = db.execute(
#         "SELECT symbol, name, SUM(shares) as shares FROM history WHERE id = :id GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY symbol", id=id)

#     # Create list of total value of all shares of each stock
#     totals = []
#     for stock in table:
#         totals.append(stock["shares"] * lookup(stock["symbol"])["price"])

#     # Create list of prices of each stock
#     prices = []
#     for stock in table:
#         prices.append(usd(lookup(stock["symbol"])["price"]))

#     # Obtain number of unique owned stocks
#     rows = range(len(table))

#     # Query database for cash
#     cash = db.execute("SELECT cash FROM users WHERE id = :id", id=id)[0]["cash"]

#     # Create sum of the user's cash plus the sum of all the stock shares owned
#     add = usd(sum(totals) + cash)

#     # Render the index html template
#     return render_template("index.html", cash=cash, table=table, totals=totals, prices=prices, rows=rows, add=add)


# @app.route("/buy", methods=["GET", "POST"])
# @login_required
# def buy():
#     """Buy shares of stock"""

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Collect user's input for symbol and shares
#         symbol = request.form.get("symbol")
#         shares = request.form.get("shares")

#         # Ensure user inputed a valid symbol
#         if not symbol or not lookup(symbol):
#             return apology("Please input a valid symbol")

#         # Ensure user inputed a number of shares
#         if not shares:
#             return apology("Please input shares")

#         # Ensure shares input was a digit
#         if not shares.isdigit():
#             return apology("Please input a valid number")

#         # Ensure shares input is not letters
#         if shares.isalpha() == True:
#             return apology("Please input a valid number")

#         # Ensure user inputs positive value of shares
#         shares = int(shares)
#         if shares < 0:
#             return apology("Please input a valid number of shares")

#         # Obtain name and price of symbol
#         name = lookup(symbol)["name"]
#         price = lookup(symbol)["price"]

#         # Collect user id
#         id = session["user_id"]

#         # Query database for cash and convert to integer
#         cash = db.execute("SELECT cash FROM users WHERE id = :id", id=id)
#         cash = int(cash[0]["cash"])

#         # Ensure user has enough money to buy stocks
#         if cash < price:
#             return apology("You do not have enough money")

#         # Update history database with transaction
#         db.execute("INSERT INTO history (datetime, id, symbol, name, shares, price) VALUES(datetime('now'), :id, :symbol, :name, :shares, :price)",
#                   id=id, symbol=symbol, name=name, shares=shares, price=price)

#         # Update user's cash
#         db.execute("UPDATE users SET cash = cash - (:price * :shares) WHERE id = :id",
#                   id=id, price=price, shares=shares)

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Collect username from user's input in register
    username = request.args.get("username")

    # Query database for username
    exist = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # Return error if username already exists
    if exist:
        return jsonify(False)

    # Return success if username does not exist
    if not exist:
        return jsonify(True)


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""

#     # Collect user's id
#     id = session["user_id"]

#     # Query database for all transactions
#     history = db.execute("SELECT symbol, shares, price, datetime FROM history WHERE id = :id ORDER BY datetime", id=id)

#     # Send dictionary to webpage
#     return render_template("history.html", history=history)


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


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Collect symbol from user's input
#         symbol = request.form.get("symbol")

#         # Determine if symbol exists
#         quote = lookup(symbol)
#         if not symbol or not quote:
#             return apology("Invalid symbol")

#         # Collect name and price
#         name = quote["name"]
#         price = quote["price"]

#         # Send user to the Quoted page
#         return render_template("quoted.html", name=name, price=price, symbol=symbol)

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Collect username, password, and confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username submitted
        if not username:
            return apology("Missing username!")

        # Ensure password and confirmation submitted
        elif not password or not confirmation:
            return apology("Missing password!")

        # Ensure password and confirmation match
        elif password != confirmation:  # i think this is my issue right here!!!
            return apology("Passwords don't match!")

        # Ensure password contains at least one letter and one number
        while True:
            if not re.search("[a-z]", password) and not re.search("[A-Z]", password):
                return apology("Password must contain letter")
            elif not re.search("[0-9]", password):
                return apology("Password must contain number")
            else:
                break

        # Query database for username
        exist = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensure username does not yet exist
        if exist:
            return apology("This username already exists!")

        # Protect password
        hash = generate_password_hash(password)

        # Insert new user into database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=hash)

        # Store login in the session
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     """Sell shares of stock"""

#     # Collect user id
#     id = session["user_id"]

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Get stock symbol and shares from user
#         symbol = request.form.get("symbol")
#         shares = request.form.get("shares")

#         # Verify input present
#         if not symbol:
#             return apology("Missing symbol")

#         # Verify input present
#         if not shares:
#             return apology("Missing shares")

#         # Verify shares is a digit
#         if not shares.isdigit():
#             return apology("Please input a valid number")

#         # Verify shares is not a letter
#         if shares.isalpha() == True:
#             return apology("Please input a valid number")

#         # Verify shares is greater than 0
#         shares = int(shares)
#         if shares < 0:
#             return apology("Please input a valid number of shares")

#         # Query database for sum of shares user has in stock
#         amount = db.execute("SELECT SUM(shares) as shares FROM history WHERE id = :id and symbol = :symbol", id=id, symbol=symbol)
#         amount = int(amount[0]["shares"])

#         # Verify user has enough shares
#         if shares > amount:
#             return apology("You do not have enough shares")

#         # Lookup name and current price of the stock
#         name = lookup(symbol)["name"]
#         sold_price = lookup(symbol)["price"]

#         # Get negative value of the number of shares sold
#         sold_shares = shares * -1

#         # Insert sell transaction into history, with price as a negative value
#         db.execute("INSERT INTO history (datetime, id, symbol, name, shares, price) VALUES(datetime('now'), :id, :symbol, :name, :shares, :price)",
#                   id=id, symbol=symbol, shares=sold_shares, price=sold_price, name=name)

#         # Update user's cash after subtracting out the price of the recent transaction
#         db.execute("UPDATE users SET cash = cash - (:price * :shares) WHERE id = :id",
#                   id=id, price=sold_price, shares=sold_shares)

#         # Redirect user to homepage
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         # Query database for list of user's stocks
#         stocks = db.execute("SELECT symbol FROM history WHERE id = :id GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY symbol", id=id)

#         # Send user to Sell page
#         return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
