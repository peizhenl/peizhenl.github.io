from flask import Blueprint, request, render_template, redirect, jsonify, session, url_for, current_app
from werkzeug.utils import secure_filename
from apps.models import User, UserAddress, GoodCategory, Good
from sqlalchemy.sql import func
from apps.db import db
import uuid
from datetime import datetime
import os,time
from apps.common import login_require


bp = Blueprint('common_views', __name__)

############## user module #####################
# home page
@bp.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@bp.route("/datasets.html", methods=['GET'])
def dataset_review():
    return render_template("datasets.html")

@bp.route("/model.html", methods=['GET'])
def model_review():
    return render_template("model.html")

@bp.route("/results.html", methods=['GET'])
def results_review():
    return render_template("results.html")