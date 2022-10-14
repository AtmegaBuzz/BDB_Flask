import enum
from backend import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class UserTypeEnum(enum.Enum):
    admin = 'admin'
    organization = 'organization'
    person = 'person'

class GenderEnum(enum.Enum):
    female = 'female'
    other = 'other'
    male = 'male'

class Image(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    img = db.Column(db.Text,nullable=False)
    mimetype = db.Column(db.Text,nullable=False)
    user = db.Column(db.Integer,db.ForeignKey('user.id'))

class Location(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    line_1 = db.Column(db.String(150))
    line_2 = db.Column(db.String(150))
    city = db.Column(db.String(100),nullable=False)
    country = db.Column(db.String(50),nullable=False)
    pin_code = db.Column(db.String(16),nullable=False)
    user = db.Column(db.Integer,db.ForeignKey('user.id'))


class Person(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False) 
    last_name = db.Column(db.String(100),nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum(GenderEnum),nullable = True)
    blood_group = db.Column(db.String(4),nullable=False)
    diseases = db.Column(db.String(400))
    location = db.relationship('Location',backref="use_locationr",uselist=False)



class User(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(200),unique=True,nullable=False)
    aadhar_card_number = db.Column(db.Integer,unique=True,nullable=False) 
    password = db.Column(db.String(16),nullable=False)

    profile_pic = db.relationship('Image',backref="use_picr",uselist=False)
    location = db.relationship('Location',backref="use_locationr",uselist=False)
    

    user_type = db.Column(
            db.Enum(UserTypeEnum),
            default = UserTypeEnum.person,
            nullable = False
        )

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
