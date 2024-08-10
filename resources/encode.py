import base64

class Encode:
    def __init__(self,data) -> None:
        self.data = data
    def decode_Url(self,key):
        key_64 = self.convert_to_base64(texto=key)
        key_ascii = self.convert_to_ascii(texto=key_64)
        data = self.data
        urlAscii = data[key_ascii]
        decodeAscci = self._decodificar_ascci(texto=urlAscii)
        url64 = self._decodificar_base64(texto_base64=decodeAscci)
        return url64
    def convert_to_ascii(self,texto):
         ascii_valores = ' '.join(str(ord(c)) for c in texto)
         return ascii_valores
    def convert_to_base64(self,texto):
        bytes_texto = texto.encode('utf-8')
        base64_bytes = base64.b64encode(bytes_texto)
        base64_texto = base64_bytes.decode('utf-8')
        return base64_texto
    def _decodificar_ascci(self,texto):
        codigos = texto.split()
        caracteres = [chr(int(codigo)) for codigo in codigos]
        texto_decodificado = ''.join(caracteres)
        return texto_decodificado
    def _decodificar_base64(self,texto_base64):
        bytes_decodificados = base64.b64decode(texto_base64)
        texto = bytes_decodificados.decode('utf-8')
        return texto
        