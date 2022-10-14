from backend.models import User,Person,Location
from backend import ma


class UserSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = User
        fields = ("email","aadhar_card_number","password")

    email = ma.auto_field(required=True)
    aadhar_card_number = ma.auto_field(required=True)
    password = ma.auto_field(required=True)


class PersonSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = Person
        fields = ("first_name","last_name","dob","gender","blood_group","diseases")

    first_name = ma.auto_field(required=True)
    last_name = ma.auto_field(required=True)
    dob = ma.auto_field()
    gender = ma.auto_field()
    blood_group = ma.auto_field(required=True)
    diseases = ma.auto_field()


class LocationSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = Location
        fields = ("line_1","line_2","city","country","pin_code")

    line_1 = ma.auto_field()
    line_2 = ma.auto_field()
    city = ma.auto_field(required=True)
    country = ma.auto_field(required=True)
    pin_code = ma.auto_field(required=True)



def required_field_validator(fields,data):

    errors = {}

    for field in fields:
        if field not in data:
            errors[field] = "field is required"
        
        elif data[field]==None or data[field].strip()=="":
            errors[field] = "field is required"

        

    return errors


def register_validator(data):

    user_info = data["data"]
    location = data["location"]

    required_field_validator(["email","password","aadhar_card_number","blood_group"],user_info)
    required_field_validator(["city","country","pin_code"],location)

    # validate age 
    
        