	###################################################
	# Starting and linking Flask together with SQL
	###################################################
	#importing what we need
import os
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

	# creating an instance of a flask application.
app = Flask(__name__)

	#find the directory we are currently in
dir_path = os.path.dirname(os.path.realpath(__file__))

	# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir_path,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdfghjkl'
	#starts our data base
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

		def __init__(self, driverName, reason, numReturned):
			self.driverName = driverName
			self.numReturned = numReturned
			self.reason = reason

		def __repr__(self):
			return (f"DRIVERNAME: {self.driverName}   NUMRETURNED: {self.numReturned}   REASON:{self.reason}")


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
	new_report = Report(driverName = driverName, reason=reason, numReturned=numReturned)
	db.session.add(new_report)
	db.session.commit()
	# flash('Report added!', category='success')
	reportList = Report.query.all()
	reportList.reverse()
	return render_template('report.html', reportList= reportList)



if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
