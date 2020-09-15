from flask import Flask, render_template, request, Response, redirect
from flask_mysqldb import MySQL
import MySQLdb
import yaml
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


app = Flask(__name__)


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

def plot_data():
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM temperatures ORDER BY date ASC;")
	data = cur.fetchall()
	#mysql.connection.commit()
	a = []
	b = []
	c = []
	for row in data:
		a.append(str(row[3]))
		b.append(float(row[1]))
		c.append(float(row[2]))
	plt.plot(a,b,'-b',label='tc1')
	plt.plot(a,c,'--r',label='tc2')
	plt.legend(loc='upper right',frameon=True)
	# matplotlib.axes._axesAxes.invert_yaxis()
	plt.xlabel('time stamp', fontsize = 18)
	plt.ylabel('temperature', fontsize = 18)
	plt.xticks(rotation=90)
	plt.show()


# def create_figure(x,y):
# 	fig = Figure()
# 	axis = fig.add_subplot(1,1,1)
# 	axis.plot(x,y)



@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		t = get_data()
		return render_template('index.html', temp = t.temp1, temp1 = t.temp2)
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute(f"TRUNCATE TABLE temperatures;")
		cur.close
		return render_template('index.html', temp = "none", temp1 = "none")

@app.route('/plot')
def plot():
	plot_data()
	return redirect('/')



# @app.route('/plot.png')
# def plot_png():
# 	x,y = get_data()
# 	fig = create_figure()
# 	output = io.BtesIO()
# 	FigureCanvas(fig).print_png(output)
# 	return Response(output.getvalue(), mimetype='image/png')
		


	


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
