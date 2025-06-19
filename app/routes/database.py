from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db
from sqlalchemy.exc import SQLAlchemyError

database_bp = Blueprint('database', __name__)

@database_bp.route('/database', methods=['GET'])
def user_database():
    users = User.query.all()
    return render_template('database.html', users=users)

@database_bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    if user_id:
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                flash('User deleted successfully', 'success')
            else:
                flash('User not found', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Database error: {str(e)}', 'danger')
    return redirect(url_for('database.user_database'))
