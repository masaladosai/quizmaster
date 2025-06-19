from flask import redirect,render_template
from app import create_app

app = create_app()

@app.route('/')
def home():
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)