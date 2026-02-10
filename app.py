from flask import Flask ,request, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///std_data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Std(db.Model):
    name = db.Column(db.String(100))
    reg_no = db.Column(db.Integer,primary_key=True)
    department = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.name}--{self.reg_no}--{self.department}--{self.email}"

@app.route("/")
def home():
    return render_template('home.html')
@app.route("/add" , methods=["GET","POST"])
def add_std():
    if request.method=="POST":
        name=request.form["name"]
        reg_no=request.form["reg_no"]
        department=request.form["department"]
        email =request.form["email"]
        std=Std(name=name,reg_no=reg_no,department=department,email=email)
        db.session.add(std)
        db.session.commit()
        return redirect(url_for('view_std'))
    
    return render_template('add.html')
@app.route("/view")
def view_std():
    all_std= Std.query.all()
    return render_template('view.html',all_std=all_std)

@app.route("/update/<int:reg_no>",methods=["GET","POST"])
def update(reg_no):
    if request.method=="POST":
        std_upd=Std.query.filter_by(reg_no=reg_no).first()
        std_upd.name=request.form["name"]
        std_upd.reg_no=request.form["reg_no"]
        std_upd.department=request.form["department"]
        std_upd.email =request.form["email"]
        db.session.add(std_upd)
        db.session.commit()
        return redirect("/view")
    std_upd=Std.query.filter_by(reg_no=reg_no).first()
    return render_template('update.html',std_upd=std_upd)  


@app.route("/delete/<int:reg_no>")
def delete(reg_no):
    del_std = Std.query.filter_by(reg_no=reg_no).first()
    print(del_std)
    db.session.delete(del_std)
    db.session.commit()
    return redirect("/view")

if __name__=="__main__":
    app.run(debug=True)