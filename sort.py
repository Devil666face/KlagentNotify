import csv
import socket
from database import Database

class Sorter:
    def __init__(self, host_dict):
        self.data = host_dict
        self.database = Database()


    def get_reuslt_dict(self):
        sorted_dict = {key:self.get_host_status(self.data[key]) for key in self.data}
        self.database.save_dict(sorted_dict)
        del self.database
        return sorted_dict
        
        
    def get_host_status(self, status_list:list):
        return sorted(status_list)[-1]
