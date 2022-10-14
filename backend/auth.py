import json
import uuid
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Blueprint, request, make_response, jsonify
from marshmallow.exceptions import ValidationError
from backend.validators import UserSchema,PersonSchema,LocationSchema,register_validator
from backend.models import User,Person
from backend import db,UPLOAD_FOLDER

auth = Blueprint("auth",__name__)


# @auth.route('/login',methods=["POST"])
# def login():

@auth.route('/register',methods=["POST"])
def register():

    user_info = json.loads(request.form["data"])
    location = json.loads(request.form["location"])
    profile_pic = request.files["profile_photo"]

    # print(type(location))

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
        return make_response(jsonify(err.messages),400)    


    errors = register_validator(user)
    if errors!={}:
        return make_response(jsonify(errors),400)

    # profile pic image save
    profile_pic_file_name = secure_filename(profile_pic.filename)
    profile_pic_name = str(uuid.uuid1()) + "_" + profile_pic_file_name
    profile_pic.save(os.path.join(UPLOAD_FOLDER,profile_pic_name))

    user_password = generate_password_hash(user.pop("password"),method='sha256') 
    user = User(**user,password=user_password,profile_pic=profile_pic_name)
    db.session.add(user)

    person = Person(**person,user=user)
    db.session.add(person)
    
    db.session.commit()
    
    

    return make_response(jsonify({"da":"da"}),200)


