from flask import Blueprint, request, make_response
from backend.models import Person
from backend.auth import is_authenticated,profile_permission
from backend.serializers import PersonSchema

person = Blueprint("views",__name__)



@person.route('/<pk>',methods=['GET','POST'])
@is_authenticated
def person_view(pk):

    if request.method=='GET':

        perm_resp = profile_permission(pk)
        if perm_resp!=None:
            return perm_resp

        person = Person.query.filter_by(id=int(pk)).first()
        if person==None:
            return make_response({"Person":"Person does not exist"},401)

        return make_response(person.values(),200)