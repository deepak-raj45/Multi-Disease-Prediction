from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
import pickle
import numpy as np

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2001'
app.config['MYSQL_DB'] = 'sys'

mysql = MySQL(app)

model = pickle.load(open('models/diabetes.pkl', 'rb'))
model1 = pickle.load(open('models/skin.pickle', 'rb'))
model2 = pickle.load(open('models/cancer.pkl', 'rb'))

def predict(values, dic):
    if len(values) == 8:
        model = pickle.load(open('models/diabetes.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 24:
        model = pickle.load(open('models/cancer.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 15:
        model = pickle.load(open('models/skin.pickle','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]

@app.route('/')
def main():
        return render_template('signin.html')


@app.route("/diabetes", methods=['GET', 'POST'])
def diabetesPage():
    return render_template('diabetes.html')

@app.route("/cancer", methods=['GET', 'POST'])
def cancerPage():
    return render_template('cancer.html')

@app.route("/skin", methods=['GET', 'POST'])
def skinPage():
    return render_template('skin.html')

@app.route("/Dresult", methods = ['POST', 'GET'])
def predictPage():
        data1 = int(request.form['Pregnancies'])
        data2 = int(request.form['Glucose'])
        data3 = int(request.form['BloodPressure'])
        data6 = float(request.form['BMI'])
        data7 = float(request.form['DiabetesPedigreeFunction'])
        data8 = int(request.form['Age'])

        arr   = np.array([[data1, data2, data3, data6, data7, data8]])
        pred  = model.predict(arr)
        return render_template('output.html', data=pred)


@app.route("/Sresult", methods = ['POST', 'GET'])
def predictskin():
        data1 = float(request.form['x'])
        data2 = float(request.form['y'])
        data3 = float(request.form['cld'])
        data6 = float(request.form['dtr'])
        data7 = float(request.form['frs'])
        data8 = float(request.form['pet'])
        data9 = float(request.form['pre'])
        data10 = float(request.form['tmn'])
        data4 = float(request.form['tmx'])
        data11 = float(request.form['tpx'])
        data12 = float(request.form['vap'])
        data13 = float(request.form['wet'])
        data14 = float(request.form['elevation'])
        data15 = float(request.form['land'])
        data16 = float(request.form['ct'])
        data17 = float(request.form['bf'])

        arr   = np.array([[data1, data2, data3, data6, data7, data8, data9, data10, data4, data11, data12, data13, data14, data15, data16, data17]])
        pred  = model1.predict(arr)
        return render_template('output.html', data=pred)


@app.route("/Cresult", methods = ['POST', 'GET'])
def predictCancer():
        data1 = float(request.form['radius_mean'])
        data2 = float(request.form['texture_mean'])
        data3 = float(request.form['perimeter_mean'])
        data4 = float(request.form['area_mean'])
        data5 = float(request.form['smoothness_mean'])
        data6 = float(request.form['compactness_mean'])
        data7 = float(request.form['concavity_mean'])
        data8 = float(request.form['concave_points_mean'])
        data9 = float(request.form['symmetry_mean'])
        data10 = float(request.form['fractal_dimension_mean'])
        data11 = float(request.form['radius_se'])
        data12 = float(request.form['texture_se'])
        data13 = float(request.form['perimeter_se'])
        data14 = float(request.form['area_se'])
        data15 = float(request.form['smoothness_se'])
        data16 = float(request.form['compactness_se'])
        data17 = float(request.form['smoothness_se'])
        data18 = float(request.form['concave_points_se'])
        data19 = float(request.form['symmetry_se'])
        data20 = float(request.form['fractal_dimension_se'])
        data21 = float(request.form['radius_worst'])
        data22 = float(request.form['texture_worst'])
        data23 = float(request.form['perimeter_worst'])
        data24 = float(request.form['area_worst'])
        data25 = float(request.form['smoothness_worst'])
        data26 = float(request.form['compactness_worst'])
        data27 = float(request.form['concavity_worst'])
        data28 = float(request.form['concave_points_worst'])
        data29 = float(request.form['symmetry_worst'])
        data30 = float(request.form['fractal_dimension_worst'])
        

        arr   = np.array([[data1, data2, data3, data4,data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23, data24, data25, data26, data27, data28, data29, data30]])
        pred  = model2.predict(arr)
        return render_template('output.html', data=pred)


@app.route('/register',methods=['POST','GET'])
def registerpage():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        datau=request.form['name']
        datae= request.form['email']
        dataph=request.form['phone']
        datap=request.form['pass']

        cur.execute('INSERT INTO login VALUES(%s,%s,%s,%s)',(datau,datae,dataph,datap))
        mysql.connection.commit()
        cur.close()
        return redirect('/diabetes')
    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        datau=request.form['your_name']
        datap=request.form['your_pass']
        cur.execute('SELECT * FROM login WHERE username=%s AND pass=%s',(datau,datap))
        mysql.connection.commit()
        s=cur.fetchall()
        cur.close()
        if len(s)==0:
            return render_template('signin.html')
        else:
            return render_template('diabetes.html')
    

if __name__ == "__main__":
    app.run(debug=True)



