
import os
from flask import Flask
from flask import render_template,request,redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory


app=Flask(__name__)
app.secret_key="develoteca"
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def ima(imagen):
     print(imagen)
     return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route("/css/<archivocss>")
def css_link(archivocss):
     return send_from_directory(os.path.join('templates/sitio/css'),archivocss)


app.route('/video/<videos>')
def vid(video):
     print(video)
     return send_from_directory(os.path.join('templates/sitio/video'),video)

@app.route('/libro')
def libro():
     conexion=mysql.connect()
     cursor= conexion.cursor()
     cursor.execute("SELECT * FROM `libro`")
     libros=cursor.fetchall()
     conexion.commit() 
     print(libros)
     return render_template('sitio/libro.html',libro=libros)

@app.route('/integrantes')
def integrantes():
     return render_template('sitio/integrantes.html')

@app.route('/admin/')
def admin_index():
     if not 'login' in session:
          return redirect("/admin/login")
     return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
     return render_template('admin/login.html')

@app.route('/admin/login',methods=['POST'])
def admin_login_post():
     _usuario=request.form['txtUsuario']
     _password=request.form['txtPassword']
     print(_usuario)
     print(_password)

     if _usuario=="admin" and _password=="123":
          session["login"]=True
          session["usuario"]="Administrador"
          return redirect("/admin")

     return render_template("admin/login.html")

@app.route('/admin/cerrar')
def admin_login_cerrar():
     session.clear()
     return redirect('/admin/login')

@app.route('/admin/libro')
def admin_libro():
     if not 'login' in session:
          return redirect("/admin/login")

     conexion=mysql.connect()
     cursor= conexion.cursor()
     cursor.execute("SELECT * FROM `libro`")
     libros=cursor.fetchall()
     conexion.commit() 
     print(libros)
     return render_template('admin/libro.html',libro=libros)

@app.route('/admin/libro/guardar',methods=['POST'])
def admin_libro_guardar():
     if not 'login' in session:
          return redirect("/admin/login")
     _nombre=request.form['txtNombre']
     _url=request.form['txtURL']
     _archivo=request.files['txtImagen']

     tiempo= datetime.now()
     horaActual=tiempo.strftime('%Y%H%M%S')

     if _archivo.filename!="":
          nuevoNombre=horaActual+"_"+_archivo.filename
          _archivo.save("templates/sitio/img/"+nuevoNombre)


     sql="INSERT INTO `libro` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
     datos=(_nombre,nuevoNombre,_url)

     conexion=mysql.connect()
     Cursor=conexion.cursor()
     Cursor.execute(sql,datos)
     conexion.commit()


     print(_nombre)
     print(_url)
     print(_archivo)

     print(request.form['txtNombre'])

     return redirect('/admin/libro')
@app.route('/admin/libros/borrar',methods=['POST'])
def admin_libro_borrar():
     if not 'login' in session:
          return redirect("/admin/login")
     _id=request.form['txtID']
     print(_id)

     conexion=mysql.connect()
     cursor= conexion.cursor()
     cursor.execute("SELECT imagen FROM `libro`WHERE id=%s",(_id))
     libro=cursor.fetchall()
     conexion.commit() 
     print(libro)

     if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
          os.unlink("templates/sitio/img/"+str(libro[0][0]))

     conexion=mysql.connect()
     cursor= conexion.cursor()
     cursor.execute("DELETE FROM `libro`WHERE id=%s",(_id))
     conexion.commit()


     return redirect('/admin/libro')



