from flask import Blueprint
from controllers import doctor_controller

doctor_bp = Blueprint("doctor", __name__)

doctor_bp.route("/doctors")(doctor_controller.index)
doctor_bp.route("/doctor/create", methods=["GET", "POST"])(doctor_controller.create)
doctor_bp.route("/doctor/edit/<doctor_id>", methods=["GET", "POST"])(doctor_controller.edit)
doctor_bp.route("/doctor/delete/<doctor_id>", methods=["POST"])(doctor_controller.delete)
