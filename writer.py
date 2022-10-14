import csv


class Writer:
    def __init__(self, data):
        try:
            with open(f'suspend_host.csv','w',encoding='cp1251',newline='') as file:
                writer = csv.writer(file,delimiter=';')
                writer.writerow(['Host:','Alarm status:','Видимость','Агент установлен','Агент активен','Постоянная защита','Авт. распределение'])
                for row in data:
                    writer.writerow([row[0],row[1],row[2],*self.get_unpack_status(row[3])])
        except PermissionError as ex:
            pass

    def get_unpack_status(self, status_str):
        result_list = list()
        for tag in status_str.split('|'):
            result_list.append(str(tag).split(':')[1])
        return result_list
        