from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import model
from config.base_datos import bd
#from models.autor import AutorModel
from controllers.autor import AutoresController
from controllers.autor import AutorController
from controllers.categoria import CategoriaController
from controllers.libro import LibroController,LibroModel, RegistroLibroController
from controllers.sede import SedesController,SedeModel,LibroCategoriaSedeController
from controllers.sede import LibroSedeController
from models.categoria import CategoriaModel
from flask_cors import CORS

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL='/docs'

API_URL='/static/swagger.json'
swagger_blueprint=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Libreria Flask -  Swagger Documentacion'
    }
)
#from models.libro import LibroModel
#from models.sede import SedeModel
#from models.sedelibro import SedeLibroModel
app = Flask(__name__)
app.register_blueprint(swagger_blueprint)
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format
#                                    formato://username:password@host:port/databasename
app.config['SQLALCHEMY_DATABASE_URI']='mysql://kantmhbzt55tmdvd:t629jbir8xtmlumw@qz8si2yulh3i7gl3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/flasklibreria'
api = Api(app)
CORS(app)
#'mysql://root:root@localhost:3306/flasklibreria'
# si tu servidor no tiene contraseña, ponlo asi:
# 'mysql://root:@localhost:3306/flasklibreria'
# para evitar el warning de la funcionalidad de sqlalchemy de track modification:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# inicio la aplicacion proveyendo las credenciales indicadas en el app.config pero aun no se ha conectado a la bd
bd.init_app(app)

#bd.drop_all(app=app)
# recien se conecta a la bd, pero necesita el driver para poder conectarse
# para conectarnos a una base de datos en mysql deberemos instalar el driver: pip install mysqlclient
bd.create_all(app=app)
#rutas de mi api restfull


@app.route('/buscar')
def buscarLibro():
    print(request.args.get('palabra'))
    palabra=request.args.get('palabra')
    if palabra:
    
     ResultadoBusquedad=LibroModel.query.filter(LibroModel.libroNombre.like('%'+palabra+'%')).all()
     if ResultadoBusquedad:
         resultado=[]
         for libro in ResultadoBusquedad:
             resultado.append(libro.json())
             return{
                 'success':True,
                 'content':resultado,
                 'message':None
             }
    print(buscarLibro)
    return{
        'success':True,
        'content':None,
        'message':'no se encontro nada para buscar o la busquedad no tuvo exito'
    },400

api.add_resource(AutoresController, '/autores')
api.add_resource(AutorController,'/autor/<int:id>')
api.add_resource(CategoriaController,'/categorias','/categoria')
api.add_resource(LibroController, '/libro' , '/libros')
api.add_resource(SedesController, '/sede' , '/sedes')
api.add_resource(LibroSedeController,'/sedeLibro/<int:id_sede>')
api.add_resource(LibroCategoriaSedeController, '/busquedaLibroSedeCat')
api.add_resource(RegistroLibroController, '/registrarSedeLibro')

if __name__ == '__main__':
    app.run(debug=True)