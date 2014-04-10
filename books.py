# -*- coding: utf-8 -*-
# 自动加载所有excel，输出汇总excel，名称为”T_文件名“

import pandas as pd
from glob import glob

sheetname = u'F1库存汇总'


def booksort(fname):
    outputfname = 'T_' + fname
    bookall = pd.read_excel(fname, sheetname)
    bookall = bookall.fillna(0)
    bookgroup = bookall.groupby(u'书号')
    bookgps = []
    for k, v in bookgroup.groups.items():
        bookgps.append(
            (k, '&&'.join(bookall.ix[v, u'货位名称'].values), bookall.ix[v, u'F1库存数量'].sum()))
    booktotal = pd.DataFrame(
        data=bookgps, columns=bookall.columns).sort(u'书号', ascending=1)
    booktotal.to_excel(outputfname, sheetname, index=False)


def main():
    for fname in [f for f in glob('*.xls*') if not f.startswith('T')]:
        booksort(fname)

if __name__ == '__main__':
    main()
