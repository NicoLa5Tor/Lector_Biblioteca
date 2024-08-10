from op import Operations_Os
datos_cult = {
    "INGENIERÍA DE SISTEMAS Y COMPUTACIÓN" : 6,
    "ADMINISTRACIÓN DE EMPRESAS" : 2,
    "POSGRADOS" : 3,
    "NUEVA FACULTAD" : 10
}
obj = Operations_Os(facult=datos_cult)
data = obj.agroup_json()
print(data)