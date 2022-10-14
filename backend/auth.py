import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, make_response, jsonify
from marshmallow.exceptions import ValidationError
from backend.validators import UserSchema,PersonSchema,LocationSchema
from backend.models import User,Person,Image


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
        "password":user_info.pop("password",None),
        "aadhar_card_number":user_info.pop("aadhar_card_number",None),
        })

        person = person_serializer.load(user_info)
        location = location_serializer.load(location)


    except ValidationError as err:
        return make_response(jsonify(err.messages),400)    


    user_password = generate_password_hash(user.pop("password"),method='sha256') 
    user = User(**user,password=user_password)

    person = Person(**person)

    
    

    return make_response(jsonify({"da":"da"}),200)


