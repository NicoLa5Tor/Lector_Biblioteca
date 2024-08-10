import os

def obtener_ruta_documentos():
    # Obtener la ruta a la carpeta "Documentos" del usuario
    ruta_documentos = os.path.join(os.path.expanduser('~'), 'Documents')
    carpeta_nueva = os.path.join(ruta_documentos, 'reserve_db')
    if not os.path.exists(carpeta_nueva):
        os.makedirs(carpeta_nueva)
        print(f"Se creó la carpeta '{carpeta_nueva}'")
    else:
        print(f"La carpeta '{carpeta_nueva}' ya existe")

    return carpeta_nueva

# Ejemplo de uso
ruta_documentos = obtener_ruta_documentos()
print(f"La ruta a la carpeta 'Documentos' es: {ruta_documentos}")
