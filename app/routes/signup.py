from flask import Flask,render_template,request,redirect,Blueprint
from sqlalchemy.exc import SQLAlchemyError
from app import create_app
from app.models import User,new_user,search_user,db
from datetime import datetime

signupbp=Blueprint('signup',__name__)







@signupbp.route('/signup',methods=["GET","POST"])
def signup():

    if request.method=="GET":
        return render_template('signup.html')
    elif request.method=="POST":
        try:
           
           v = [value for key, value in request.form.items()]
           email=User.query.filter_by(email=v[0]).first()
           if email is None:
                    dob_date = datetime.strptime(v[1], "%Y-%m-%d").date()
                    new_user(v[0], dob_date, v[2], v[3], v[4])
                    return v
           else:
               return "this email is already registered....Try another"
        except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
        except Exception as e:
            return f"an error occured:{e}"