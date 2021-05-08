from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import sys
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(application)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return 'Contact Detail ' + str(self.id)

@application.route('/')
def Main():
    return render_template('mainpage.html')
@application.route('/location')
def location():
    return render_template('location.html')
@application.route('/contactus')
def contactus():
    return render_template('contactus.html')
@application.route('/menu')
def menu():
    return render_template('menu.html')
@application.route('/catering')
def catering():
    return render_template('catering.html')
@application.route('/contactdetails',methods=['POST','GET'])
def contactdetails():
    if request.method == 'POST':
        contact_name= request.form['name']
        contact_phone = request.form['phone']
        contact_email = request.form['email']
        contact_reason=request.form['optradio']
        new_contact = Contact(name=contact_name,phone= contact_phone,email= contact_email,reason= contact_reason)
        db.session.add(new_contact)
        db.session.commit()
        return redirect('/contactdetails')
    else:
        all_posts = Contact.query.order_by(Contact.date_posted).all()
        return render_template('contactdetails.html', contacts=all_posts)

@application.route('/detail/delete/<int:id>')
def delete(id):
    post = Contact.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/contactdetails')

if __name__ == "__main__":
    application.debug=True
    application.run(host='0.0.0.0', port=80)
