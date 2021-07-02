import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    transactions = db.execute("SELECT * FROM portfolio WHERE user_id=?", session["user_id"])
    total = 0
    for transaction in transactions:
        quote = lookup(transaction["symbol"])
        transaction["shares"] = int(transaction["shares"])
        transaction["name"] = quote["name"]
        transaction["price"] = quote["price"]
        total += transaction["price"]*transaction["shares"]
    user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    total += user_cash
    return render_template("index.html", transactions=transactions, user_cash=user_cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method =="POST":
        
        share = lookup(request.form.get("symbol"))
        
        if not share:
            return apology("this symbol doesn't exist", 403)
            
        num_of_shares = int(request.form.get("shares"))    
        if num_of_shares <= 0:
            return apology("you must provide a positive integer", 403)
        
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        cost = share["price"]*num_of_shares
        
        if user_cash < cost:
            return apology("not enough funds", 403)
            
        db.execute("UPDATE users SET cash=? WHERE id=?", user_cash-cost, session["user_id"])    
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], share["symbol"], num_of_shares, share["price"])
        
        users_portfolio = db.execute("SELECT * FROM portfolio WHERE user_id=?", session["user_id"])
        if any (d["symbol"] == share["symbol"] for d in users_portfolio):
            users_shares = next(item for item in users_portfolio if item["symbol"] == share["symbol"])["shares"]
            db.execute("UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?", users_shares+num_of_shares, session["user_id"], share["symbol"])
        else:
            db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], share["symbol"], num_of_shares, share["price"])
        
        return redirect("/")
    else:
        
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM history WHERE user_id=?", session["user_id"])
    return render_template("history.html", transactions=transactions)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method =="POST":
        
        result = lookup(request.form.get("symbol"))
        if not result:
            return apology("this symbol doesn't exist")
        
        return render_template("quoted.html", name=result["name"], price=result["price"], symbol=result["symbol"])
    
    else:
        
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":
        
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)
            
        # Ensure username doesn't exist already
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return apology("that username already exists", 403)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 403)
            
        # Ensure confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("must provide confirmation", 403)
            
        # Ensure confirmation is equal to password
        if password != confirmation:
            return apology("confirmation is not equal the password", 403)
            
        # Hash password    
        hash = generate_password_hash(password)
        
        # Insert user to database
        user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        
        return redirect("/login")
        
    else:
        
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbols_db = db.execute("SELECT symbol FROM portfolio WHERE user_id=?", session["user_id"])
    symbols = [d["symbol"] for d in symbols_db]
    
    if request.method =="POST":
        
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("You must choose a symbol", 403)
        sold_shares = int(request.form.get("shares"))
        if not sold_shares:
            return apology("You must type a number of shares", 403)
            
        quote = lookup(symbol)
        price = quote["price"]
            
        data = db.execute("SELECT * FROM portfolio WHERE user_id=? AND symbol=?", session["user_id"], symbol)
        users_shares = data[0]["shares"]
        price = data[0]["price"]
        current_shares = int(users_shares) - int(sold_shares)
        profit = sold_shares * price
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        updated_cash = user_cash + profit
        
        if sold_shares > users_shares:
            return apology("You've got not enough shares", 403)
        
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, -sold_shares, price)
        if current_shares == 0:
            db.execute("DELETE FROM portfolio WHERE user_id=? AND symbol=?", session["user_id"], symbol)
        else:
            db.execute("UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?", current_shares, session["user_id"], symbol)
        db.execute("UPDATE users SET cash=? WHERE id=?", updated_cash, session["user_id"])
        
        return redirect("/")
    else:
        
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
