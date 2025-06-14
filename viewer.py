from flask import Flask, render_template, request, Response, send_file, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_engine, get_session, ExchangeRate, User, Favorite
from io import StringIO, BytesIO
from openpyxl import Workbook
from datetime import datetime
import csv

app = Flask(__name__)
app.secret_key = "supersekretnyklucz"

# Logowanie
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Zaloguj się, aby uzyskać dostęp do aplikacji."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    engine = get_engine()
    session = get_session(engine)
    return session.query(User).get(int(user_id))


@app.route("/", methods=["GET"])
@login_required
def index():
    engine = get_engine()
    session = get_session(engine)

    # Lista dostępnych walut
    available_currencies = session.query(ExchangeRate.code).distinct().all()
    currency_list = sorted([code[0] for code in available_currencies])

    selected_currency = request.args.get("currency", "EUR")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    only_favorites = request.args.get("only_favorites") == "on"

    # Przetwarzanie dat
    start, end = None, None
    try:
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        flash("Niepoprawny format daty.", "danger")

    # Pobierz ulubione waluty użytkownika
    fav_rows = session.query(Favorite).filter_by(user_id=current_user.id).all()
    favorites = [f.currency_code for f in fav_rows]

    # Filtrowanie danych
    query = session.query(ExchangeRate)
    if only_favorites and favorites:
        query = query.filter(ExchangeRate.code.in_(favorites))
    else:
        query = query.filter_by(code=selected_currency)

    if start:
        query = query.filter(ExchangeRate.date >= start)
    if end:
        query = query.filter(ExchangeRate.date <= end)

    filtered_rates = query.order_by(ExchangeRate.date.asc()).all()

    labels = [r.date.strftime("%Y-%m-%d") for r in filtered_rates]
    values = [r.rate for r in filtered_rates]

    return render_template("rates.html",
                           rates=filtered_rates,
                           labels=labels,
                           values=values,
                           currency=selected_currency,
                           currencies=currency_list,
                           favorites=favorites,
                           start_date=start_date,
                           end_date=end_date,
                           only_favorites=only_favorites)


@app.route("/export")
@login_required
def export_csv():
    engine = get_engine()
    session = get_session(engine)

    currency = request.args.get("currency", "EUR")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = session.query(ExchangeRate).filter_by(code=currency)
    try:
        if start_date:
            query = query.filter(ExchangeRate.date >= datetime.strptime(
                start_date, "%Y-%m-%d").date())
        if end_date:
            query = query.filter(ExchangeRate.date <= datetime.strptime(
                end_date, "%Y-%m-%d").date())
    except ValueError:
        pass

    rates = query.order_by(ExchangeRate.date.asc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Data", "Kod", "Waluta", "Kurs średni"])
    for r in rates:
        writer.writerow(
            [r.date.strftime("%Y-%m-%d"), r.code, r.currency, r.rate])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers[
        "Content-Disposition"] = f"attachment; filename=kursy_{currency}.csv"
    return response


@app.route("/export_xlsx")
@login_required
def export_xlsx():
    engine = get_engine()
    session = get_session(engine)

    currency = request.args.get("currency", "EUR")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = session.query(ExchangeRate).filter_by(code=currency)
    try:
        if start_date:
            query = query.filter(ExchangeRate.date >= datetime.strptime(
                start_date, "%Y-%m-%d").date())
        if end_date:
            query = query.filter(ExchangeRate.date <= datetime.strptime(
                end_date, "%Y-%m-%d").date())
    except ValueError:
        pass

    rates = query.order_by(ExchangeRate.date.asc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = f"Kursy {currency}"
    ws.append(["Data", "Kod", "Waluta", "Kurs średni"])
    for r in rates:
        ws.append([r.date.strftime("%Y-%m-%d"), r.code, r.currency, r.rate])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        download_name=f"kursy_{currency}.xlsx",
        as_attachment=True,
        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.route("/register", methods=["GET", "POST"])
def register():
    engine = get_engine()
    session = get_session(engine)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if session.query(User).filter_by(username=username).first():
            flash("Taki użytkownik już istnieje.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    engine = get_engine()
    session = get_session(engine)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Nieprawidłowa nazwa użytkownika lub hasło.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/toggle_favorite/<code>")
@login_required
def toggle_favorite(code):
    engine = get_engine()
    session = get_session(engine)

    fav = session.query(Favorite).filter_by(user_id=current_user.id,
                                            currency_code=code).first()
    if fav:
        session.delete(fav)
    else:
        new_fav = Favorite(user_id=current_user.id, currency_code=code)
        session.add(new_fav)

    session.commit()
    return ("", 204)


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def manage_favorites():
    engine = get_engine()
    session = get_session(engine)

    all_currencies = session.query(ExchangeRate.code).distinct().all()
    currency_list = sorted([c[0] for c in all_currencies])

    if request.method == "POST":
        selected = request.form.getlist("favorites")
        session.query(Favorite).filter_by(user_id=current_user.id).delete()
        for code in selected:
            fav = Favorite(user_id=current_user.id, currency_code=code)
            session.add(fav)
        session.commit()
        flash("✅ Ulubione waluty zostały zapisane.")
        return redirect(url_for("index"))

    existing = session.query(Favorite).filter_by(user_id=current_user.id).all()
    current_favorites = [f.currency_code for f in existing]

    return render_template("favorites.html",
                           currencies=currency_list,
                           current_favorites=current_favorites)
