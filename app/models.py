from flask_sqlalchemy import SQLAlchemy

from app import db

# ✅ Define Subject model first because Chapter depends on it
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectname = db.Column(db.String(80), nullable=False)
    subjectcode = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Subject {self.subjectname}>'


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectid = db.Column(db.Integer, db.ForeignKey('subject.id'))
    chaptername = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)

    subject = db.relationship('Subject', backref='chapters')

    def __repr__(self):
        return f'<Chapter {self.chaptername}>'


# ✅ CRUD functions for Chapter
def new_chapter(sid, cname, cdesc):
    new_chap = Chapter(subjectid=sid, chaptername=cname, description=cdesc)
    db.session.add(new_chap)
    db.session.commit()
    print('Chapter added:', new_chap)


def search_chapter():
    chapl=[]
    chaps=Chapter.query.all()
    
    for chap in chaps:
        chapl.append([chap.id,chap.subjectid,chap.chaptername,chap.description])
    return chapl


def delete_chapter(record_id):
    record = Chapter.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()


# ✅ CRUD functions for Subject
def new_subject(sname, sdesc, scode):
    new_sub = Subject(subjectname=sname, description=sdesc, subjectcode=scode)
    db.session.add(new_sub)
    db.session.commit()
    print('Subject added:', new_sub)


def search_subject():
    subl=[]
    
    subs=Subject.query.all()
    for sub in subs:
        subl.append([sub.id,sub.subjectname,sub.subjectcode,sub.description])
    return subl




def delete_subject(record_id):
    record = Subject.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapterid = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    quizname = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)

    chapter = db.relationship('Chapter', backref='quiz')

    def __repr__(self):
        return f'<quiz {self.quizname}>'
    
def new_quiz(cid,qname,qdesc):
    new_quiz = Quiz(chapterid=cid,quizname=qname,description=qdesc)
    db.session.add(new_quiz)
    db.session.commit()
    print('Quiz added:', new_quiz)


def search_quiz():
    qlist=[]
    
    quiz=Quiz.query.all()
    for q in quiz:
        qlist.append([q.id,q.chapterid,q.quizname,q.description])
    return qlist




def delete_quiz(record_id):
    record = Quiz.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quizid = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    qstatement = db.Column(db.String(180), nullable=False)
    option1 = db.Column(db.String(80), nullable=False)
    option2 = db.Column(db.String(80), nullable=False)
    option3 = db.Column(db.String(80), nullable=False)
    option4 = db.Column(db.String(80), nullable=False)
    rightoption = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref='Question')

    def __repr__(self):
        return f'<question {self.qstatement}>'
    
def new_question(quizid,qstatement,op1,op2,op3,op4,rop):
    new_ques = Question(quizid=quizid,qstatement=qstatement,option1=op1,option2=op2,option3=op3,option4=op4,rightoption=rop)
    db.session.add(new_ques)
    db.session.commit()
    print('Question added:', new_ques)


def search_question():
    queslist=[]
    
    question=Question.query.all()
    for ques in question:
        queslist.append([ques.id,ques.quizid,ques.qstatement,ques.option1,ques.option2,ques.option3,ques.option4,ques.rightoption])
    return queslist




def delete_question(record_id):
    record = Question.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()





class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    qualification=db.Column(db.String(80),nullable=False)
    dob=db.Column(db.Date,nullable=False)
    password=db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return f'<user{self.username}>'


    
def new_user(email,dob,username,qual,password):

        new_user=User(email=email,dob=dob,username=username,qualification=qual,password=password)
        db.session.add(new_user)
        db.session.commit()
        print('user added:',new_user)

def search_user():

        users=User.query.all()
        for user in users:
            print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}, Age: {user.age}')
