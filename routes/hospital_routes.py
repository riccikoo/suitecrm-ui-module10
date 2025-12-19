from flask import Blueprint, session, redirect
from controllers import hospital_controller

hospital_bp = Blueprint("hospital", __name__)

@hospital_bp.before_request
def auth_check():
    if "access_token" not in session:
        return redirect("/login")

# Hospital CRUD routes
hospital_bp.route("/hospitals")(hospital_controller.index)
hospital_bp.route("/hospital/create", methods=["GET", "POST"])(hospital_controller.create)
hospital_bp.route("/hospital/edit/<hospital_id>", methods=["GET", "POST"])(hospital_controller.edit)
hospital_bp.route("/hospital/delete/<hospital_id>", methods=["POST"])(hospital_controller.delete)

# Additional API routes related to doctors and assignments
# Pastikan fungsi-fungsi ini sudah ada di hospital_controller atau import sesuai kebutuhan
hospital_bp.route("/doctors/api", methods=["GET"])(hospital_controller.get_all_doctors_api)
hospital_bp.route("/hospital/<hospital_id>/assigned-doctors", methods=["GET"])(hospital_controller.get_assigned_doctors)
hospital_bp.route("/hospital/<hospital_id>/assign-doctor", methods=["POST"])(hospital_controller.assign_doctor)
hospital_bp.route("/hospital/<hospital_id>/unassign-doctor", methods=["POST"])(hospital_controller.unassign_doctor)
