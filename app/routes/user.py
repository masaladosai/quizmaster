from flask import Flask,render_template,request,jsonify, session,Blueprint
from app.models import *
user_bp = Blueprint('user', __name__)


@user_bp.route('/user',methods=['POST','GET'])
def user():
    if request.method=="GET":
        sub_list=search_subject()
        return render_template("user.html",sub_list=sub_list)
    elif request.method=="POST":
        if request.form.get('action')=="start":
            q_id=request.form.get('quiz')
            session['quiz']=q_id
            ques_list=[]
    
            question=Question.query.filter_by(quizid=q_id).all()
            for ques in question:
                 ques_list.append([ques.id,ques.quizid,ques.qstatement,ques.option1,ques.option2,ques.option3,ques.option4,ques.rightoption])
            session["ques_list"] = ques_list
            return render_template('user.html',ques_list=ques_list)
        elif request.form.get('action')=='finish':
            ques_list = session.get("ques_list", [])  # Retrieve from session
            answers = request.form.to_dict()  # Get user answers
            correct_count = 0
            results = []

            for ques in ques_list:
                user_answer = answers.get(str(ques[0]), "")
                correct_answer = str(ques[7])
                is_correct = user_answer == correct_answer

                if is_correct:
                    correct_count += 1

                results.append({
                    "question": ques[2],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct
                })
            total_questions = len(ques_list)
            score = int((correct_count / total_questions) * 100)
            email=session['email']
            # Save marks using email
            add_marks(email, session.get('quiz'), score)

            total_questions = len(ques_list)
            return render_template("result.html",
                                   correct_answers=correct_count,
                                   total_questions=total_questions,
                                   results=results)
    else:
        return "an error occured"


@user_bp.route('/get_chapters/<int:subject_id>')
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subjectid=subject_id).all()
    chapter_list = [{'id': c.id, 'name': c.chaptername} for c in chapters]
    return jsonify(chapter_list)


@user_bp.route('/get_quiz/<int:chapter_id>')
def get_quiz(chapter_id):
    quizes = Quiz.query.filter_by(chapterid=chapter_id).all()
    quiz_list = [{'id': q.id, 'name': q.quizname} for q in quizes]
    return jsonify(quiz_list)
