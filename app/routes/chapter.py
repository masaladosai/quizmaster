from flask import request,render_template,Blueprint

from app import create_app
from app.models import Subject, search_subject,Chapter,new_chapter,search_chapter,delete_chapter,db
from sqlalchemy.exc import SQLAlchemyError
chapter_bp = Blueprint('chapter', __name__)



@chapter_bp.route('/chapter',methods=['GET','POST'])
def chapter():
    if request.method=='GET':
        sub_list=search_subject()
        chap_list=search_chapter()

        return render_template('chapter.html',sub_list=sub_list,chap_list=chap_list)
    
    elif request.method=='POST':
     if request.form.get('action')=='add':
        try:
            sid=request.form.get('subjectid')
            cname=request.form.get('cname')
            cdesc=request.form.get('cdesc')
            new_chapter(sid,cname,cdesc)
            chap_list=search_chapter()
            sub_list=search_subject()

            return render_template('chapter.html',chap_list=chap_list,sub_list=sub_list)
        except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
        except Exception as e:
            return f"an error occured:{e}"
     elif request.form.get('action')=='delete':
         try:
             itemid=request.form.get('itemid')
             if itemid:
                 delete_chapter(int(itemid))
                 chap_list=search_chapter()
                 sub_list=search_subject()

                 return render_template('chapter.html',chap_list=chap_list,sub_list=sub_list)

             else:
                 return 'no item id'
         except SQLAlchemyError as e:  
                db.session.rollback()
                return f"Database error: {str(e)}"
        
         except Exception as e:
            return f"an error occured:{e}"
                 

         

        
