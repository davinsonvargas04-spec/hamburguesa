from urllib.parse import quote

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

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
        opgg_stats=session.get("opgg_stats"),
    )


@main_bp.route("/opgg", methods=["GET", "POST"])
@login_required
def opgg_stats():
    if request.method == "POST":
        summoner_name = request.form.get("summoner_name", "").strip()
        region = request.form.get("region", "").strip().lower()
        ranked_tier = request.form.get("ranked_tier", "").strip()
        lp = request.form.get("lp", "").strip()
        wins = request.form.get("wins", "").strip()
        losses = request.form.get("losses", "").strip()
        kda = request.form.get("kda", "").strip()
        main_champion = request.form.get("main_champion", "").strip()

        if not summoner_name or not region:
            flash("Invocador y region son obligatorios.", "danger")
            return redirect(url_for("main.opgg_stats"))

        profile_slug = quote(summoner_name.replace(" ", "-"))
        profile_url = f"https://www.op.gg/summoners/{region}/{profile_slug}"

        session["opgg_stats"] = {
            "summoner_name": summoner_name,
            "region": region.upper(),
            "ranked_tier": ranked_tier or "Sin registrar",
            "lp": lp or "0",
            "wins": wins or "0",
            "losses": losses or "0",
            "kda": kda or "0.00",
            "main_champion": main_champion or "Sin registrar",
            "profile_url": profile_url,
        }
        flash("Estadisticas de OP.GG actualizadas.", "success")
        return redirect(url_for("main.opgg_stats"))

    return render_template("opgg.html", opgg_stats=session.get("opgg_stats"))
