
#esta clase se hizo con el fin de no depender de apis para el consumo y el incercion de datos de mongo atlas, 
#dado que lo que se necesita es rapidez y agilidad, la api que ya he creado demora mientras el servicio inicia, lo que la hace inceficiente,
#pero no la hace no funcional
import pymongo
from .encode import Encode
from .message import Message
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, PyMongoError
import datetime


class Operations_Database:
    def __init__(self,data,facults) -> None:
        self.facult = facults
        self.object = Encode(data=data)
        self.db = self._connection_database()
        self.dataAct = datetime.date.today()
        self.me = Message()
        pass
    def update_const(self,facults):
        self.facult = facults
    def database_main(self,y=None,m = None):
        #traer el id espeifico
        #id = self.object.decode_Url(key='id_item')
        #print(f"id: {id}")
        ms = "Los datos de hoy se guardaron con éxito"
        if y  is not None and m is not None:
            year = f"concurrent_{y}"
            month = m
            ms = "Los datos de la base Reserva se guardaron exitosamente"
        else:
            year = f"concurrent_{str(self.dataAct.year)}"
            month = str(self.dataAct.month)
        item = self._getItem(item=year)
        if item:
            #concatenar lso resultados existentes
            concat = self.concat_results(item=item,month=month)
            #actualizar datos
            query = f"Value.{month}"
            update = self.update_database(item=concat,id=year,query=query)
            if update > 0:
                self.me.show_message_op(message=ms,title="Data Success")
        else:
            #si el documento no existe entonces se crea uno nuevo, estos se guardan por año
            data = {
                month : self.facult
            }
            add = self.add_item(id=year,item=data)
            if add:
                self.me.show_message_op(message=ms,title="Data Success-New Document")
        
    def add_item(self,item,id):
        try:
            data = {
                "_id": id,
                "Value" : item
            }
            additem = self.db.insert_one(data)
            return additem
        except ServerSelectionTimeoutError as sste:
           raise ServerSelectionTimeoutError('\n(ADD) Error de conexión: {}'.format(sste))
        except OperationFailure as of:
            raise OperationFailure('\n(ADD) Error en la operación: {}'.format(of))
        except PyMongoError as pme:
            raise PyMongoError('\n(ADD) Error en PyMongo: {}'.format(pme))
        except Exception as e:
            raise Exception('\n(ADD) Ocurrió un error inesperado: {}'.format(e))

    def update_database(self,item,id,query):
        try:
            result = self.db.update_one(
                {'_id' : id},
                {"$set":{query:item}},
            )
            return result.modified_count
        except ServerSelectionTimeoutError as sste:
           raise ServerSelectionTimeoutError('\n(UPDATE) Error de conexión: {}'.format(sste))
        except OperationFailure as of:
            raise OperationFailure('\n(UPDATE) Error en la operación: {}'.format(of))
        except PyMongoError as pme:
            raise PyMongoError('\n(UPDATE) Error en PyMongo: {}'.format(pme))
        except Exception as e:
            raise Exception('\n(UPDATE) Ocurrió un error inesperado: {}'.format(e))

    def concat_results(self,item,month):
        result = {}
        try:
            if 'Value' in item:
                if month in item['Value']:
                    for key,value in self.facult.items():
                        if key in item['Value'][month]:
                            item['Value'][month][key] += value
                        else:
                            item['Value'][month][key] = value
                else:
                    item['Value'][month] = self.facult
                result = item['Value'][month]
            else:
                result = self.facult
            return result
        except Exception as e:
            raise Exception("\n(CONCATENACIÓN) Excepción controlada: {}".format(e))
    
    def _getItem(self,item):
        try:
            it = self.db.find_one({"_id": item})
            return it
        except ServerSelectionTimeoutError as sste:
           raise ServerSelectionTimeoutError('\n(ITEM) Error de conexión: {}'.format(sste))
        except OperationFailure as of:
            raise OperationFailure('\n(ITEM) Error en la operación: {}'.format(of))
        except PyMongoError as pme:
            raise PyMongoError('\n(ITEM) Error en PyMongo: {}'.format(pme))
        except Exception as e:
            raise Exception('\n(ITEM) Ocurrió un error inesperado: {}'.format(e))
    def _connection_database(self):
        try:
            name_client = self.object.decode_Url(key='url_database')
            name_db = self.object.decode_Url(key='name_database')
            collection = self.object.decode_Url(key='collection')
           # print(f"La coleccion es_ {collection}")
            client = pymongo.MongoClient(name_client,serverSelectionTimeoutMS=10000)
            db = client[name_db]
            collection = db[collection]
            return collection
        except ServerSelectionTimeoutError as sste:
              raise ServerSelectionTimeoutError("\n(CLIENTE) Error TimeoutrError: {}".format(sste))
        except OperationFailure as of:
              raise OperationFailure("\n(CLIENTE) Error en la operación: {}".format(of))
        except PyMongoError as pme:
            raise PyMongoError("\n(CLIENTE) Error en PyMongo: {}".format(pme))
        except Exception as e:
            raise Exception("\n(CLIENTE) Error inesperado, controlado por Exception: {}".format(e))
    

   