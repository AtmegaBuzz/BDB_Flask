import json
from lib2to3.pgen2 import token
from textwrap import wrap
import uuid
import os
import jwt
import datetime

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Blueprint, make_response, jsonify, request
from marshmallow.exceptions import ValidationError
from backend.validators import register_validator
from backend.serializers import UserSchema,PersonSchema,LocationSchema
from backend.models import User,Person
from extensions import db,UPLOAD_FOLDER,SECRET_KEY

auth = Blueprint("auth",__name__)


@auth.route('/register',methods=["POST"])
def register():

    user_info = json.loads(request.form["data"])
    location = json.loads(request.form["location"])
    profile_pic = request.files["profile_photo"]


    user_serializer = UserSchema()
    person_serializer= PersonSchema()
    location_serializer = LocationSchema()

    try:
        user = user_serializer.load({
        "email":user_info.pop("email",None),
        "phone_number":user_info.pop("phone_number",None),
        "password":user_info.pop("password",None),
        "aadhar_card_number":user_info.pop("aadhar_card_number",None),
        })
        person = person_serializer.load(user_info)
        location = location_serializer.load(location)


    except ValidationError as err:
        return make_response(err.messages,400)    


    errors = register_validator(user)
    if errors!={}:
        return make_response(errors,400)

    # profile pic image save
    profile_pic_name = None
    if profile_pic.content_type!=None:
        profile_pic_file_name = secure_filename(profile_pic.filename)
        profile_pic_name = str(uuid.uuid1()) + "_" + profile_pic_file_name
        profile_pic.save(os.path.join(UPLOAD_FOLDER,profile_pic_name))
    user_password = generate_password_hash(user.pop("password"),method='sha256') 
    user = User(**user,password=user_password,profile_pic=profile_pic_name)
    db.session.add(user)

    person = Person(**person,user=user)
    db.session.add(person)

    db.session.commit()
    
    return make_response({"message":"user created"},200)


@auth.route('/login',methods=["POST"])
def login():

    creds = request.json

    if "email" not in creds or "password" not in creds:
        return make_response({"format":"invalid format passed"},400)

    user = User.query.filter_by(
            email=creds["email"]
        ).first()
    if user==None:
        return make_response({"credentials":"invalid credentials"},401,{'WWW-Authenticate':'basic realm="Login Required"'})
    else:
        if check_password_hash(user.password,creds["password"])==False:
            return make_response({"credentials":"invalid credentials"},401,{'WWW-Authenticate':'basic realm="Login Required"'})

    token = jwt.encode({
        'user':user.email,
        'expire':str(datetime.datetime.utcnow()+datetime.timedelta(hours=24))
        },SECRET_KEY)

    return jsonify({"token":token})


def get_token():
    token = request.headers["Authorization"]
    if not token:
        return make_response({"Token":"Token is missing"},401)
    try:
        data = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        return data
    except ValidationError as err:
        return make_response(jsonify(err.messages),401)

# is authenticated decorator 
def is_authenticated(func):

    @wraps(func)
    def wrapper(*args,**kwargs):

        token_data = get_token()

        if type(token_data)!=dict: 
            # failed to decode token returning 401 response
            return token_data
        
        
        return func(*args,**kwargs)

    return wrapper


def profile_permission(pk):

    token_data = get_token()
    
    if type(token_data)!=dict:
        # failed to decode token returning 401 response
        return token_data

    if User.query.filter_by(person=pk,email=token_data["user"]).first()==None:
        return make_response({"Permission":"do not have permission to view this page"},401)
    return None
