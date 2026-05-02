from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # для работы сессий

DATA_FILE = "balance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "last_reset" not in data:
                data["last_reset"] = datetime.now().strftime("%Y-%m-%d")
            return data
    return {"balance": 1000, "last_reset": datetime.now().strftime("%Y-%m-%d")}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Главная страница (для ребёнка)
@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()

    # Еженедельный бонус
    today = datetime.now()
    last_reset = datetime.strptime(data["last_reset"], "%Y-%m-%d")
    if today.weekday() == 5 and (today - last_reset).days >= 6:
        data["balance"] += 1000
        data["last_reset"] = today.strftime("%Y-%m-%d")
        save_data(data)

    if request.method == "POST":
        action = request.form.get("action")
        if action == "add100":
            data["balance"] += 100
        elif action == "minus50" and data["balance"] >= 50:
            data["balance"] -= 50
        elif action == "minus100" and data["balance"] >= 100:
            data["balance"] -= 100
        save_data(data)
        return redirect("/")

    return render_template("index.html", balance=data["balance"])

# Логин в админку
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if login == "1234" and password == "1234":
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Неверный логин или пароль. Попробуй ещё раз."
    return """
    <h2 style="text-align:center; margin-top:100px;">Вход в админ-кабинет</h2>
    <form method="POST" style="max-width:300px; margin:50px auto; text-align:center;">
        <input type="text" name="login" placeholder="Логин" style="padding:10px; width:100%; margin:10px 0;" required><br>
        <input type="password" name="password" placeholder="Пароль" style="padding:10px; width:100%; margin:10px 0;" required><br>
        <button type="submit" style="padding:12px 30px; font-size:18px;">Войти</button>
    </form>
    """

# Админ-панель
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = load_data()

    if request.method == "POST":
        if "reset" in request.form:
            data["balance"] = 1000
            data["last_reset"] = datetime.now().strftime("%Y-%m-%d")
        elif "set_balance" in request.form:
            try:
                data["balance"] = int(request.form.get("new_balance"))
            except:
                pass
        save_data(data)
        return redirect("/admin")

    return render_template("admin.html", balance=data["balance"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    print("🚀 Приложение запущено!")
    print("Главный интерфейс: http://127.0.0.1:5000")
    app.run(debug=True)