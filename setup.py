import os
import subprocess
import pysubs2
from ftplib import FTP

def download_files(ftp_connection, remote_directory, local_directory):
    """
    Descarga los archivos desde el servidor FTP al directorio local.
    """
    try:
        # Cambiar al directorio remoto
        ftp_connection.cwd(remote_directory)

        # Descargar archivo 1
        filename = 'VIDEO_LD.mp4'
        local_path = os.path.join(local_directory, filename)
        ftp_connection.retrbinary('RETR ' + filename, open(local_path, 'wb').write)

        # Descargar archivo 2
        filename = 'es.vtt'
        local_path = os.path.join(local_directory, filename)
        ftp_connection.retrbinary('RETR ' + filename, open(local_path, 'wb').write)

    except Exception as e:
        print(f'Error al descargar archivos: {e}')

def check_encoding(filepath):
    """
    Comprueba que la codificación del archivo sea UTF-8.
    """
    encoding = 'utf-8'
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            f.read()
        print(f'El archivo {filepath} tiene una codificación válida de {encoding}')
    except Exception as e:
        print(f'El archivo {filepath} no tiene una codificación válida de {encoding}')

def split_subtitles(subtitle_file):
    """
    Divide los subtítulos en fragmentos de 30 minutos cada uno.
    """
    try:
        subs = pysubs2.load(subtitle_file)
        duration = 1800 # 30 minutos en segundos
        start_time = 0
        fragment_index = 0
        for i in range(0, len(subs)):
            if subs[i].start > start_time + duration:
                fragment = subs[start_time:i]
                fragment.save(f'{fragment_index}.vtt')
                start_time = subs[i].start
                fragment_index += 1
        fragment = subs[start_time:]
        fragment.save(f'{fragment_index}.vtt')
        print(f'{fragment_index + 1} fragmentos creados con éxito')
    except Exception as e:
        print(f'Error al dividir subtítulos: {e}')

if __name__ == '__main__':
    # Conectarse al servidor FTP
    ftp = FTP('ftp.ejemplo.com')
    ftp.login()

    # Pedir al usuario la ruta del directorio
    remote_directory = input("Ingrese la ruta del directorio donde se encuentran los archivos: ")

    # Descargar archivos
    local_directory = os.getcwd()
    download_files(ftp, remote_directory, local_directory)

    # Cerrar conexión
    ftp.quit()

    # Sincronizar subtítulos
    subtitle_file = 'es.vtt'
    video_file = 'VIDEO_LD.mp4'
    try:
        subprocess.run(['ffsubsync', video_file, subtitle_file])
        print("Subtitulos sincronizados exitosamente.")
    except Exception as e:
        print(f'Error al sincronizar subtítulos: {e}')

    # Comprobar codificación de los ficheros
    check_encoding(subtitle_file)
    #divide los subtítulos
    split_subtitles(subtitle_file)
