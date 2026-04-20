from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import re
import os
from pathlib import Path
import pandas as pd

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "register.db"
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_REGEX = re.compile(r"^[0-9+\-()\s]{6,20}$")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS register (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ovog TEXT NOT NULL,
            ner TEXT NOT NULL,
            utas TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))

def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone.strip()))

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ovog = request.form.get("ovog", "").strip()
        ner = request.form.get("ner", "").strip()
        utas = request.form.get("utas", "").strip()
        email = request.form.get("email", "").strip()

        if not ovog or not ner or not utas or not email:
            flash("Бүх талбарыг бөглөнө үү.", "error")
            return render_template("register.html")

        if not is_valid_email(email):
            flash("Email формат буруу байна. Жишээ: name@example.com", "error")
            return render_template("register.html", form_data=request.form)

        if not is_valid_phone(utas):
            flash("Утасны дугаарын формат буруу байна. Зөвхөн тоо, +, -, (), зай ашиглаж болно.", "error")
            return render_template("register.html", form_data=request.form)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO register (ovog, ner, utas, email) VALUES (?, ?, ?, ?)",
                (ovog, ner, utas, email)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("Энэ email өмнө нь бүртгэгдсэн байна.", "error")
            return render_template("register.html", form_data=request.form)
        conn.close()

        return redirect(url_for("success"))

    return render_template("register.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/admin")
def admin():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM register ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", rows=rows)

@app.route("/admin/export-excel")
def export_excel():
    conn = get_connection()
    df = pd.read_sql_query("SELECT id, ovog, ner, utas, email, created_at FROM register ORDER BY id DESC", conn)
    conn.close()

    file_path = EXPORT_DIR / "register.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="register.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
