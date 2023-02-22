import os

from pyexcel import save_book_as


def convert(xls_file):
    filename = os.path.basename(xls_file).split(".")[0]
    dirname = os.path.dirname(xls_file)
    out = os.path.join(dirname, f"{filename}-zmieniony.xlsx")

    save_book_as(file_name=xls_file, dest_file_name=out)
