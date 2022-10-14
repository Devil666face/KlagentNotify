import KlAkOAPI.ChunkAccessor
import time
import csv
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup

class KscHostInfo:
    def __init__(self, server):
        self.server = server


    def get_host_dict(self):
        # self.fields_to_select =  ["KLHST_WKS_DN","KLHST_WKS_STATUS","KLHST_WKS_FQDN"]
        self.fields_to_select =  ["KLHST_WKS_FQDN","KLHST_WKS_STATUS"]
        strAccessor = KlAkOAPI.HostGroup.KlAkHostGroup(self.server).FindHosts("", self.fields_to_select, [], {'KLGRP_FIND_FROM_CUR_VS_ONLY': False}, lMaxLifeTime = 60 * 60).OutPar('strAccessor')
        oChunkAccessor = KlAkOAPI.ChunkAccessor.KlAkChunkAccessor(self.server)    
        nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()      
        result_list = list()
        for nStart in range(0, nCount, 1000):
            oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, 1000)
            oHosts = oChunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']
            for oObj in oHosts:
                result_list.append([self.get_field(oObj, field) for field in self.fields_to_select])

        # self.save_in_csv('host',result_list)
        return self.sorted_dict(hosts=result_list)
        

    def sorted_dict(self, hosts):
        host_dict = dict()
        for host in hosts:
            if not host[0] in host_dict:
                host_dict[host[0]] = [host[1]]
            else:
                host_active_list = host_dict[host[0]]
                host_active_list.append(host[1])
        return host_dict


    def get_field(self, oObj, field_name):
        try:
            return oObj[field_name]
        except:
            return "-"


    def save_in_csv(self, table_name, data):
        with open(f'{table_name}.csv','w',encoding='cp1251',newline='') as file:
            writer = csv.writer(file,delimiter=';')
            for row in data:
                writer.writerow(row)