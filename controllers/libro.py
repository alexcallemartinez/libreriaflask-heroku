from flask_restful  import Resource, reqparse
from models.libro import LibroModel
from models.sedelibro import SedeLibroModel

serializer = reqparse.RequestParser()
serializer.add_argument(
    'libro_nombre',
    type=str,
    required=True,
    help='Falta el libro_nombre',
    location='json'
)
serializer.add_argument(
    'libro_cant',
    type=int,
    required=True,
    help='Falta el libro_cant',
    location='json'
)
serializer.add_argument(
    'libro_edicion',
    type=str,
    required=True,
    help='Falta el libro_edicion',
    location='json'
)
serializer.add_argument(
    'autor_id',
    type=int,
    required=True,
    help='Falta el autor_id',
    location='json'
)
serializer.add_argument(
    'categoria_id',
    type=int,
    required=True,
    help='Falta el categoria_id',
    location='json'
)

class LibroController(Resource):
    def post(self):
       data= serializer.parse_args()
       nuevoLibro=LibroModel(data['libro_nombre'],data['libro_cant'],data['libro_edicion'], data['autor_id'], data['categoria_id'])
       nuevoLibro.save()
       return {
           'success':True,
           'content':nuevoLibro.json(),
           'message':'Se creo el libro exitosamente'
       },201

    def get(self):
        libros=LibroModel.query.all()
        resultado=[]
        for libro in libros:
            resultadoTemporal=libro.json()
            resultadoTemporal['autor']=libro.autorLibro.json() 
            resultadoTemporal['categoria']=libro.categoriaLibro.json()
            del resultadoTemporal['autor_id']
            del resultadoTemporal['categoria_id']
            resultado.append(resultadoTemporal)
            return {
                'succes':True,
            'content':resultado,
            'message':None
            },      


class RegistroLibroController(Resource):
    def post(self):
        serializerPost=reqparse.RequestParser(bundle_errors=True)
        serializerPost.add_argument(
            'libro_id',
            type=int,
            required=True,
            help='Falta el libro_id',
            location='json'
        )
        serializerPost.add_argument(
            'sedes',
            type=list,
            required=True,
            help='Falta las sedes',
            location='json'
        )

        data= serializerPost.parse_args()
        try:
            
        #print(data)
             for  sede  in data['sedes']:
              SedeLibroModel(sede['sede_id'],data['libro_id']).save()
              return{
              'success':True,
               'content':None,
               'message':'se vinculo correctamente el libro con las sedes'
             },201
        except:
          return{
             'success':False,
             'content':None,
             'message':'Error al registrar los libros con lassedes, vuelva a intentarlo nuevamente'
             },500