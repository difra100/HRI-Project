"""
Utilities.
"""
import os 
import subprocess
import zipfile
import tarfile
import os
import re


def clean_string(input_string):
    # Use regex to remove non-alphanumeric characters
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s\p{P}]+', '', input_string)

    return cleaned_string

def extract_multistream_bz2(bz2_filepath, output_filepath):
    if not os.path.exists(output_filepath):
        command = ['bzip2', '-dk', bz2_filepath]
        subprocess.call(command)
        print("File extracted successfully.")
    else:
        print("Output file already exists. Skipping extraction.")

def check_and_download_file(filename, directory, url):
    filepath = os.path.join(directory, filename)

    # Check if the file already exists
    if os.path.isfile(filepath):
        return True
    else:
        # Download the file using wget
        wget_command = ["wget", "-P", directory, url]
        subprocess.call(wget_command)
        print("File downloaded:", filepath)

def unzip_file_if_needed(zip_path, extract_path):
    print("Inside UNZIP", zip_path, extract_path)
    if not os.path.exists(extract_path) or not os.listdir(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print("File unzipped successfully.")
    else:
        print("Destination directory is not empty. Skipping unzip operation.")

def un_tgz_file_if_needed(tgz_path, extract_path):
    if not os.path.exists(extract_path) or not os.listdir(extract_path):
        with tarfile.open(tgz_path, 'r') as tar_ref:
            tar_ref.extractall(extract_path)
        print("File extracted successfully.")
    else:
        print("Destination directory is not empty. Skipping extraction.")

import os
import pickle
import hashlib
CACHE_DIR = "../cache"

def get_hash(*args, **kwargs):
    hash_object = hashlib.md5()
    hash_object.update(repr(args).encode('utf-8'))
    hash_object.update(repr(kwargs).encode('utf-8'))
    return hash_object.hexdigest()

def persistent_disk_memoize(func):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    def memoized_func(*args, **kwargs):
        cache_key = get_hash(args, kwargs)
        cache_file = os.path.join(CACHE_DIR, "{}_{}.pkl".format(func.__name__, cache_key))

        if os.path.exists(cache_file):
            print("Loading from cache")
            with open(cache_file, "rb") as f:
                result = pickle.load(f)
        else:
            print("Recomputing")
            result = func(*args, **kwargs)
            with open(cache_file, "wb") as f:
                pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)

        return result

    return memoized_func
