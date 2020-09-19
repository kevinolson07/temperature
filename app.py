from flask import Flask, render_template, request, Response, redirect, make_response, session
from flask_mysqldb import MySQL
import MySQLdb
import yaml
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


app = Flask(__name__)

app.secret_key='Keep this secret, keep this hidden'

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

#fethcing most recent values from SQL table
def get_data():	
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM temperatures ORDER BY date DESC;")
	data = cur.fetchall() 					
	x = []
	y = []
	z = []
	for row in data:
		x.append(str(row[1]))
		y.append(str(row[3]))
		z.append(str(row[2]))

	class data:
		def __init__(self):
			if not y:
				self.temp1 = "None"
				self.temp2 = "None"
			else:
				self.temp1 = x[0]
				self.temp2 = z[0]
	return data()

#fetching predefined amount of values from table
def plot_data(numSamples):
	cur = mysql.connection.cursor()
	val = str(numSamples)
	cur.execute("SELECT * FROM temperatures ORDER BY ID DESC LIMIT "+val) 
	data = cur.fetchall()
	a = []
	b = []
	c = []
	for row in data:
		a.append(str(row[3]))
		b.append(float(row[1]))
		c.append(float(row[2]))
	a.reverse()
	b.reverse()
	c.reverse()
	return a,b,c

def plot_data1(numSamples):
	cur = mysql.connection.cursor()
	val = str(numSamples)
	cur.execute("SELECT * FROM OTS_controller ORDER BY ID DESC LIMIT "+val) 
	data = cur.fetchall()
	a = []
	b = []
	c = []
	for row in data:
		a.append(str(row[4]))
		b.append(float(row[3]))
		c.append(float(row[2]))
	a.reverse()
	b.reverse()
	c.reverse()
	return a,b,c

#Home route
@app.route('/', methods=['GET','POST'])
def index():
	t = get_data()
	if request.method == "POST":
		session['numSamples'] = request.form['numSamples']
	return render_template('index.html', temp = t.temp1, temp1 = t.temp2)
	
#route used to handle plotting temperature data 
@app.route('/plot', methods=['GET','POST'])
def plot():
	numSamples = session.get('numSamples')
	print(numSamples)
	if numSamples == '':
		numSamples = 5
		print(numSamples)
	else:
		numSamples = session.get('numSamples')
	print("creating new plot with get")
	time, temp1, temp2  = plot_data(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title('Temperature VS Time')
	xs = range(int(numSamples))
	axis.plot(time, temp1,temp2)
	axis.set_ylabel('Temperature (degC)')
	fig.autofmt_xdate()
	fig.subplots_adjust (left=0.3,bottom=0.4)
	axis.set_xlabel('Timestamps (date-time)',labelpad=0)
	canvas = FigureCanvas(fig)
	axis.set_yticks([0,10,20,30,40,50,60,70])
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image.png'
	return response

#route used to handle plotting OTS_controller data 
@app.route('/plot_pwm', methods=['GET','POST'])
def plot_pwm():
	numSamples = session.get('numSamples')
	print(numSamples)
	if numSamples == '':
		numSamples = 5
		print(numSamples)
	else:
		numSamples = session.get('numSamples')
	print("creating new plot with get")
	time_stamp, temp, pwm = plot_data1(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title('Temperature VS Time')
	xs = range(int(numSamples))
	axis.plot(time_stamp, pwm)
	axis.set_ylabel('PWM')
	fig.autofmt_xdate()
	fig.subplots_adjust (left=0.3,bottom=0.4)
	axis.set_xlabel('Timestamps (date-time)',labelpad=0)
	canvas = FigureCanvas(fig)
	#axis.set_yticks([0,10,20,30,40,50,60,70])
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image.png'
	return response

		
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
