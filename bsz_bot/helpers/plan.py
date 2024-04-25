import requests
from requests.auth import HTTPBasicAuth
from pdf2image import convert_from_path
from PIL import Image

class Plan:
    def __init__(self, file_url : str, username : str = '', password : str = '', output_name : str = 'document') -> None:
        self.__file_url = file_url
        self.__username = username
        self.__password = password
        self.__output = output_name

    def fetch(self):
        response = requests.get(self.__file_url, auth=HTTPBasicAuth(self.__username, self.__password))

        if response.status_code == 200:
            with open(f"{self.__output}.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)
            return 200
        else:
            return response.status_code
        
    def save_as_png(self):
        images = convert_from_path(f"{self.__output}.pdf")

        combined_image = Image.new('RGB', (images[0].width, sum(image.height for image in images)))

        y_offset = 0
        for image in images:
            combined_image.paste(image, (0, y_offset))
            y_offset += image.height

        combined_image.save(f"{self.__output}.png", 'PNG')

    def download(self):
        error_code = self.fetch()
        if error_code == 200:
            self.save_as_png()
        return error_code
