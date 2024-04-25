import requests
import json
from requests.auth import HTTPBasicAuth
from pdf2image import convert_from_path
from PIL import Image
from .log import logger

import hashlib  
  
def hash_read_file(fileName):
  
    h1 = hashlib.sha1()
    with open(fileName, "rb") as file:
  
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h1.update(chunk)
              
    # 160bit digest should be enough
    return h1.hexdigest()

class Plan:
    __settings_file = "auth_settings.json"

    def __init__(self) -> None:
        self.__error = False
        self.__load_settings()

    @staticmethod
    def save_settings(file_url : str = '', username : str = '', password : str = '', output_name : str = 'document'):
        data = {
            'file_url': file_url,
            'username': username,
            'password': password,
            'output_name': output_name
        }
        with open(Plan.__settings_file, 'w') as file:
            json.dump(data, file, indent=4)

    def __load_settings(self):
            try:
                with open(Plan.__settings_file, 'r') as file:
                    data = json.load(file)
                self.__file_url = data['file_url']
                self.__username = data['username']
                self.__password = data['password']
                self.__output = data['output_name']
            except FileNotFoundError:
                logger.error(f"{Plan.__settings_file} not found")                

    def fetch(self) -> int:
        response = requests.get(self.__file_url, auth=HTTPBasicAuth(self.__username, self.__password))

        if response.status_code == 200:
            with open(f"{self.__output}.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)
            return 200
        else:
            return response.status_code
        
    def save_as_png(self) -> None:
        images = convert_from_path(f"{self.__output}.pdf")

        combined_image = Image.new('RGB', (images[0].width, sum(image.height for image in images)))

        y_offset = 0
        for image in images:
            combined_image.paste(image, (0, y_offset))
            y_offset += image.height

        combined_image.save(f"{self.__output}.png", 'PNG')

    def download(self) -> int:
        error_code = self.fetch()
        if error_code == 200:
            self.save_as_png()
        return error_code
    
    def new_plan_available(self) -> bool:
        old_file_hash = hash_read_file(f"{self.__output}.pdf")
        if self.download() != 200:
            self.__error = True
            return False
        new_file_hash = hash_read_file(f"{self.__output}.pdf")
        self.__error = False
        return old_file_hash != new_file_hash

    def any_errors(self) -> bool:
        return self.__error
    
    def get_file_name(self) -> str:
        return self.__output
    
