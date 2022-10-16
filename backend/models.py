import enum
from turtle import title
from extensions import db
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

class BloodTypeEnum(enum.Enum):
    a_postive = 'A+'
    a_negative = 'A-'
    b_postive = 'B+'
    b_negative = 'B-'
    o_postive = 'O+'
    o_negative = 'O-'
    ab_postive = 'AB+'
    ab_negative = 'AB-'


class Location(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    line_1 = db.Column(db.String(150))
    line_2 = db.Column(db.String(150))
    city = db.Column(db.String(100),nullable=False)
    country = db.Column(db.String(50),nullable=False)
    pin_code = db.Column(db.String(16),nullable=False)
    user = db.Column(db.Integer,db.ForeignKey('user.id'))

class DonationCamp(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    organization = db.Column(db.Integer,db.ForeignKey('organization.id'),uselist=False)
    people_attending = db.Column(db.Integer,db.ForeignKey('person.id'))
    location = db.Column(db.Integer,db.ForeignKey('location.id'),uselist=False)

class Organization(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False) 
    camps_organized = db.Column(db.Integer,default=0,nullable=False)
    user = db.relationship('User',backref="user",uselist=False)


class Person(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False) 
    last_name = db.Column(db.String(100),nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum(GenderEnum),nullable = True)
    blood_group = db.Column(db.Enum(BloodTypeEnum),nullable=False)
    camps_attended = db.Column(db.Integer,default=0,nullable=False)
    saved = db.Column(db.Integer,default=0,nullable=False)
    diseases = db.Column(db.String(400))
    user = db.relationship('User',backref="user",uselist=False)



class User(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(200),unique=True,nullable=False)
    phone_number = db.Column(db.String(16),nullable=True)
    aadhar_card_number = db.Column(db.Integer,unique=True,nullable=False) 
    password = db.Column(db.String(16),nullable=False)
    
    profile_pic = db.Column(db.String(1000),nullable=True)
    location = db.relationship('Location',backref="user_location",uselist=False)
    person = db.Column(db.Integer,db.ForeignKey('person.id'))

    user_type = db.Column(
            db.Enum(UserTypeEnum),
            default = UserTypeEnum.person,
            nullable = False
        )

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

