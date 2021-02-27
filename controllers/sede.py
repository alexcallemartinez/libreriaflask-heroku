from models.libro import LibroModel
from flask_restful import Resource,reqparse
from models.sede import SedeModel
#basico
#get all sede 
#crate sede
#vincula una sede con varioss libro y viceversa(un libro con varias sede)
serializer= reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    location='json',
    dest='latitud'
)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required=True,
    help='Falta la sede_ubicacion',
    location='json',
     dest='ubicacion'
)
serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    location='json',
    dest='longitud'
)

class SedesController(Resource):
    def post(self):
       data=serializer.parse_args()
       nuevaSede=SedeModel(data['ubicacion'],data['latitud'],data['longitud'])
       nuevaSede.save()
       return{
           'success':True,
           'content':nuevaSede.json(),
           'message':'se creo la sede exitosamente'
       }
    def  get(self):
        sedes=SedeModel.query.all()
        resultado=[]
        for sede in sedes:
            resultado.append(sede.json())
        return{
            'succes': True,
            'content':resultado,
            'message':None
        }    


class LibroSedeController(Resource):
   def get(self,id_sede):
        sede=SedeModel.query.filter_by(sedeId=id_sede).first()
        sedeLibros=sede.libros
        libros=[]
        for sedeLibro in sedeLibros:
            libro=sedeLibro.libroSede.json()
            libro['autor']=sedeLibro.libroSede.autorLibro.json()
            libro['categoria']=sedeLibro.libroSede.categoriaLibro.json()
            del libro['categoria']['categoria_id']
            del libro['autor_id']
            libros.append(libro)
           # libros.append(sedeLibro.autorLibro.json() 
        resultado=sede.json()
        resultado['libros']=libros
        return{
             'succes':True,
             'content':resultado
            
         }

class LibroCategoriaSedeController(Resource):
    def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.remove_argument('sede_longitud')
        serializer.add_argument(
        'categoria',
        type=int,
        required=True,
        help='Falta la categoria',
        location='args'
        )
        serializer.add_argument(
        'sede',
        type=int,
        required=True,
        help='Falta la sede',
         location='args'
        )
        data=serializer.parse_args()
        sede=SedeModel.query.filter_by(sedeId=data['sede']).first()
        libros=[]
        for sedeLibro in sede.libros:
            #print(sedeLibro.librosede)
            if (sedeLibro.libroSede.categoria ==  data['categoria']):
                libros.append(sedeLibro.libroSede.json())
    
        return{
          'success':True , 
          'content':libros
          }







#busqueda de todos los librps de una sede