from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models.user import User, db

auth_bp = Blueprint("auth", __name__)


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesion para acceder.", "warning")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapped_view


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")

        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return render_template("register.html")
        if not correo:
            flash("El correo es obligatorio.", "danger")
            return render_template("register.html")
        if len(password) < 6:
            flash("La contrasena debe tener al menos 6 caracteres.", "danger")
            return render_template("register.html")
        if User.query.filter_by(correo=correo).first():
            flash("El correo ya esta registrado.", "danger")
            return render_template("register.html")

        new_user = User(
            nombre=nombre,
            correo=correo,
            password_hash=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registro exitoso. Ahora inicia sesion.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(correo=correo).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Credenciales incorrectas.", "danger")
            return render_template("login.html")

        session["user_id"] = user.id
        session["user_name"] = user.nombre
        session["user_email"] = user.correo

        flash("Bienvenido al dashboard.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("main.home"))
