from flask import render_template, request, redirect, flash, session, jsonify
from datetime import datetime
import requests
from services.suitecrm_service import SuiteCRMService
from services.doctor_hospital_service import assign_doctor_to_hospital, unassign_doctor_from_hospital

MODULE = "ha_hospital"
DOCTOR_MODULE = "ha_doctor"

def index():
    token = session.get("access_token")
    res = SuiteCRMService.get_all(MODULE, token)

    if res.status_code == 200:
        return render_template("hospital/hospitals.html", hospitals=res.json())

    flash("Gagal mengambil data rumah sakit", "danger")
    return redirect("/dashboard")

def create():
    if request.method == "POST":
        token = session.get("access_token")

        payload = {
            "data": {
                "type": MODULE,
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

        res = SuiteCRMService.create(token, payload)

        if res.status_code in [200, 201]:
            flash("Rumah sakit berhasil ditambahkan!", "success")
            return redirect("/hospitals")

        flash(res.text, "danger")

    return render_template("hospital/hospital_form.html")

def edit(hospital_id):
    token = session.get("access_token")

    if request.method == "GET":
        res = SuiteCRMService.get_by_id(MODULE, hospital_id, token)

        if res.status_code == 200:
            return render_template(
                "hospital/hospital_edit.html",
                hospital=res.json()["data"]
            )

        flash("Data rumah sakit tidak ditemukan", "danger")
        return redirect("/hospitals")

    payload = {
        "data": {
            "type": MODULE,
            "id": hospital_id,
            "attributes": {
                "name": request.form.get("name"),
                "unit": request.form.get("unit"),
                "address": request.form.get("address"),
                "phone": request.form.get("phone"),
                "description": request.form.get("description"),
            }
        }
    }

    res = SuiteCRMService.update(token, payload)

    if res.status_code in [200, 201]:
        flash("Data rumah sakit berhasil diperbarui!", "success")
    else:
        flash(res.text, "danger")

    return redirect("/hospitals")

def delete(hospital_id):
    token = session.get("access_token")

    res = SuiteCRMService.delete(MODULE, hospital_id, token)

    if res.status_code in [200, 204]:
        flash("Rumah sakit berhasil dihapus", "success")
    else:
        flash(res.text, "danger")

    return redirect("/hospitals")

# -- Doctor Assignment Endpoints --

def get_assigned_doctors(hospital_id):
    token = session.get("access_token")

    url = f"{SuiteCRMService.API_V8}/ha_hospital/{hospital_id}/relationships/ha_doctor_ha_hospital_1"
    res = requests.get(url, headers=SuiteCRMService.headers(token))

    if res.status_code != 200:
        return jsonify({"doctors": []}), 200

    doctors_data = res.json().get("data", [])
    return jsonify({"doctors": doctors_data}), 200

def assign_doctor(hospital_id):
    token = session.get("access_token")
    data = request.json
    doctor_id = data.get("doctor_id")

    if not doctor_id:
        return jsonify({"message": "Doctor ID is required"}), 400

    success, message = assign_doctor_to_hospital(doctor_id, hospital_id, token)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400

def unassign_doctor(hospital_id):
    token = session.get("access_token")
    data = request.json
    doctor_id = data.get("doctor_id")

    if not doctor_id:
        return jsonify({"message": "Doctor ID is required"}), 400

    success, message = unassign_doctor_from_hospital(doctor_id, hospital_id, token)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400

def get_all_doctors_api():
    token = session.get("access_token")
    res = SuiteCRMService.get_all(DOCTOR_MODULE, token)

    if res.status_code == 200:
        return jsonify({"doctors": res.json().get("data", [])}), 200
    else:
        return jsonify({"doctors": []}), 200
