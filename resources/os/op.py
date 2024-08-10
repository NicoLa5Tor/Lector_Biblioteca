import os,json,sys
import datetime
class Operations_Os:
    def __init__(self) -> None:
        #self.folder = os.path.join(os.getcwd(),'reserve_db')
        self.folder = self._path_reserve()
        self.actual_date = datetime.date.today()        
        pass
    def _path_reserve(self):
        path_documents = os.path.join(os.path.expanduser('~'), 'Documents')
        reserve = os.path.join(path_documents, 'reserve_db')
        if not os.path.exists(reserve):
            os.makedirs(reserve)
            print(f"Se creó la carpeta '{reserve}'")
        else:
            print(f"La carpeta '{reserve}' ya existe")

        return reserve
    def main_operations(self,facult_today):
        try:
            today = f"{str(self.actual_date.year)}-{str(self.actual_date.month)}.json"
            data_path =  self.get_path(name=today)
            item = facult_today
            operation = "Create"
            if os.path.exists(data_path):
                data_json = self.get_json(path=data_path)
                item = self.concat_items_reserve(item_json=data_json,today=facult_today)
                operation = "Update"
            self._create_update_json(item=item,path=data_path)
            return operation
        except Exception as e:
            print(f"Error {e}")
            return False
    def get_path(self,name):
        data_path = os.path.join(self.folder,name)
        return data_path

    def _create_update_json(self,item,path):
        try:
            data = {
                "Value" : item
            }
            with open(path,'w',encoding='utf-8') as dt:
                json.dump(data,dt,indent=2,ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error en el update {e}")

    def get_json(self,path):
        with open(path,'r',encoding='utf-8') as dt:
            data = json.load(dt)
        return data['Value']
    def concat_items_reserve(self,item_json,today):
        for key,value in today.items():
            if key in item_json:
                item_json[key] += value
            else:
                item_json[key] = value
        return item_json
    def  agroup_json(self):
            list_json = [arch for arch in os.listdir(self.folder) if arch.endswith(".json")]
            return list_json  
    def config(self):
        config = self.get_resource_path('config.json')
        print(config)
        with open(config,'r') as data:
            dat = json.load(data)
        return dat
    def get_resource_path(self,relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)





        
    

