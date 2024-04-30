import os
import requests
import json
import discord
from requests.auth import HTTPBasicAuth
from pdf2image import convert_from_path
from PIL import Image
from .log import logger
from .settings import GuildSettings

import hashlib  
  
def hash_read_file(fileName):
    """
    Calculate the SHA-1 hash of the contents of the file specified by fileName.

    Parameters:
    fileName (str): The path to the file for which the hash needs to be calculated.

    Returns:
    str: The SHA-1 hash digest of the file content.
    """
  
    h1 = hashlib.sha1()
    try: 
        with open(fileName, "rb") as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h1.update(chunk)
    except FileNotFoundError:
        logger.error(f"{fileName} not found")
        return "File not found"
              
    # 160bit digest should be enough
    return h1.hexdigest()

class Plan:
    __settings_file = "auth_settings.json"

    def __init__(self, guild : discord.Guild) -> None:
        """
        Initializes a new instance of the class.

        This constructor initializes the object with default values for the private variables `__error` and `__load_settings()`.
        The `__error` variable is set to `False`, indicating that no error has occurred.
        The `__load_settings()` method is called to load the settings for the object.

        Parameters:
            None

        Returns:
            None
        """
        self.__guild = guild
        self.__error = False
        self.__load_settings(guild)

    @staticmethod
    def save_settings(file_url : str = '', username : str = '', password : str = '', output_name : str = 'document'):
        """
        Save the settings to a JSON file.

        This static method saves the settings to a JSON file. The settings include the file URL, username, password, and output name.

        Parameters:
            file_url (str): The URL of the file. Defaults to an empty string.
            username (str): The username. Defaults to an empty string.
            password (str): The password. Defaults to an empty string.
            output_name (str): The name of the output. Defaults to 'document'.

        Returns:
            None
        """
        data = {
            'file_url': file_url,
            'username': username,
            'password': password,
            'output_name': output_name
        }
        with open(Plan.__settings_file, 'w') as file:
            json.dump(data, file, indent=4)

    def __load_settings(self, guild : discord.Guild):
            """
            Load the settings from the JSON file.

            This method reads the settings from a JSON file specified by `Plan.__settings_file`.
            It updates the object's private variables with the loaded settings such as `__file_url`, `__username`, `__password`, and `__output`.

            Parameters:
                None

            Returns:
                None
            """
            try:
                with open(Plan.__settings_file, 'r') as file:
                    data = json.load(file)
                self.__file_url = data['file_url']
                self.__username = data['username']
                self.__password = data['password']
                self.__output = data['output_name']
            except FileNotFoundError:
                logger.error(f"{Plan.__settings_file} not found")      

            settings = GuildSettings(guild)
            if settings.get("file_url") != '(use default)':
                self.__file_url = settings.get("file_url")
            if settings.get("username") != '(use default)':
                self.__username = settings.get("username")
            if settings.get("password") != '(use default)':
                self.__password = settings.get("password")
            self.__output = settings.get("output_name")

    def fetch(self) -> int:
        """
        Fetches the PDF file from the specified URL using HTTP GET request with authentication.
        
        Returns:
            int: The HTTP status code. Returns 200 if the request is successful and the PDF file is saved.
                 Otherwise, returns the corresponding HTTP status code.
        """
        response = requests.get(self.__file_url, auth=HTTPBasicAuth(self.__username, self.__password))
        self.__error_code = response.status_code
        if response.status_code == 200:
            with open(f"{os.getenv('SETTINGS_VOLUME')}/{self.__output}.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)
            self.__error = False
            return 200
        else:
            self.__error = True
            return response.status_code
        
    def save_as_png(self) -> None:
        """
        Save the combined images as a PNG file.

        Parameters:
            None

        Returns:
            None
        """
        images = convert_from_path(f"{os.getenv('SETTINGS_VOLUME')}/{self.__output}.pdf")

        combined_image = Image.new('RGB', (images[0].width, sum(image.height for image in images)))

        y_offset = 0
        for image in images:
            combined_image.paste(image, (0, y_offset))
            y_offset += image.height

        combined_image.save(f"{self.__output}.png", 'PNG')

    def download(self) -> int:
        """
        Fetches the data, saves it as a PNG if the fetch was successful, and returns the error code.
        """
        error_code = self.fetch()
        if error_code == 200:
            self.save_as_png()
        return error_code
    
    def new_plan_available(self) -> bool:
        """
        Checks if a new plan is available by comparing the hash of the old file with the hash of the new file.
        
        Returns:
            bool: True if a new plan is available, False otherwise.
        """
        old_file_hash = hash_read_file(f"{os.getenv('SETTINGS_VOLUME')}/{self.__output}.pdf")
        if self.download() != 200:
            self.__error = True
            return False
        new_file_hash = hash_read_file(f"{os.getenv('SETTINGS_VOLUME')}/{self.__output}.pdf")
        self.__error = False
        return old_file_hash != new_file_hash

    def any_errors(self) -> bool:
        """
        Check if there are any errors.

        Returns:
            bool: True if there are any errors, False otherwise.
        """
        return self.__error
    
    def get_error_code(self) -> int:
        """
        Returns the error code.

        :return: An integer representing the error code.
        :rtype: int
        """
        return self.__error_code
    
    def get_file_name(self) -> str:
        """
        Returns the name of the file associated with the object.

        :return: A string representing the name of the file.
        :rtype: str
        """
        return self.__output
    
