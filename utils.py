import hashlib
import numpy as np
import os
from error import FileNotSelectedError, FileSizeError, LanguageError

ROOT = os.getcwd()
LANGUAGES = ['en', 'hi', 'ar', 'fr', 'de', 'es', 'pt', 'pl', 'it', 'tr', 'ru', 'nl', 'cs', 'zh-cn', 'ja', 'ko', 'hu']


def hash256(input_string):
    input_bytes = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_bytes)
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def rand(n=4):
    char = "abcdefghijklmnopqrstuvwxyz"
    arr = np.random.randint(0, 26, size=n)
    name = [char[i] for i in arr]
    return ''.join(name)


def get_dir(path):
    d = os.path.join(ROOT, path)
    if not os.path.isdir(d):
        os.mkdir(d)
    return d


def get_speakers(tag):
    d = os.path.join(get_dir("speakers"), tag)
    speakers = [os.path.join(d, i) for i in os.listdir(d)]
    return speakers


def file_check(file_path):
    file_size_bytes = os.path.getsize(file_path)
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    if file_size_mb > 24:
        raise FileSizeError()


def save_speaker(file):
    if file.filename == '':
        raise FileNotSelectedError

    d = os.path.join(get_dir("speakers"), "custom")
    extension = file.filename.split(".")[-1]
    code = rand(4)
    filename = code + "." + extension
    file_path = os.path.join(d, filename)
    file.save(file_path)
    file_check(file_path)
    return file_path, code


def save_file(file):
    if file.filename == '':
        raise FileNotSelectedError

    d = get_dir("files")
    extension = file.filename.split(".")[-1]
    filename = rand(8) + "." + extension
    file_path = os.path.join(d, filename)
    file.save(file_path)
    file_check(file_path)
    return file_path


def check_language(lang):
    if lang not in LANGUAGES:
        raise LanguageError()
