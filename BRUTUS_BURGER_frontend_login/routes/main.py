from flask import Blueprint, render_template, session

from routes.auth import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        user_email=session.get("user_email"),
    )
