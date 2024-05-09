import sys


class Bar_code:

    def read_barcode(self):
        barcode_data = ""
        try:
            while True:
                char = sys.stdin.read(1)
                if char == '\n':
                    return barcode_data
                else:
                    barcode_data += char
        except KeyboardInterrupt:
            # Manejar la interrupción de teclado (Ctrl+C)
            return None
    def main(self):
        print("Escanea un código de barras:")
        while True:
            barcode = self.read_barcode()
            if barcode:
                print("Código de barras leído:", barcode)
                return barcode
            else:
                print("Interrupción de teclado. Saliendo...")
                return None

    

    
