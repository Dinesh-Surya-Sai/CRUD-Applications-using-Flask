import os
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate





app = Flask(__name__)
app.secret_key = "Secret Key"

################Database Configuration######################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

class Data(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    course = db.Column(db.String(100))
    batch_num = db.Column(db.String(100))


    def __init__(self,name,email,phone,course,batch_num):
        self.name=name
        self.email = email
        self.phone = phone
        self.course = course
        self.batch_num= batch_num







@app.route("/")

def Index():

    all_data = Data.query.all()

    return render_template('index.html',student = all_data)



@app.route('/insert',methods= ['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        batch_num = request.form['batch_num']


        my_data=Data(name,email,phone,course,batch_num)
        db.session.add(my_data)
        db.session.commit()
        flash('Student Inserted Successfully')
        return redirect(url_for('Index'))

@app.route('/update',methods = ['GET','POST'])

def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.course = request.form['course']
        my_data.batch_num = request.form['batch_num']

        db.session.commit()
        flash('Student Updated Successfully')
        return redirect(url_for('Index'))


@app.route('/delete/<id>/',methods = ['GET','POST'])
def delete(id):

    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Student Deleted Successfully')

    return redirect(url_for('Index'))





if __name__=="__main__":
    app.run(debug = True)
