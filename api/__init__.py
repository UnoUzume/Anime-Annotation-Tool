from flask import Blueprint, render_template, request, jsonify, current_app, flash, g

api = Blueprint("api", __name__, template_folder="templates")


@api.route('/')
def index():
    return "opencv api"
