"""
NOTEPADAI
(Prepare)

A script to download/check the data set in order to promise functionality
Reference: Mozilla Voice Dataset - https://voice.mozilla.org/en/datasets
"""

import os
import requests
import sys
import tarfile

# Download link for the Mozilla Common Voice package (generated from my email address)
URL = "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335139bd3fb4.s3.amazonaws.com/cv-corpus-1/"  # LANG.tar.gz

VALID_LANGUAGES = {
    'en': "English",
    'de': "German",
    'fr': "French",
    'cy': "Welsh",
    'br': "Breton",
    'cv': "Chuvash",
    'tr': "Turkish",
    'tt': "Tatar",
    'ky': "Kyrgyz",
    'ga-IE': "Irish",
    'kab': "Kabyle",
    'ca': "Catalan",
    'zh-TW': "Chinese (Taiwan)",
    'sl': "Slovenian",
    'it': "Italian",
    'nl': "Dutch",
    'cnh': "Hakha Chin",
    'eo': "Esperanto"
}


class Prepare:
    def __init__(
            self,
            lang=list(VALID_LANGUAGES)[0],
            path='./', mode="download",
            show_progress=True,
            del_archive=True):

        self.lang = lang
        self.path = path

        self.__check_lang()

        try:
            os.mkdir(os.path.join(path, lang))
        except OSError:
            pass
        self.path = os.path.join(self.path, lang)

        if mode is "download":
            self.archive = os.path.join(path, lang, lang + ".tar.gz")
            self.__download_data(show_progress)
        elif mode is "extract":
            self.archive = os.path.join(path, lang + ".tar.gz")
        else:
            print("Invalid mode. Valid modes are 'download' and 'extract'.")
            sys.exit(3)

        self.__extract_data()

        if del_archive:
            self.__del_archive()

    def __check_lang(self):
        if self.lang not in VALID_LANGUAGES.keys():
            print("Invalid language code.")
            print("Currently available languages are:")
            for key in VALID_LANGUAGES:
                print(key + "  - " + VALID_LANGUAGES[key])
            sys.exit(2)

    def __download_data(self, show_progress=False):
        url = URL + self.lang + ".tar.gz"
        print("Downloading a new data set in " + VALID_LANGUAGES[self.lang] + " to " + self.path)
        print("from " + url + "...")
        try:
            if show_progress:
                from tqdm import tqdm_gui
                with open(self.archive, "wb") as file:
                    for data in tqdm_gui(requests.get(url, stream=True).iter_content()):
                        file.write(data)
            else:
                from tqdm import tqdm
                with open(self.archive, "wb") as file:
                    for data in tqdm(requests.get(url, stream=True).iter_content()):
                        file.write(data)
        except KeyboardInterrupt:
            print("Interrupted by user.")
            self.__del_archive()
            sys.exit(1)

    def __extract_data(self):
        try:
            with tarfile.open(self.archive) as tar:
                def is_within_directory(directory, target):
                	
                	abs_directory = os.path.abspath(directory)
                	abs_target = os.path.abspath(target)
                
                	prefix = os.path.commonprefix([abs_directory, abs_target])
                	
                	return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                	for member in tar.getmembers():
                		member_path = os.path.join(path, member.name)
                		if not is_within_directory(path, member_path):
                			raise Exception("Attempted Path Traversal in Tar File")
                
                	tar.extractall(path, members, numeric_owner=numeric_owner) 
                	
                
                safe_extract(tar, path=self.path)
                tar.close()
        except RuntimeError:
            print("Couldn't find data set (" + self.archive + ")")
            sys.exit(4)

    def __del_archive(self):
        os.remove(self.archive)
