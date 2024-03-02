from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"

# with app.app_context():
#     db.create_all()

    
@app.route("/", methods=["GET", "POST"])
def web():
    error = None
    success = "nosuccess"
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if name and email and password:
            user_info = UserInfo.query.filter_by(email=email).first()
            if user_info is None:
                user_info = UserInfo(name=name, email=email, password=password)
                db.session.add(user_info)
                db.session.commit()
                success = "Successfully Account Registered."
            else:
                error = "Email already exist."
                print(error)
    alluserinfo = UserInfo.query.all()
    return render_template("index.html", alluserinfo=alluserinfo, error=error, success=success)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    code = None
    pin_error = None
    if request.method == 'POST':
        if request.form['pin_code'] == '109238':
            code = request.form['pin_code']
        else:
            pin_error = 'INVALID PIN CODE.'
            return 'INVALID PIN CODE.'
    alluserinfo = UserInfo.query.all()
    return render_template("admin.html", alluserinfo=alluserinfo, pin_error=pin_error, code=code)


@app.route("/delete/<int:id>")
def delete(id):
    user_info = UserInfo.query.filter_by(id=id).first()
    db.session.delete(user_info)
    db.session.commit()
    return redirect("/admin")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def update(id):
    success = None
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_info = UserInfo.query.filter_by(id=id).first()
        user_info.name = name
        user_info.email = email
        user_info.password = password
        db.session.add(user_info)
        db.session.commit()
        success = "Information Successfully Updated."
        
    user_info = UserInfo.query.filter_by(id=id).first()
    return render_template('edit.html', user_info=user_info, success=success)
    

if __name__ == "__main__":
    app.run()