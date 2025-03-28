from app.routes.subject import subjects_bp
from app.routes.chapter import chapter_bp
from app.routes.quiz import quiz_bp
from app.routes.question import question_bp
from app.routes.user import user_bp
from app.routes.index import index_bp
from app.routes.signup import signupbp
from app.routes.admin import admin_bp


def register_blueprints(app):
    app.register_blueprint(subjects_bp)
    app.register_blueprint(chapter_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(signupbp)
    app.register_blueprint(admin_bp)