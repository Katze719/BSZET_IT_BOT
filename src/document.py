import requests
from requests.auth import HTTPBasicAuth

# Die URL des PDF-Dokuments mit Benutzername und Passwort
pdf_url = "http://geschuetzt.bszet.de/s-lk-vw/Vertretungsplaene/vertretungsplan-bs-it.pdf"

# Benutzername und Passwort für die Authentifizierung
benutzername = "bsz-et-2324"
passwort = "schulleiter#23"


def save_pdf_doc():
    response = requests.get(pdf_url, auth=HTTPBasicAuth(benutzername, passwort))

    if response.status_code == 200:
        with open("vertretungsplan.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        return 200
    else:
        return response.status_code
