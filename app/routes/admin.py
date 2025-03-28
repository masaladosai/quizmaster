from flask import Blueprint, render_template
from app import db
from app.models import User, Question, Subject,Quiz  

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin',methods=['GET','POST'])
def admin_dashboard():
    total_users = db.session.query(User).count()
    total_questions = db.session.query(Question).count()
    total_subjects = db.session.query(Subject).count()
    total_quizzes = db.session.query(Quiz).count()

    return render_template('admin.html',total_users=total_users,total_questions=total_questions,total_subjects=total_subjects,
                           total_quizzes=total_quizzes)