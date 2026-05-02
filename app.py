from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import json
import os

app = Flask(__name__, template_folder="templates")   # ← Это важно!
app.secret_key = "supersecretkey"

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

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("login") == "1234" and request.form.get("password") == "1234":
            session["admin"] = True
            return redirect("/admin")
        else:
            return "<h2 style='text-align:center;margin-top:100px;color:red'>Неверный логин или пароль</h2>"
    return """
    <h2 style="text-align:center;margin-top:80px;">Вход в админку</h2>
    <form method="POST" style="max-width:300px;margin:40px auto;text-align:center;">
        <input type="text" name="login" placeholder="Логин" style="padding:12px;width:100%;margin:10px 0;" required><br>
        <input type="password" name="password" placeholder="Пароль" style="padding:12px;width:100%;margin:10px 0;" required><br>
        <button type="submit" style="padding:12px 40px;font-size:18px;">Войти</button>
    </form>
    """

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")
    data = load_data()
    if request.method == "POST":
        if "reset" in request.form:
            data["balance"] = 1000
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
    app.run(host="0.0.0.0", port=5000)
