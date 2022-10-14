# #!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""This module presents samples of usage KlAkOAPIWrapperLib package to parse, compose and output KlAkParams object. KlAkParams corresponds to params container that is essential part of KLOAPI."""

import sys
import datetime
from KlAkOAPI.Params import KlAkParams, KlAkArray, paramString, paramInt, paramBool, paramLong, paramDateTime, paramDate, paramParams, paramArray, paramFloat, paramDouble, paramBinary
from KlAkOAPI.Error import KlAkParamTypeError
    
def KlAkParams_Output():    
    """ This module shows how you can compose KlAkParams, parse its contents and use advantages of formatted output"""
    print (main.__doc__)
    
    # sample of raw data that can be recieved in response to KLOAPI call (such as KlAkOAPI.ReportManager.GetStatisticsData(...))
    print('- parse data')
    data = {'KLRPT_CHART_DATA': [{'type': 'params', 'value': {'data': [20, 10, 1], 'name': '2 days ago'}}, {'type': 'params', 'value': {'data': [20, 10, 1], 'name': '1 day ago'}}], 'KLRPT_CHART_DATA_DESC': 'Amounts of vulnerability instances', 'KLRPT_CHART_SERIES': ['critical', 'high-level', 'warning-level'], 'KLRPT_CHART_STACK_SERIES': True, 'TIME_CREATED': {'type': 'datetime', 'value': '2020-04-08T12:22:35Z'}}
    print('Sample of raw data that can be recieved in response to KLOAPI call:')
    print(data, '\n')
    
    parsed_data = KlAkParams(data)
    print ('Same data in terms of KLOAPI data types:')
    print(parsed_data)
    
    chart_array = parsed_data['KLRPT_CHART_DATA']
    print('Extracted 0-th chart data is:\n', chart_array[0])
    
    time_created = parsed_data['TIME_CREATED']
    print('Chart created time (parsed_data["TIME_CREATED"]) is:\n', time_created, '\n')

    # samples of composing data for input parameter to KLOAPI call  (such as KlAkOAPI.ReportManager.RequestStatisticsData(...))
    print('- compose data')
    # composing params as dictionary
    options_products = KlAkParams({'KLRPT_PROD_NAME': '1093', 'KLRPT_PROD_NAME_LOC': 'Administration server', 'KLRPT_PROD_VER': '1.0.0.0'})
   
    # other type of composing - add values one by one; other params can be added as well
    options_format = KlAkParams()
    options_format.AddInt('KLRPT_TARGET_TYPE', 0)
    options_format.AddBool('KLRPT_PDF_LANDSCAPE', True)
    options_format.AddDateTime('KLRPT_TIME_CREATED', datetime.datetime.now())
    options_format.AddParams('KLRPT_PRODUCTS', options_products)
    
    # output the composed data on different levels of abstraction 
    print('Sample of composed data:')
    print(options_format)   
    print('Same data, raw output (protocol level abstraction, this data is used in HTTP POST method):')
    print(options_format.data, '\n')
    print('Same data, in terms of JSON / python data types (language-level abstraction, formatted for better readability):')
    print(options_format.PrintRaw())    
    
    # compose params with other params using converters: paramParams, paramInt, etc.
    options_timezone = KlAkParams({'RPT_TZ_BIAS': paramInt(-180), 'RPT_TZ_DAYLIGHT_BIAS': paramInt(-60), 'RPT_TZ_DAYLIGHT_DATE': paramParams({'RPT_STM_DAY':0, 'RPT_STM_DAYOFWEEK':0, 'RPT_STM_HOUR':0, 'RPT_STM_MILLISECOND':0, 'RPT_STM_MINUTE':0, 'RPT_STM_MONTH':0, 'RPT_STM_SECOND':0, 'RPT_STM_YEAR':0}), 'RPT_TZ_DAYLIGHT_NAME': paramString('Russia TZ 2 Daylight Time')})
 
    # compose array of params
    array_loc_products = KlAkArray()
    array_loc_products.AddParams(options_products)
    array_loc_products.AddParams({'KLRPT_PROD_NAME': '1103', 'KLRPT_PROD_NAME_LOC': 'Nagent', 'KLRPT_PROD_VER': '1.0.0.0'})
    
    options = KlAkParams()
    # compose array of params - use KlAkParams
    options.AddArray('KLRPT_LOC_PRODUCTS_1', array_loc_products)        
    # other way of composing array of params - use converters
    options.AddArray('KLRPT_LOC_PRODUCTS_2', [paramParams(options_products), paramParams({'KLRPT_PROD_NAME': '1103', 'KLRPT_PROD_NAME_LOC': 'Nagent', 'KLRPT_PROD_VER': '1.0.0.0'})])    
    # compose value from another params
    options.Add('KLRPT_LOC_PRODUCT', options_format.GetValue('KLRPT_PRODUCTS'))
    options.Add('KLRPT_TIME_CREATED', options_format.GetValue('KLRPT_TIME_CREATED'))

    # output the composed data on different levels of abstraction 
    print('Sample of other data, in terms of KLOAPI data types (application level abstraction, data samples in KLOAPI documentation are given in this view):')
    print(options)
    print('Same data, raw output (protocol level abstraction, this data is used in HTTP POST method):')
    print(options.data)
    
    
def main():
    KlAkParams_Output()

    
if __name__ == '__main__':
    main()