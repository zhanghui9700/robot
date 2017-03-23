#-*- coding=utf-8 -*-

import logging
import os
import xlrd

LOG = logging.getLogger(__name__)


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
        """
        result =  [
            {"category": "T claim - tested working", 
             "product_ids": ["2447HU5_0001263", "428424U_0000057", "ZLNN3A6Y_000008"]}, 
            {"category": "G claim - tested/failed", 
             "product_ids": ["ZLNN14L0_000034", "4282AD4_0000008"]}, 
        ]
        """

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
            top_category, category, product = [
                    sheet.cell_value(rowx=row, colx=i) for i in range(3)]
            _.setdefault(category, []).append(product)

        result =  []
        for k,v in _.items():
            result.append({"category": k, "product_ids": v})

        LOG.info("target order: %s", result)
        return result
