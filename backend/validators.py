import phonenumbers
import re
from backend.models import User
from phonenumbers.phonenumberutil import NumberParseException


def register_validator(user):

    errors = {}
    phone_no_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


    
    if(re.fullmatch(phone_no_regex, user["email"])==False):
        errors["email"] = "invalid email"
    
    else:
        user_obj = User.query.filter_by(email=user["email"]).first()
        if user_obj:
            errors["email"] = "email already exists"     
            return errors

    if len(user["password"])<8 or len(user["password"])>16:
        errors["password"] = "password should be in between 8-16 chars"

    if len(str(user["aadhar_card_number"]))!=12:
        errors["aadhar_card_number"] = "invalid aadhar_card_number"
    
    else:
        user_obj = User.query.filter_by(aadhar_card_number=user["aadhar_card_number"]).first()
        if user_obj:
            errors["aadhar_card_number"] = "aadhar_card_number already exists"     
            return errors

    if user["phone_number"]!=None:
        try:
            phone_number = phonenumbers.parse(user["phone_number"])
            if phonenumbers.is_possible_number(phone_number)==False: 
                errors["phone_number"] = "invalid phone_number"    

        except NumberParseException:
            errors["phone_number"] = "invalid phone_number format"

    return errors


