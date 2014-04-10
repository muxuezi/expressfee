# -*- coding: utf-8 -*-
# 自动加载excel，输出汇总excel，名称为”T_文件名“

import pandas as pd
from glob import glob
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()

LINK_OBJ = [u'书名2', u'备注', u'备注1']
ADD_OBJ = [u'合计库存数量', u'保留1年销售后报废数量', u'报废码洋']


def showobj(obj):
    for idx, l in enumerate(obj):
        print idx + 1, l


def objparse(obj):
    return [x.strip() for x in obj.split(',')]


def inputobj(obj, defautlobj):
    return objparse(obj) if obj else defautlobj


def objnames(bookall):
    allcol = bookall.columns
    print u'所有列名:\n', bookall.columns
    print ''

    link_obj = raw_input(u'******请输入要连接的列名,用逗号(,)分割:\n')
    link_obj = inputobj(link_obj, LINK_OBJ)
    print u'要连接的列名:\n', showobj(link_obj)
    print ''

    add_obj = raw_input(u'******请输入要相加的列名,用逗号分割:\n')
    add_obj = inputobj(add_obj, ADD_OBJ)
    print u'要相加的列名:\n', showobj(add_obj)
    print ''

    return allcol, link_obj, add_obj


def booksort(fname):
    outputfname = 'T_' + fname
    sheetname = pd.ExcelFile(fname).sheet_names[0]
    bookall = pd.read_excel(fname, sheetname)
    allcol, link_obj, add_obj = objnames(bookall)
    obj = 'ISBN'
#     bookall = bookall.fillna()
    bookgroup = bookall.groupby(obj)
#     print bookgroup.groups
    bookgps = []
    booksingle = [v[1][0] for v in bookgroup.groups.items() if len(v[1]) == 1]
    bookmuit = [v for v in bookgroup.groups.items() if len(v[1]) > 1]
    for k, v in bookmuit:
        bookunit = []
        # bookunit.append()
        for i in allcol:
#             i = i.encode('utf-8')
            if i in link_obj:
                bookunit.append('&&'.join([str(x)
                                for x in bookall.ix[v, i].values]))
            elif i in add_obj:
                bookunit.append(bookall.ix[v, i].sum())
            else:
                bookunit.append([x for x in bookall.ix[v, i] if x != 'nan'][0])
        bookgps.append(bookunit)
    bookmuitall = pd.DataFrame(data=bookgps, columns=bookall.columns)
    print u'要合并的ISBN有:\n',
    for k, idx in bookmuit:
        print int(k), idx
    print ''
    booksingleall = bookall.iloc[booksingle]
    booktotal = pd.concat([bookmuitall, booksingleall]).sort(obj, ascending=1)
    booktotal.to_excel(outputfname, sheetname, index=False)


for fname in [f for f in glob('*.xls*') if not f.startswith('T')]:
    booksort(fname)
    print fname, u'处理完毕'
print 'K.O.'
