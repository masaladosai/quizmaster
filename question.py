from flask import request,render_template

from app import create_app
from app.models import Quiz, search_quiz,Question,new_question,search_question,delete_question,db
from sqlalchemy.exc import SQLAlchemyError
app = create_app()



@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET':
        quiz_list=search_quiz()
        ques_list=search_question()

        return render_template('question.html',quiz_list=quiz_list,ques_list=ques_list)
    
    elif request.method=='POST':
     if request.form.get('action')=='add':
        try:
            quizid=request.form.get('quizid')
            questionstm=request.form.get('qstat')
            qopt1=request.form.get('qopt1')
            qopt2=request.form.get('qopt2')
            qopt3=request.form.get('qopt3')
            qopt4=request.form.get('qopt4')
            ropt=request.form.get('rop')
            new_question(quizid,questionstm,qopt1,qopt2,qopt3,qopt4,ropt)
            ques_list=search_question()
            quiz_list=search_quiz()

            return render_template('question.html',ques_list=ques_list,quiz_list=quiz_list)
        except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
        except Exception as e:
            return f"an error occured:{e}"
     elif request.form.get('action')=='delete':
         try:
             itemid=request.form.get('itemid')
             if itemid:
                 delete_question(int(itemid))
                 quiz_list=search_quiz()
                 ques_list=search_question()

                 return render_template('question.html',quiz_list=quiz_list,ques_list=ques_list)

             else:
                 return 'no item id'
         except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
         except Exception as e:
            return f"an error occured:{e}"
                 

         

        

if __name__=="__main__":
    app.run(debug=True)
