from .os.op import Operations_Os
from .web_srap import WebScrap
from .message import Message
class After:
    def __init__(self) -> None:
        self.obj = Operations_Os()
        self.web = WebScrap()
        self.me = Message()
        pass
    def valid_reserve(self):
        print("Entra a reserva")
        self.me.show_message_op(time=3,
                                message="Revisando la base de datos de Reserva..",
                                title="Search database")
        data = self.obj.agroup_json()
        if len(data) > 0:
            
            for i in data:
                path_item = self.obj.get_path(name=i)
                item = self.obj.get_json(path=path_item)
                y,m_json = i.split('-')
                m,_ = m_json.split('.')
                #print(item)
                self.web.save_database(m=m,y=y,item=item,p=path_item,name_p=i)
                

                


