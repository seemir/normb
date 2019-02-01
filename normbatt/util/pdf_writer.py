# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


class PDFWriter:
    """
    A class to provide an API for writing lines of plain text
    to a PDF file.

    """

    def __init__(self, file_name='NormalityReport.pdf', file_dir='reports/'):
        """

        Parameters
        ----------
        pdf_fn      :   string
                        name of the PDF file to be created.

        """
        self.__canv = canvas.Canvas(file_dir + file_name)
        self.__font_name = None
        self.__font_size = None
        self.__header_str = None
        self.__footer_str = None
        self.__lines_per_page = 80
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

    def set_font(self, font_name, font_size):
        """
        Set the font name and size

        Parameters
        ----------
        font_name   : str
                      name of font
        font_size   : int, float
                      size of font

        """
        self.__font_name = font_name
        self.__font_size = font_size
        self.__reset_font()

    def __reset_font(self):
        """
        Method that reset the font name and size selected

        """
        self.__canv.setFont(self.__font_name, self.__font_size)

    def set_header(self, header_str):
        """
        Set the name to be displayed on the header of the pdf

        Parameters
        ----------
        header_str  : str
                      header name

        """
        self.__header_str = header_str

    def set_footer(self, footer_str):
        """
        Set the name to be displayed on the footer of the pdf

        Parameters
        ----------
        footer_str  : str
                      footer name

        """
        self.__footer_str = footer_str

    def write_line(self, line):
        """
        Write a line of text, "line", to the PDF file. Take care of doing a next page
        (footer/header) if needed - using __endPage() / __beginPage(). Update the line counter.
        Call __writeLine() to actually write the line.

        Parameters
        ----------
        line    : str
                  line of text

        """
        if self.__line_ctr == 0:
            self.__begin_page()

        self.__write_line(line)
        self.__line_ctr += 1

        if self.__line_ctr >= self.__body_lines:
            self.__end_page()

    def __write_line(self, line):
        """

        Parameters
        ----------
        line     : str
                   line fof text to be written

        """
        self.__page_saved = 0
        self.__canv.drawString(self.__x, self.__y, line)
        self.__y = self.__y - self.__dy

    def __begin_page(self):
        """"
        Do stuff to the begin of a new page.

        """
        self.__page_num += 1
        self.__y = self.__top_y
        self.__reset_font()
        self.__write_header()

    def __end_page(self):
        """
        Do stuff to the end and save the current page.

        """
        if self.__line_ctr < self.__body_lines:
            lines_remaining = self.__body_lines - self.__line_ctr
            self.__y = self.__y - (self.__dy * lines_remaining)
        self.__write_footer()
        if not self.__page_saved:
            self.__canv.save()
            self.__page_saved = 1
            self.__line_ctr = 0

    def save_page(self):
        """
        Save page.

        """
        self.__end_page()

    def __write_header(self):
        """
        Write page header

        """
        if self.__header_str is None or self.__header_str == "":
            return
        hdr_lin = self.__header_str
        aut_lin = 'Author: Samir Adrik'
        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, hdr_lin)
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, aut_lin)
        self.__y = self.__y - self.__dy
        self.__page_saved = 0

    def __write_footer(self):
        """
        Write page footer

        """
        if self.__footer_str is None or self.__footer_str == "":
            return

        ftr_lin = self.__footer_str + str.rjust("Page: " + str(self.__page_num), 45)

        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, ftr_lin)
        self.__y = self.__y - self.__dy
        self.__canv.drawString(self.__x, self.__y, "")
        self.__y = self.__y - self.__dy
        self.__page_saved = 0

    def close(self):
        """
        Print footer of last page, if not already printed. Save the page.

        """
        if not self.__page_saved:
            self.save_page()
