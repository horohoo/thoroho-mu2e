##############################################################
# A simple script to combine multiple PDFs into one.         #
#                                                            #
# @author: Tyler Horoho                                      #
# Created 18 July 2022                                       #
##############################################################

from PyPDF2 import PdfMerger

merger1 = PdfMerger()

for feb in range(2):
    for ch in range(64):
        merger1.append('smallrun/PEvstemp_feb{0}_ch{1}.pdf'.format(feb, ch))

merger1.write("PEvstemp.pdf")
merger1.close()

merger2 = PdfMerger()

for feb in range(2):
    for ch in range(64):
        merger2.append('smallrun/smallrun_feb{0}_ch{1}.pdf'.format(feb, ch))

merger2.write("smallrun.pdf")
merger2.close()
