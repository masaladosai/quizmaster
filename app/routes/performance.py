from flask import Blueprint, render_template, session
from app.models import Marks, db

performance_bp = Blueprint('performance', __name__)

@performance_bp.route('/performance')
def performance():
    email_id = session.get('email')
    
    if not email_id:
        return "User not logged in", 403  # Ensure user is logged in

    # Fetch user marks data
    user_marks = Marks.query.filter_by(email=email_id).all()
    
    if not user_marks:
        return render_template("performance.html", 
                               user_id=email_id,  # ✅ Fixed: Use user_id instead of email_id
                               total_quizzes=0, 
                               avg_marks=0, 
                               max_marks=0, 
                               marks_data=[], 
                               labels=[], 
                               scores=[])

    # Calculate statistics
    total_quizzes = len(user_marks)
    avg_marks = round(sum(mark.marks for mark in user_marks) / total_quizzes, 2)
    max_marks = max(mark.marks for mark in user_marks)

    # Prepare data for the table and chart
    marks_data = [{"quiz_id": mark.quiz_id, "marks": mark.marks, "date": mark.date.strftime('%Y-%m-%d')} for mark in user_marks]
    
    # Chart data
    labels = [mark.date.strftime('%Y-%m-%d') for mark in user_marks]
    scores = [mark.marks for mark in user_marks]

    return render_template("performance.html", 
                           user_id=email_id,  # ✅ Fixed: `user_id` for the template
                           total_quizzes=total_quizzes, 
                           avg_marks=avg_marks, 
                           max_marks=max_marks, 
                           marks_data=marks_data, 
                           labels=labels, 
                           scores=scores)
