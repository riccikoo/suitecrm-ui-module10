from flask import session, flash, redirect, request, render_template
import requests
from config import TOKEN_URL, CLIENT_ID, CLIENT_SECRET
from services.suitecrm_service import SuiteCRMService

def dashboard():
    if "access_token" not in session:
        return redirect("/login")

    token = session["access_token"]

    hospital_res = SuiteCRMService.get_all("ha_hospital", token)

    hospital_count = 0
    recent_hospitals = []

    if hospital_res.status_code == 200:
        json_data = hospital_res.json()
        all_hospitals = json_data.get("data", [])
        hospital_count = len(all_hospitals)
        recent_hospitals = all_hospitals[:5]  # ambil 5 data terbaru

    dashboard_data = {
        "hospital_count": hospital_count,
        "recent_hospitals": recent_hospitals
    }

    return render_template("dashboard.html", dashboard=dashboard_data)

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
                return redirect("/")
        flash("Login gagal", "danger")

    # Jika GET atau gagal login
    return render_template("login.html")

def logout():
    session.clear()
    flash("Logout berhasil", "info")
    return redirect("/login")
