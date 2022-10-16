from extensions import ma
from backend.models import User,Person,Location


class UserSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = User
        fields = ("email","phone_number","aadhar_card_number","password")

    email = ma.auto_field(required=True)
    phone_number = ma.auto_field(required=False)
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



