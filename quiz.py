from flask import request,render_template

from app import create_app
from app.models import Quiz, search_quiz,Chapter,new_quiz,search_chapter,delete_chapter,db,delete_quiz
from sqlalchemy.exc import SQLAlchemyError
app = create_app()



@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET':
        quiz_list=search_quiz()
        chap_list=search_chapter()

        return render_template('quiz.html',quiz_list=quiz_list,chap_list=chap_list)
    
    elif request.method=='POST':
     if request.form.get('action')=='add':
        try:
            cid=request.form.get('chapid')
            qname=request.form.get('qname')
            qdesc=request.form.get('qdesc')
            new_quiz(cid,qname,qdesc)
            chap_list=search_chapter()
            quiz_list=search_quiz()

            return render_template('quiz.html',chap_list=chap_list,quiz_list=quiz_list)
        except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
        except Exception as e:
            return f"an error occured:{e}"
     elif request.form.get('action')=='delete':
         try:
             itemid=request.form.get('itemid')
             if itemid:
                 delete_quiz(int(itemid))
                 quiz_list=search_quiz()
                 chap_list=search_chapter()

                 return render_template('quiz.html',quiz_list=quiz_list,chap_list=chap_list)

             else:
                 return 'no item id'
         except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
         except Exception as e:
            return f"an error occured:{e}"
                 

         

        

if __name__=="__main__":
    app.run(debug=True)
