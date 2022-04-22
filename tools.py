# _*_ coding: utf-8 _*_
import os
import json
import pandas as pd

from typing import Dict
from typing import List
from typing import Optional


def conver_dic(dict: Optional[Dict]) -> Dict:
    """ 字典换key """

    dict.update({"最低薪资": dict.pop("min")})
    dict.update({"平均薪资": dict.pop("mean")})
    dict.update({"最高薪资": dict.pop("max")})
    return dict


def json2csv(data: List[dict], filename: str = 'data', encoding='utf_8'):
    """ json数据转存到csv

    :param data: JSON数据
    :param filename: CSV文件名
    """

    filename = filename if filename[-4:] == '.csv' else f'{filename}.csv'

    format_data = [{k: json.dumps(v, ensure_ascii=False).replace(',', ' ').replace('\n', ' ') for k, v in item.items()} for item in data]
    dataframe = pd.DataFrame(format_data)

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    if os.path.exists(filename):
        dataframe.to_csv(filename, mode='a', encoding=encoding, index=False, index_label=False, sep=',', header=False)
    else:
        dataframe.to_csv(filename, mode='a', encoding=encoding, index=False, index_label=False, sep=',')


def csv_to_xlsx(csv_dir):
    csv = pd.read_csv(csv_dir, encoding='utf-8')
    csv.to_excel(f'{csv_dir[:-4]}.xlsx', sheet_name='data')
