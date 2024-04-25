import requests
from requests.auth import HTTPBasicAuth

def fetch_document(file_url : str, output_name : str = 'vertretungsplan.pdf' , username : str = '', password : str = ''):
    response = requests.get(file_url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        with open(output_name, "wb") as pdf_file:
            pdf_file.write(response.content)
        return 200
    else:
        return response.status_code
