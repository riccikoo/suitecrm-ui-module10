from flask import render_template, request, redirect, flash, session
from datetime import datetime
from services.suitecrm_service import SuiteCRMService

MODULE = "ha_doctor"


def index():
    token = session.get("access_token")
    res = SuiteCRMService.get_all(MODULE, token)
    doctors = res.json().get("data", []) if res.status_code == 200 else []
    return render_template("doctor/doctor.html", doctors=doctors)


def create():
    if request.method == "POST":
        token = session.get("access_token")

        data = {
            "data": {
                "type": MODULE,
                "attributes": {
                    "name": request.form.get("name"),
                    "gender": request.form.get("gender"),
                    "nik": request.form.get("nik"),
                    "no_sip": request.form.get("no_sip"),
                    "specialization": request.form.get("specialization"),
                    "email": request.form.get("email"),
                    "date_entered": datetime.now().isoformat(),
                    "deleted": 0
                }
            }
        }

        res = SuiteCRMService.create(token, data)

        if res.status_code in [200, 201]:
            flash("Dokter berhasil ditambahkan", "success")
            return redirect("/doctors")

        flash("Gagal menambahkan dokter", "danger")

    return render_template("doctor/doctor_create.html")


def edit(doctor_id):
    token = session.get("access_token")

    if request.method == "GET":
        res = SuiteCRMService.get_by_id(MODULE, doctor_id, token)
        doctor = res.json().get("data") if res.status_code == 200 else None
        return render_template("doctor/doctor_edit.html", doctor=doctor)

    if request.method == "POST":
        data = {
            "data": {
                "type": MODULE,
                "id": doctor_id,
                "attributes": {
                    "name": request.form.get("name"),
                    "gender": request.form.get("gender"),
                    "specialization": request.form.get("specialization"),
                    "email": request.form.get("email")
                }
            }
        }

        res = SuiteCRMService.update(token, data)

        if res.status_code in [200, 201]:
            flash("Data dokter berhasil diperbarui", "success")
            return redirect("/doctors")

        flash("Update gagal", "danger")
        return redirect(f"/doctor/edit/{doctor_id}")


def delete(doctor_id):
    token = session.get("access_token")
    res = SuiteCRMService.delete(MODULE, doctor_id, token)

    if res.status_code in [200, 204]:
        flash("Dokter berhasil dihapus", "success")
    else:
        flash("Gagal menghapus dokter", "danger")

    return redirect("/doctors")
