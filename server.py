import urllib3
import socket
import os
from pathlib import Path
from KlAkOAPI.AdmServer import KlAkAdmServer


class KscServer:
    def __init__(self, **kwargs):
        urllib3.disable_warnings()
        server_url = f"https://{socket.getfqdn(kwargs.get('ip',''))}:{kwargs.get('server_port','13299')}"
        path_to_SSL_verify_cert = Path(os.getcwd(),'klserver.cer')
        self.server = KlAkAdmServer.Create(server_url, kwargs.get('username'), kwargs.get('password'), verify = path_to_SSL_verify_cert) 
    
    def get_server(self):
        return self.server