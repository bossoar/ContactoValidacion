from logging import debug
from os import P_DETACH
from flask import Flask
from flask import render_template,request,redirect
import pyodbc


app = Flask(__name__)


# Conectar base de datos
conn_str = (
    r'Driver={SQL Server};'
    r'Server=SRV13-VMSQL\NORPATAGONICA;'
    r'Database=Prueba;'
    r'Trusted_Connection=yes;'
    )


@app.route('/')
def index():
    
                
            conexion = pyodbc.connect(conn_str)
            cursor = conexion.cursor()
            cursor.execute("""SELECT * FROM Terminal""" )
            terminales = cursor.fetchall()
            
            conexion.commit()
            return render_template('terminal/index.html',terminales=terminales)



@app.route('/destroy/<int:numero>')
def destroy(numero):
      conexion = pyodbc.connect(conn_str)
      cursor = conexion.cursor()
      print(numero)
      cursor.execute("delete from Terminal where Numero =? ",(numero) )  
    #   cursor.execute("delete from Terminal where Numero =  " )  
      conexion.commit()
      return redirect("/")  




@app.route('/edit/<int:numero>')
def edit(numero):

      conexion = pyodbc.connect(conn_str)
      cursor = conexion.cursor()
      
      cursor.execute("select * from  Terminal where Numero =? ",(numero) ) 
      terminales = cursor.fetchall()

      conexion.commit()
      return render_template("terminal/edit.html",terminales=terminales)


@app.route('/update',methods = ['POST'])
def update():

    numero = request.form['txtNumero']
    _observaciones = request.form['txtobservaciones'] 
    conexion = pyodbc.connect(conn_str)
    cursor = conexion.cursor()
    cursor.execute("UPDATE Terminal SET observaciones = ? where numero =?",_observaciones,numero)
    conexion.commit()
    cursor.close()
    


    return redirect('/')







@app.route('/create')
def create():
    return render_template('terminal/create.html')
    
     
@app.route('/store', methods=['GET', 'POST'])
def storage():
               
                _numero = request.form['txtNumero']
                _observaciones = request.form['txtobservaciones']
              
                
                conexion = pyodbc.connect(conn_str)
                cursor = conexion.cursor()
                cursor.execute("""INSERT INTO Terminal(Numero,Observaciones) VALUES (?,?)""",_numero,_observaciones)
                conexion.commit()
                cursor.close()

                return redirect('/')







if __name__ == '__main__':
    app.run(debug=True)






