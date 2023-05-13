import os

from fastapi import UploadFile, File
from loguru import logger

from services.Storage import Storage


def save_file_place(file: UploadFile = File(...)):
    try:
        content = file.file.read()

        with open('tmp_files/' + file.filename, 'wb') as f:
            f.write(content)

        s3 = Storage('photo-place')
        file_url = s3.save_file(file.filename)
    except Exception as e:
        logger.error(f'Возникла ошибка в сохранении файла {e}')
        raise e

    finally:
        file.file.close()
        if os.path.isfile('tmp_files/' + file.filename):
            os.remove('tmp_files/' + file.filename)

    return file_url


def save_file_user(file: UploadFile = File(...)):
    try:
        content = file.file.read()

        with open('tmp_files/' + file.filename, 'wb') as f:
            f.write(content)

        s4 = Storage('photo-user')
        file_url = s4.save_file(file.filename)
    except Exception as e:
        logger.error(f'Возникла ошибка в сохранении файла {e}')
        raise e

    finally:
        file.file.close()
        if os.path.isfile('tmp_files/' + file.filename):
            os.remove('tmp_files/' + file.filename)

    return file_url


def save_file_ad(file: UploadFile = File(...)):
    try:
        content = file.file.read()

        with open('tmp_files/' + file.filename, 'wb') as f:
            f.write(content)

        s3 = Storage('photo-ad')
        file_url = s3.save_file(file.filename)
    except Exception as e:
        logger.error(f'Возникла ошибка в сохранении файла {e}')
        raise e

    finally:
        file.file.close()
        if os.path.isfile('tmp_files/' + file.filename):
            os.remove('tmp_files/' + file.filename)

    return file_url
