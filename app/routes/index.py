from flask import Flask,render_template,request,redirect,Blueprint
from sqlalchemy.exc import SQLAlchemyError
from app import create_app
from app.models import User

index_bp=Blueprint('index',__name__)







@index_bp.route('/',methods=["GET","POST"])
def home():
    
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
      try:
            
            v = [value for key, value in request.form.items()]
            

            if v[0]=='kilmish@gmail.com' and v[1]=="andhera":
                return redirect('/admin')
            else:
                    user=User.query.filter_by(email=v[0]).first()
                    if user is not None:
                        if user.email==v[0] and user.password==v[1]:
                            return redirect('/user')
                        else:
                            return "incorrect password"
                    else:
                         return "email is not registered"
      except SQLAlchemyError as e:
          return str(e)
      except Exception as e:
          return str(e)