
from host import KscHostInfo
from sort import Sorter
from database import Database
from datetime import datetime

class Analyzer:
    def __init__(self, server):
        database = Database()
        self.dict_old = database.get_dict()
        host_list = KscHostInfo(server).get_host_dict()
        self.sorted_dict_new = Sorter(host_list).get_reuslt_dict()
        
    def compare_dicts(self):
        message=''
        suspect_host_list = []
        for new_key in self.sorted_dict_new:
            old_value_status = self.dict_old.get(new_key, 'new_host')
            new_value_status = self.sorted_dict_new[new_key]

            # Новый хост
            if old_value_status=='new_host':
                message+=f'[{self.time()}] [Host:{new_key}] [Info:New host]\n'

            # У хоста изменился статус
            if old_value_status!=new_value_status:
                message+=f'[{self.time()}] [Host:{new_key}] [Info:{self.get_message(old_value_status, new_value_status)}]\n'

                # У хоста изменился статус и получился статус аларма
                if self.alarm_status(new_value_status, add_host_without_agent=False):
                    # Аларм сработает только если статус хоста поменялся по сравнению с предыдущим
                    message+=f'[{self.time()}] [Host:{new_key}] [Alarm status:{new_value_status}] [Info:{self.get_full_info(new_value_status)}]\n'

        
            # Подозрительный хост
            if self.suspect_status(new_value_status):
                suspect_host_list.append([f'{self.time()}',new_key, new_value_status, self.get_full_info(new_value_status)])

        return message, suspect_host_list

    def suspect_status(self, status_new):
        '''Подозрительный хост'''
        five_bit_digit_list_new = self.make_five_bit_digit(list(self.get_bin_digit(status_new)))
        if five_bit_digit_list_new[5]==1 and five_bit_digit_list_new[3]==0:
            # Хост включен и Агент не установлен
            return True
        if five_bit_digit_list_new[5]==1 and (five_bit_digit_list_new[2]==0 or five_bit_digit_list_new[1]==0):
            # Хост включен и (Агент не активен или постоянная защита не установлена) вне зависимости от установленности агента
            return True
        return False

    def alarm_status(self, status_new, add_host_without_agent):
        '''Аларм хост'''
        five_bit_digit_list_new = self.make_five_bit_digit(list(self.get_bin_digit(status_new)))
        # if five_bit_digit_list_new[5]==1 and five_bit_digit_list_new[3]==1 and (five_bit_digit_list_new[2]==0 or five_bit_digit_list_new[1]==0):
        #     #Хост-виден и агент-установлен и (агент-не активен или постоянная защита-не установлена)
        #     return True
        if five_bit_digit_list_new[5]==1 and (five_bit_digit_list_new[3]==0 or five_bit_digit_list_new[2]==0 or five_bit_digit_list_new[1]==0):
            #Хост-виден и агент-перестал быть установлен относительно предыдущего снимка
            return True
        return False

    def get_message(self, status_old, status_new):
        '''Получаем разницу между старым и новым статусом'''
        five_bit_digit_list_old = self.make_five_bit_digit(list(self.get_bin_digit(status_old)))
        five_bit_digit_list_new = self.make_five_bit_digit(list(self.get_bin_digit(status_new)))
        return self.make_message(five_bit_digit_list_old, five_bit_digit_list_new)

    def get_full_info(self, status):
        '''Получаем всю инфу по статусу хоста'''
        five_bit_digit = self.make_five_bit_digit(list(self.get_bin_digit(status)))
        message = ['Видимость хоста:',
                    '',
                    'Агент администрирования установлен:',
                    'Агент администрирования активен:',
                    'Установлена постоянная защита:',
                    'Компьютер временно переключен на текущий сервер:']
        for i in range(6):
            try:
                if i!=1:
                    message[i] = f'{message[i]} {self.get_status(five_bit_digit[5-i])}'
            except Exception as ex:
                print(ex)
                print(f'Err on {i} {five_bit_digit}')
        message.pop(1)
        return '|'.join(message)

    # Все следующие методы для вас черный ящик
    def make_five_bit_digit(self, bin_digit_list:list):
        for i in range(6-len(bin_digit_list)):
            bin_digit_list.insert(0,'0')
        five_bit_digit_list = list(map(int,bin_digit_list))
        return five_bit_digit_list

    def make_message(self, bit_digit_old, bit_digit_new):
        message = list()
        if bit_digit_old[5]==0 and bit_digit_new[5]==1:
            message.append('Хост включился')
        if bit_digit_old[5]==1 and bit_digit_new[5]==0:
            message.append('Хост выключился')

        if bit_digit_old[3]==0 and bit_digit_new[3]==1:
            message.append('Статус агента сменился на установлен')
        if bit_digit_old[3]==1 and bit_digit_new[3]==0:
            message.append('Статус агента сменился на не установлен')
            
        if bit_digit_old[2]==0 and bit_digit_new[2]==1:
            message.append('Агент стал активным')
        if bit_digit_old[2]==1 and bit_digit_new[2]==0:
            message.append('Агент стал не активным')

        if bit_digit_old[1]==0 and bit_digit_new[1]==1:
            message.append('Постоянная защита установлена')
        if bit_digit_old[1]==1 and bit_digit_new[1]==0:
            message.append('Постоянная защита разорвана')
        
        if bit_digit_old[0]==0 and bit_digit_new[0]==1:
            message.append('Компьютер был временно переключен на текущий сервер в результате переключения профиля NLA')
        if bit_digit_old[0]==1 and bit_digit_new[0]==0:
            message.append('Компьютер был отключен с текущего сервера в результате переключения профиля NLA')

        return '|'.join(message)

    def get_status(self, bin_status):
        return "Да" if bin_status==1 else "Нет"

    def get_bin_digit(self, status):
        return str(bin(status)).replace('0b','')

    def time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%SS").replace('S','')