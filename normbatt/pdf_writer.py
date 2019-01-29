# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import string
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


class PDFWriter:
    """
    A class to provide an API for writing lines of plain text
    to a PDF file.

    """

    def __init__(self, pdf_fn):
        """

        Parameters
        ----------
        pdf_fn      :   string
                        name of the PDF file to be created.

        """

        self.__pdf_fn = pdf_fn
        self.__canv = canvas.Canvas(pdf_fn)
        self.__font_name = None
        self.__font_size = None
        self.__header_str = None
        self.__footer_str = None

        self.__lines_per_page = 72
        self.__hdr_lines = 3
        self.__ftr_lines = 3

        self.__body_lines = self.__lines_per_page - self.__hdr_lines - self.__ftr_lines

        self.__x = 0.25 * inch
        self.__top_y = 11.0 * inch
        self.__y = self.__top_y
        self.__dy = 0.125 * inch

        self.__line_ctr = 0
        self.__page_saved = 0
        self.__page_num = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def setFont(self, font_name, font_size):
        self.__font_name = font_name
        self.__font_size = font_size
        self.__resetFont()

    def __resetFont(self):
        self.__canv.setFont(self.__font_name, self.__font_size)

    def setHeader(self, header_str):
        self.__header_str = header_str

    def setFooter(self, footer_str):
        self.__footer_str = footer_str

    def writeLine(self, lin):
        if self.__line_ctr == 0:
            self.__beginPage()

        self.__writeLine(lin)
        self.__line_ctr += 1

        if self.__line_ctr >= self.__body_lines:
            self.__endPage()

    def __writeLine(self, lin):
        self.__page_saved = 0
        self.__canv.drawString(self.__x, self.__y, lin)
        self.__y = self.__y - self.__dy

    def __beginPage(self):
        self.__page_num += 1
        self.__y = self.__top_y
        self.__resetFont()
        self.__writeHeader()

    def __endPage(self):
        if self.__line_ctr < self.__body_lines:
            lines_remaining = self.__body_lines - self.__line_ctr
            self.__y = self.__y - (self.__dy * lines_remaining)
        self.__writeFooter()
        if not self.__page_saved:
            self.__canv.save()
            self.__page_saved = 1
            self.__line_ctr = 0

    def savePage(self):
        self.__endPage()

    def __writeHeader(self):
        if self.__header_str == None or self.__header_str == "":
            return
        hdr_lin = self.__header_str + str.rjust("Page: " + str(self.__page_num), 20)
        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, hdr_lin)
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__page_saved = 0

    def __writeFooter(self):
        if self.__footer_str == None or self.__footer_str == "":
            return

        ftr_lin = self.__footer_str + str.rjust("Page: " + str(self.__page_num), 20)

        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, ftr_lin)
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__page_saved = 0

    def close(self):
        if not self.__page_saved:
            self.savePage()
