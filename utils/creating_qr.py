import qrcode

def generate_qr(qr_text, output_file="qr_code.png"):
    """
    Genera un código QR a partir del texto proporcionado y lo guarda como imagen.

    :param qr_text: Texto o URL que se quiere convertir en QR.
    :param output_file: Nombre del archivo de salida.
    """
    qr = qrcode.QRCode(
        version=1,  # Controla el tamaño del QR (1 es el más pequeño)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
        box_size=10,  # Tamaño de cada caja del QR
        border=4,  # Tamaño del borde blanco
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(output_file)

    print(f"✅ Código QR generado y guardado en: {output_file}")

# Ejemplo de uso:
if __name__ == "__main__":
    qr_content = input("🔹 Introduce el texto o URL para generar el QR: ")
    generate_qr(qr_content)
