from flask import Blueprint, request
from controllers.user_controller import login, logout, dashboard

user_bp = Blueprint("user", __name__)

user_bp.route("/login", methods=["GET", "POST"])(login)
user_bp.route("/logout")(logout)
user_bp.route("/", methods=["GET"])(dashboard)