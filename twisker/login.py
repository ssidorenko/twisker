from flask import request, flash, redirect, url_for, render_template
from twisker.main import login_manager, app
from models import TwiskUser
from flask_login import login_required, login_user, logout_user


@login_manager.user_loader
def load_user(userid):
    return TwiskUser.get_by_id(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        user = TwiskUser.get_by_id(request.form["username"])
        if user:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(user, remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
