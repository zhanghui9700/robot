#-*- coding=utf-8 -*-

import logging
import os
import xlrd

LOG = logging.getLogger(__name__)


class Product(object):

    def __init__(self, top_category, category, number, quantity):
        self.top_category = top_category
        self.category = category
        self.number = number
        self.quantity = quantity

    def __str__(self):
        return "%s: %s" % (self.number, self.quantity)

    def __repr__(self):
        return u"%s: %s" % (self.number, self.quantity)



class OrderTarget():

    def __init__(self, path="/opt/18m/excels/"):
        self.path = path
        self.target = None
        self._find_target()

    def _find_target(self):
        os.chdir(self.path)
        excels = []
        for f in os.listdir('.'):
            if os.path.isfile(f):
                ext = os.path.splitext(f)[1]
                if ext in [".xls", ".xlsx"]:
                    excels.append(f)

        for excel in excels:
            xls_path = os.path.join(self.path, excel)
            xls_done_path = "%s.done" % xls_path
            xls_done = os.path.exists(xls_done_path)
            if not xls_done:
                self.target = xls_path
                break
        LOG.info("find excel by path: %s, target: %s", 
                            self.path, self.target)

    def mark_complete(self):
        if not self.target:
            return

        p = "%s.done" % self.target
        with open(p, 'a'):
            os.utime(p, None)
        LOG.info("xtouch %s", p) 

    def construct(self): 
        if not self.target:
            LOG.info("no target excel find break") 
            return None

        book = xlrd.open_workbook(self.target)
        sheet = book.sheet_by_index(0)
        rows, cols = sheet.nrows, sheet.ncols
        start_row = 0 
        while True:
            header = sheet.cell_value(rowx=start_row, colx=0)
            if header.startswith("PC"):
                break
            else:
                start_row += 1

        if start_row > rows:
            for rx in range(sheet.nrows):
                LOG.info(sheet.row(rx))
            raise Exception("excel data foramt error")

        _ = {}
        for row in range(rows):
            if row < start_row:
                continue
            top_category, category, product, desc, quantity = [
                    sheet.cell_value(rowx=row, colx=i) for i in range(5)]
            _.setdefault(top_category, {}).setdefault(category, []).append(
                Product(top_category, category, product, int(quantity)))

        result =  []
        for top, v in _.items():
            for category, products in v.items():
                result.append({"top": top,
                               "category": category, 
                               "product_ids": products})

        LOG.info("target order: %s", result)
        return result
