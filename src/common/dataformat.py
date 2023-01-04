#!/usr/bin/python3
import xlrd
import logging
import logging.handlers
import datetime
import decimal
from decimal import localcontext
from typing import Union
import  os

import collections.abc
import numbers
from typing import Any
import  csv

bytes_types = (bytes, bytearray)
integer_types = (int,)
text_types = (str,)
string_types = (bytes, str, bytearray)


def is_integer(value: Any) -> bool:
    return isinstance(value, integer_types) and not isinstance(value, bool)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes_types)


def is_text(value: Any) -> bool:
    return isinstance(value, text_types)


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


def is_boolean(value: Any) -> bool:
    return isinstance(value, bool)


def is_dict(obj: Any) -> bool:
    return isinstance(obj, collections.abc.Mapping)


def is_list_like(obj: Any) -> bool:
    return not is_string(obj) and isinstance(obj, collections.abc.Sequence)


def is_list(obj: Any) -> bool:
    return isinstance(obj, list)


def is_tuple(obj: Any) -> bool:
    return isinstance(obj, tuple)


def is_null(obj: Any) -> bool:
    return obj is None


def is_number(obj: Any) -> bool:
    return isinstance(obj, numbers.Number)

def FromWei(number: int, unit: int) -> Union[int, decimal.Decimal]:

    if number == 0:
        return 0
    unit_value = decimal.Decimal(10**unit)

    with localcontext() as ctx:
        ctx.prec = 999
        d_number = decimal.Decimal(value=number, context=ctx)
        result_value = d_number / unit_value

    return result_value


def ToWei(number: Union[int, float, str, decimal.Decimal], unit: int) -> int:
  
    if is_integer(number) or is_string(number):
        d_number = decimal.Decimal(value=number)
    elif isinstance(number, float):
        d_number = decimal.Decimal(value=str(number))
    elif isinstance(number, decimal.Decimal):
        d_number = number
    else:
        raise TypeError("Unsupported type.  Must be one of integer, float, or string")

    s_number = str(number)
    unit_value = decimal.Decimal(10**unit)

    if d_number == decimal.Decimal(0):
        return 0

    if d_number < 1 and "." in s_number:
        with localcontext() as ctx:
            multiplier = len(s_number) - s_number.index(".") - 1
            ctx.prec = multiplier
            d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with localcontext() as ctx:
        ctx.prec = 999
        result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value
    return int(result_value)

def GetExcelData(file_xls):   
    book = xlrd.open_workbook(file_xls)
    sheet = book.sheets()[0]
    nrows = sheet.nrows
    ncols = sheet.ncols
    i = 0
    result = []
    while i < nrows:
        row_value = sheet.row_values(i)
        dict_data = []
        for j in range(ncols):
            dict_data.append(row_value[j])
        result.append(dict_data)
        i = i+1
    return result  

def GetCsvData(file_csv):   
    result = []
    with open(file_csv) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                result.append(row)
    return result  


logger = logging.getLogger('standard')
logger.setLevel(logging.DEBUG)
def InitLog(path:str, project:str):
    d = datetime.datetime.today()
    if os.path.exists(path) == False : 
        os.mkdir(path)

    all_log =  path + project + "_" + d.strftime('%Y%m%d%H') +"_all.log"
    error_log = path + project + "_" +d.strftime('%Y%m%d%H') +"_error.log"
 
    rf_handler = logging.handlers.TimedRotatingFileHandler(all_log, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    f_handler = logging.FileHandler(error_log)
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
  