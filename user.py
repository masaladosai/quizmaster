from flask import Flask,render_template,request,jsonify, session
from app.models import *
from app import create_app

app=create_app()
app.secret_key = "pizza" 

@app.route('/',methods=['POST','GET'])
def user():
    if request.method=="GET":
        sub_list=search_subject()
        return render_template("user.html",sub_list=sub_list)
    elif request.method=="POST":
        if request.form.get('action')=="start":
            q_id=request.form.get('quiz')
            ques_list=[]
    
            question=Question.query.filter_by(quizid=q_id).all()
            for ques in question:
                 ques_list.append([ques.id,ques.quizid,ques.qstatement,ques.option1,ques.option2,ques.option3,ques.option4,ques.rightoption])
            session["ques_list"] = ques_list
            return render_template('user.html',ques_list=ques_list)
        elif request.form.get('action')=='finish':
            sum=0
            answers=request.form.to_dict()
            ques_list = session.get("ques_list", [])
            for ques in ques_list:
                if str(ques[7])==answers[str(ques[0])]:
                    sum+=1
            score=sum/len(ques_list)
            
            return f"Your Score: {score * 100:.2f}%"
    else:
        return "an error occured"


@app.route('/get_chapters/<int:subject_id>')
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subjectid=subject_id).all()
    chapter_list = [{'id': c.id, 'name': c.chaptername} for c in chapters]
    return jsonify(chapter_list)


@app.route('/get_quiz/<int:chapter_id>')
def get_quiz(chapter_id):
    quizes = Quiz.query.filter_by(chapterid=chapter_id).all()
    quiz_list = [{'id': q.id, 'name': q.quizname} for q in quizes]
    return jsonify(quiz_list)

if __name__=="__main__":
    app.run(debug=True)

