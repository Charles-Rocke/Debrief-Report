	###################################################
	# Starting and linking Flask together with SQL
	###################################################
	#importing what we need
import os
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from PIL import Image
	# creating an instance of a flask application.
app = Flask(__name__)

	#find the directory we are currently in
dir_path = os.path.dirname(os.path.realpath(__file__))

	# Connects our Flask App to our Database
db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
	###################################################
	##################################################
	# Creating a User Table
	##################################################


class Report(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	driverName = db.Column(db.String(80))
	reason = db.Column(db.Text)
	numReturned = db.Column(db.Integer)
	pic = db.Column(db.LargeBinary)
	

	def __init__(self, driverName, reason, numReturned, pic):
		self.driverName = driverName
		self.numReturned = numReturned
		self.reason = reason
		self.pic = pic

	def __repr__(self):
		return (f"DRIVERNAME: {self.driverName}   NUMRETURNED: {self.numReturned}   REASON:{self.reason}   PIC:{self.pic}")


db.create_all()
	#####################################################


@app.route('/', methods = ['GET', 'POST'])
def form():

	return render_template('form.html')


@app.route('/admin-report', methods = ['GET', 'POST'])
def report():
	driverName = request.form.get('driverName')
	reason = request.form.get('reason')
	numReturned = request.form.get('numReturned')
	photo = request.form.get('fileImage')
	im = Image.open('image.jpg')
	pic = im.show()
	new_report = Report(driverName = driverName, reason=reason, numReturned=numReturned, pic = pic)
	db.session.add(new_report)
	db.session.commit()
	# flash('Report added!', category='success')
	reportList = Report.query.all()
	reportList.reverse()
	return render_template('report.html', reportList= reportList, pic = pic)



if __name__ == '__main__':
	db.create_all()
	app.run(debug=True,host='0.0.0.0')
