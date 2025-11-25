from flask import Flask, render_template, request, redirect, flash, session
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mod10-client"

BASE_URL = "http://localhost/module10/public"
TOKEN_URL = f"{BASE_URL}/Api/access_token"
API_V8 = f"{BASE_URL}/Api/V8/module"

CLIENT_ID = "28a99247-3767-43ea-f308-692421e042c6"
CLIENT_SECRET = "mod10-client"


# =========================== HOME ===========================
@app.route("/")
def home():
    if "access_token" not in session:
        return redirect("/login")
    return redirect("/dashboard")


# =========================== DASHBOARD ===========================
@app.route("/dashboard")
def dashboard():
    if "access_token" not in session:
        return redirect("/login")

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json"
    }

    # --- GET HOSPITAL LIST ---
    hospital_url = f"{API_V8}/ha_hospital"
    hospital_res = requests.get(hospital_url, headers=headers)

    hospital_count = 0
    recent_hospitals = []

    if hospital_res.status_code == 200:
        json_data = hospital_res.json()
        all_hospitals = json_data.get("data", [])
        hospital_count = len(all_hospitals)

        # ambil 5 data terbaru
        recent_hospitals = all_hospitals[:5]

    # Dashboard data final
    dashboard_data = {
        "hospital_count": hospital_count,
        "recent_hospitals": recent_hospitals
    }

    return render_template("dashboard.html", dashboard=dashboard_data)


# =========================== LOGIN ===========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": request.form["username"],
            "password": request.form["password"]
        }

        res = requests.post(TOKEN_URL, data=data)

        if res.status_code == 200:
            token = res.json().get("access_token")

            if token:
                session["access_token"] = token
                flash("Login berhasil!", "success")
                return redirect("/dashboard")
            else:
                flash("Login gagal! Token tidak ditemukan.", "danger")
        else:
            flash("Login gagal! Periksa username/password.", "danger")

    return render_template("login.html")


# =========================== CREATE HOSPITAL ===========================
@app.route("/hospital/create", methods=["GET", "POST"])
def create_hospital():
    if "access_token" not in session:
        return redirect("/login")

    if request.method == "POST":

        data = {
            "data": {
                "type": "ha_hospital",
                "attributes": {
                    "name": request.form.get("name"),
                    "unit": request.form.get("unit"),
                    "address": request.form.get("address"),
                    "phone": request.form.get("phone"),
                    "description": request.form.get("description"),
                    "date_entered": datetime.now().isoformat(),
                    "deleted": 0
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {session['access_token']}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_V8, json=data, headers=headers)

        if response.status_code in [200, 201]:
            flash("Rumah sakit berhasil ditambahkan!", "success")
        else:
            flash(f"Error: {response.text}", "danger")

        return redirect("/hospital/create")

    return render_template("hospital_form.html")


# =========================== GET HOSPITAL LIST ===========================
@app.route('/hospitals')
def get_hospitals():

    # wajib login
    if "access_token" not in session:
        flash("Silakan login dulu", "warning")
        return redirect("/login")

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/Api/V8/module/ha_hospital"
    response = requests.get(url, headers=headers)

    # token invalid / expired
    if response.status_code == 401:
        flash("Sesi habis, silakan login ulang", "danger")
        session.clear()
        return redirect("/login")

    if response.status_code == 200:
        hospitals = response.json()
        return render_template("hospitals.html", hospitals=hospitals)
    else:
        flash(f"Error GET Hospital: {response.text}", "danger")
        return redirect("/hospital/create")

# =========================== LOGOUT ===========================
@app.route("/logout")
def logout():
    session.clear()
    flash("Berhasil logout!", "info")
    return redirect("/login")


# =========================== MAIN ===========================
if __name__ == "__main__":
    app.run(debug=True)
