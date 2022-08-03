##############################################################
# A simple script to combine multiple PDFs into one.         #
#                                                            #
# @author: Tyler Horoho                                      #
# Created 18 July 2022                                       #
##############################################################

from PyPDF2 import PdfMerger

merger = PdfMerger()

for feb in range(2):
    for ch in range(64):
        merger.append('smallrun/smallrun_feb{0}_ch{1}.pdf'.format(feb, ch))

merger.write("smallrun.pdf")
merger.close()
