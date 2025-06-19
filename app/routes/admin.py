from flask import Blueprint, render_template
from app import db
from app.models import User, Question, Subject,Quiz,Marks
from sqlalchemy import func 

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin',methods=['GET','POST'])
def admin_dashboard():
    registrations = (
        db.session.query(User.date_registered, func.count(User.id))
        .group_by(User.date_registered)
        .order_by(User.date_registered)
        .all()
    )

    labels = [reg[0].strftime('%Y-%m-%d') for reg in registrations]
    data = [reg[1] for reg in registrations]

    # Query top 5 most attempted quizzes
    top_quizzes = (
        db.session.query(Marks.quiz_id, Quiz.quizname, func.count(Marks.quiz_id))
        .join(Quiz, Marks.quiz_id == Quiz.id)
        .group_by(Marks.quiz_id, Quiz.quizname)
        .order_by(func.count(Marks.quiz_id).desc())
        .limit(5)
        .all()
    )

    # Prepare pie chart data
    pie_labels = [quiz[1] for quiz in top_quizzes]  # Quiz names
    pie_data = [quiz[2] for quiz in top_quizzes] 

    # Prepare labels (dates) and data (count of users)
    labels = [reg[0].strftime('%Y-%m-%d') for reg in registrations]
    data = [reg[1] for reg in registrations]
    total_users = db.session.query(User).count()
    total_questions = db.session.query(Question).count()
    total_subjects = db.session.query(Subject).count()
    total_quizzes = db.session.query(Quiz).count()

    return render_template('admin.html',total_users=total_users,total_questions=total_questions,total_subjects=total_subjects,
                           total_quizzes=total_quizzes,labels=labels,data=data,pie_labels=pie_labels,pie_data=pie_data)