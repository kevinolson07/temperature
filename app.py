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
#mysql = MySQL.connect(host=db['mysql_host'], user=db['mysql_user'],passwd=db['mysql_password'], db=db['mysql_db'])

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

def get_data():
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM temperatures ORDER BY date DESC;")
	data = cur.fetchall()
	#mysql.connection.commit()
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

def plot_data(numSamples):
	cur = mysql.connection.cursor()
	val = str(numSamples)
	#print('numSamples:',type(numSamples), numSamples)
	cur.execute("SELECT * FROM temperatures ORDER BY ID DESC LIMIT "+val)
	data = cur.fetchall()
	#mysql.connection.commit()
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
	# fig = plt.figure()
	# ax = fig.add_subplot(1,1,1)
	# ax.clear()
	# ax.plot(a,b,'-b',label='tc1')
	# ax.plot(a,c,'--r',label='tc2')
	# ax.legend(loc='upper right',frameon=True)
	# # matplotlib.axes._axesAxes.invert_yaxis()
	# # ax.xlabel('time stamp', fontsize = 18)
	# # ax.ylabel('temperature', fontsize = 18)
	# ax.xticks(rotation=90)
	# plt.show()


# def create_figure(x,y):
# 	fig = Figure()
# 	axis = fig.add_subplot(1,1,1)
# 	axis.plot(x,y)



@app.route('/', methods=['GET','POST'])
def index():
	t = get_data()
	if request.method == "POST":
		session['numSamples'] = request.form['numSamples']
	return render_template('index.html', temp = t.temp1, temp1 = t.temp2)
	

@app.route('/plot', methods=['GET','POST'])
def plot():
	#numSamples = request.form['numSamples']
	# if numSamples >=1:
	# 	numSamples = numSamples
	# 	print(numSamples)
	# else:
	numSamples = session.get('numSamples')
	print(numSamples)
	if numSamples == '':
		numSamples = 5
		print(numSamples)
	else:
		numSamples = session.get('numSamples')
	print("creating new plot with get")
	time, temp1, temp2 = plot_data(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title('Temperature (degC)')
	xs = range(int(numSamples))
	plt.xticks(rotation=90)
	axis.plot(time, temp1)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image.png'
	return response
	# return redirect('/')
	# return Response(output.getvalue(), mimetype='image.png')
	




# @app.route('/plot/temp')
# def plot_temp():
	
# 	return response

		


	


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
