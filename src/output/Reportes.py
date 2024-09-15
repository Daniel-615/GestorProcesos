import os
from dotenv import load_dotenv
from docx2pdf import convert
from PIL import Image
from PyPDF2 import PdfMerger

load_dotenv()

class Reportes:
    def __init__(self):
        pass
    def infLog(self,gestor,message):
        log=gestor.getLog()
        log.log_info(message)
    def warnLog(self,gestor,message):
        log=gestor.getLog()
        log.log_warning(message)
    def errLog(self,gestor,message):
        log=gestor.getLog()
        log.log_error(message)
    def convertir_docx_a_pdf(self, file,gestor):
        """Convierte un archivo DOCX a PDF usando docx2pdf."""
        ruta_pdf = os.getenv('REPORTS_PATH_PDF')

        if ruta_pdf is None:
            message="La ruta del directorio PDF no está definida en las variables de entorno."
            self.warnLog(gestor,message)
            return None

        input_file = file
        output_file = os.path.join(ruta_pdf, f"{os.path.splitext(os.path.basename(file))[0]}.pdf")

        if not os.path.exists(file):
            message=f"El archivo {file} no existe."
            self.warnLog(gestor,message)
            return None

        try:
            convert(input_file, output_file)
            # Remover archivo docx
            os.remove(input_file)
            message=f"Archivo convertido a PDF: {output_file}"
            self.infLog(gestor,message)

            return output_file
        except Exception as e:
            message=f"Error al convertir el archivo a PDF: {e}"
            self.errLog(gestor,message)
            
            return None

    def convertir_imagenes_a_pdf(self, output_pdf,gestor):
        """Convierte todas las imágenes en un directorio a un único archivo PDF y lo concatena si ya existe."""
        DIRECTORIO_IMAGENES = os.getenv('REPORTS_PATH_IMG')
        RUTA_SALIDA_PDF = os.getenv('REPORTS_PATH_PDF')

        if not os.path.exists(DIRECTORIO_IMAGENES):
            message=f"El directorio de imágenes {DIRECTORIO_IMAGENES} no existe."
            self.warnLog(gestor,message)
            return None

        if not os.path.exists(RUTA_SALIDA_PDF):
            message=f"El directorio de salida {RUTA_SALIDA_PDF} no existe."
            self.warnLog(gestor,message)
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
                    rutas_imagenes.append(file_path)
                except Exception as e:
                    message=f"Error al abrir la imagen {file_path}: {e}"
                    self.errLog(gestor,message)

        if not imagenes:
            message="No se encontraron imágenes válidas para convertir."
            self.warnLog(message)
            return None

        nuevo_pdf_path = os.path.join(RUTA_SALIDA_PDF, f"{output_pdf}_temp.pdf")

        try:
            # Guardar el nuevo PDF a partir de las imágenes
            imagenes[0].save(nuevo_pdf_path, save_all=True, append_images=imagenes[1:])
            message=f"Imagenes convertidas y guardadas en: {nuevo_pdf_path}"
            self.infLog(gestor,message)

            archivo_pdf_existente = os.path.join(RUTA_SALIDA_PDF, f"{output_pdf}.pdf")
            if os.path.exists(archivo_pdf_existente):
                # Crear un archivo temporal para el merge
                pdf_temporal = os.path.join(RUTA_SALIDA_PDF, f"{output_pdf}_merged.pdf")
                merger = PdfMerger()

                # Agregar el PDF existente y el nuevo
                merger.append(archivo_pdf_existente)
                merger.append(nuevo_pdf_path)

                # Escribir el archivo mergeado en un nuevo archivo temporal
                with open(pdf_temporal, 'wb') as salida:
                    merger.write(salida)

                merger.close()

                # Reemplazar el archivo original con el archivo mergeado
                os.remove(archivo_pdf_existente)
                os.rename(pdf_temporal, archivo_pdf_existente)
                message=f"Archivos concatenados y guardados en: {archivo_pdf_existente}"
                self.infLog(gestor,message)

            else:
                # Si no existe el PDF previo, simplemente renombrar el nuevo archivo
                os.rename(nuevo_pdf_path, archivo_pdf_existente)
                message=f"Nuevo PDF guardado en: {archivo_pdf_existente}"
                self.infLog(gestor,message)

            # Eliminar imágenes
            for file_path in rutas_imagenes:
                try:
                    os.remove(file_path)
                except Exception as e:
                    message=f"Error al eliminar la imagen {file_path}: {e}"
                    self.errLog(gestor,message)

            return archivo_pdf_existente
        except Exception as e:
            message=f"Error al convertir imágenes a PDF: {e}"
            self.errLog(gestor,message)
            return None