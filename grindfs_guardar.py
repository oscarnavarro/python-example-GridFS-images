# -*- coding: utf-8 -*-
import cStringIO
import gridfs
from pymongo import MongoClient
from bson.objectid import ObjectId
from configuracion import SERVIDOR
from PIL import Image

URI = 'mongodb://{}:{}@{}:{}/{}'.format(SERVIDOR['USUARIO'],
                                        SERVIDOR['PASSWORD'], SERVIDOR['HOST'],
                                        SERVIDOR['PORT'], SERVIDOR['NOMBRE_DB'])


try:
    conexion = MongoClient(URI)
except:
    conexion = MongoClient('mongodb://localhost:27017')

try:
    db = conexion.get_default_database()
except:
    db = conexion.test


class FotosGridfs:

    def __init__(self, coleccion):
        self.__coleccion = coleccion
        self.grid = gridfs.GridFS(db, self.__coleccion)

    def consultar(self, pk):
        foto = self.grid.exists({"_id": ObjectId(pk)})
        foto = self.grid.get(ObjectId(pk))

        stream = cStringIO.StringIO(foto.read())
        img = Image.open(stream)
        return img.show()

    def guardar(self, archivo):
        with open(archivo, 'rb') as archivos:
            _id = self.grid.put(archivos)

        print('el id es: {}'.format(_id))

    def borrar(self, pk):
        self.grid.delete(ObjectId(pk))

    def listar(self):
        lista = self.grid.find({})
        for lis in lista:
            print("Id Imagen:{}, fecha: {}".format(lis._id, lis.uploadDate))
