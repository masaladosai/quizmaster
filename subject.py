from flask import request,render_template

from app import create_app
from app.models import Subject, new_subject, search_subject,delete_subject,db
from sqlalchemy.exc import SQLAlchemyError
app = create_app()


@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET':
        sub_list=search_subject()

        return render_template('add.html',sub_list=sub_list)
    
    elif request.method=='POST':
     if request.form.get('action')=='add':
        try:
            sname=request.form.get('subject')
            scode=request.form.get('scode')
            sdesc=request.form.get('sdesc')
            new_subject(sname,sdesc,scode)
            sub_list=search_subject()

            return render_template('add.html',sub_list=sub_list)
        except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
        except Exception as e:
            return f"an error occured:{e}"
     elif request.form.get('action')=='delete':
         try:
             itemid=request.form.get('itemid')
             if itemid:
                 delete_subject(int(itemid))
                 sub_list=search_subject()

                 return render_template('add.html',sub_list=sub_list)

             else:
                 return 'no item id'
         except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
         except Exception as e:
            return f"an error occured:{e}"
                 

         

        

if __name__=="__main__":
    app.run(debug=True)