import os
from dotenv import load_dotenv
from docx2pdf import convert
from PIL import Image
from PyPDF2 import PdfMerger

load_dotenv()

class Reportes:
    def __init__(self):
        pass

    def convertir_docx_a_pdf(self, file):
        """Convierte un archivo DOCX a PDF usando docx2pdf."""
        ruta_pdf = os.getenv('REPORTS_PATH_PDF')

        if ruta_pdf is None:
            print("La ruta del directorio PDF no está definida en las variables de entorno.")
            return None

        input_file = file
        output_file = os.path.join(ruta_pdf, f"{os.path.splitext(os.path.basename(file))[0]}.pdf")

        if not os.path.exists(file):
            print(f"El archivo {file} no existe.")
            return None

        try:
            convert(input_file, output_file)
            # Remover archivo docx
            os.remove(input_file)
            print(f"Archivo convertido a PDF: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error al convertir el archivo a PDF: {e}")
            return None

    def convertir_imagenes_a_pdf(self, output_pdf):
        """Convierte todas las imágenes en un directorio a un único archivo PDF y lo concatena si ya existe."""
        DIRECTORIO_IMAGENES = os.getenv('REPORTS_PATH_IMG')
        RUTA_SALIDA_PDF = os.getenv('REPORTS_PATH_PDF')

        if not os.path.exists(DIRECTORIO_IMAGENES):
            print(f"El directorio de imágenes {DIRECTORIO_IMAGENES} no existe.")
            return None

        if not os.path.exists(RUTA_SALIDA_PDF):
            print(f"El directorio de salida {RUTA_SALIDA_PDF} no existe.")
            return None

        archivos = os.listdir(DIRECTORIO_IMAGENES)
        imagenes = []
        rutas_imagenes = []

        # Filtrar solo archivos de imagen
        for archivo in archivos:
            file_path = os.path.join(DIRECTORIO_IMAGENES, archivo)
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    img = Image.open(file_path)
                    img = img.convert('RGB')  # Asegurarse de que esté en modo RGB para PDF
                    imagenes.append(img)
                    rutas_imagenes.append(file_path)  # Agregar la ruta de la imagen para eliminarla después
                except Exception as e:
                    print(f"Error al abrir la imagen {file_path}: {e}")

        if not imagenes:
            print("No se encontraron imágenes válidas para convertir.")
            return None

        nuevo_pdf_path = os.path.join(RUTA_SALIDA_PDF, f"{output_pdf}_nuevo.pdf")

        try:
            # Guardar el nuevo PDF a partir de las imágenes
            imagenes[0].save(nuevo_pdf_path, save_all=True, append_images=imagenes[1:])
            print(f"Imágenes convertidas y guardadas en: {nuevo_pdf_path}")

            # Concatenar con el PDF existente si ya existe
            archivo_pdf_existente = os.path.join(RUTA_SALIDA_PDF, f"{output_pdf}.pdf")
            if os.path.exists(archivo_pdf_existente):
                merger = PdfMerger()
                merger.append(archivo_pdf_existente)
                merger.append(nuevo_pdf_path)

                output_pdf_path = os.path.join(RUTA_SALIDA_PDF, f"{output_pdf}.pdf")
                with open(output_pdf_path, 'wb') as salida:
                    merger.write(salida)
                merger.close()

                # Eliminar el PDF nuevo
                os.remove(nuevo_pdf_path)
                print(f"Archivos concatenados y guardados en: {output_pdf_path}")
            else:
                # Renombrar el nuevo PDF si no existe previamente
                os.rename(nuevo_pdf_path, archivo_pdf_existente)
                print(f"Nuevo PDF guardado en: {archivo_pdf_existente}")

            # Eliminar imágenes
            for file_path in rutas_imagenes:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error al eliminar la imagen {file_path}: {e}")

            return archivo_pdf_existente
        except Exception as e:
            print(f"Error al convertir imágenes a PDF: {e}")
            return None
