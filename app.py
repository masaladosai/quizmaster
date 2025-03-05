from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError 
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///quiz_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    qualification=db.Column(db.String(80),nullable=False)
    dob=db.Column(db.Date,nullable=False)
    password=db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return f'<user{self.username}>'


def database_operations():
    with app.app_context():
        db.create_all()
        print('database created')
    
def new_user(email,dob,username,qual,password):
     with app.app_context(): 

        new_user=User(email=email,dob=dob,username=username,qualification=qual,password=password)
        db.session.add(new_user)
        db.session.commit()
        print('user added:',new_user)

def search_user():
    with app.app_context():

        users=User.query.all()
        for user in users:
            print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}, Age: {user.age}')

database_operations()

@app.route('/',methods=["GET","POST"])
def home():
    
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
      try:
            
            v = [value for key, value in request.form.items()]
            

            if v[0]=='kilmish@gmail.com' and v[1]=="andhera":
                return "admin dashboard"
            else:
                    user=User.query.filter_by(email=v[0]).first()
                    if user is not None:
                        if user.email==v[0] and user.password==v[1]:
                            return "user dashboard is rendering"
                        else:
                            return "incorrect password"
                    else:
                         return "email is not registered"
      except SQLAlchemyError as e:
          return str(e)
      except Exception as e:
          return str(e)
     

            
           
           

    




@app.route('/signup',methods=["GET","POST"])
def signup():

    if request.method=="GET":
        return render_template('signup.html')
    elif request.method=="POST":
        try:
           
           v = [value for key, value in request.form.items()]
           email=User.query.filter_by(email=v[0]).first()
           if email is None:
                    dob = datetime.strptime(v[1], "%Y-%m-%d").date()
                    new_user(v[0],dob,v[2],v[3],v[4])
                    return v
           else:
               return "this email is already registered....Try another"
        except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
        except Exception as e:
            return f"an error occured:{e}"




if __name__=="__main__":
    app.run(debug=True)