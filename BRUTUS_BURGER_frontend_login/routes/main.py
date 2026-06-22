from urllib.parse import quote

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from routes.auth import login_required

main_bp = Blueprint("main", __name__)
SUPPORTED_OPGG_REGIONS = (
    ("br", "Brasil"),
    ("eune", "EUNE"),
    ("euw", "EUW"),
    ("jp", "Japón"),
    ("kr", "Corea"),
    ("lan", "LAN"),
    ("las", "LAS"),
    ("na", "NA"),
    ("oce", "Oceanía"),
    ("ru", "Rusia"),
    ("tr", "Turquía"),
)


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
            flash("Invocador y región son obligatorios.", "danger")
            return redirect(url_for("main.opgg_stats"))
        if region not in {code for code, _ in SUPPORTED_OPGG_REGIONS}:
            flash("Selecciona una región válida.", "danger")
            return redirect(url_for("main.opgg_stats"))
        try:
            lp_value = int(lp) if lp else 0
            wins_value = int(wins) if wins else 0
            losses_value = int(losses) if losses else 0
        except ValueError:
            flash("LP, victorias y derrotas deben ser números enteros.", "danger")
            return redirect(url_for("main.opgg_stats"))
        if lp_value < 0 or wins_value < 0 or losses_value < 0:
            flash("LP, victorias y derrotas no pueden ser negativos.", "danger")
            return redirect(url_for("main.opgg_stats"))

        encoded_region = quote(region, safe="")
        encoded_summoner_name = quote(summoner_name)
        profile_url = f"https://www.op.gg/summoners/{encoded_region}/{encoded_summoner_name}"

        session["opgg_stats"] = {
            "summoner_name": summoner_name,
            "region": region,
            "ranked_tier": ranked_tier or "Sin registrar",
            "lp": str(lp_value),
            "wins": str(wins_value),
            "losses": str(losses_value),
            "kda": kda or "0.00",
            "main_champion": main_champion or "Sin registrar",
            "profile_url": profile_url,
        }
        flash("Estadísticas de OP.GG actualizadas.", "success")
        return redirect(url_for("main.opgg_stats"))

    return render_template(
        "opgg.html",
        opgg_stats=session.get("opgg_stats"),
        supported_regions=SUPPORTED_OPGG_REGIONS,
    )
