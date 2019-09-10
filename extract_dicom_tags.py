
import pydicom
import sys

tag = sys.argv[1]
inputfile = sys.argv[2]

ds = pydicom.read_file(inputfile)
if tag in ds:
    print(ds.data_element(tag).value)
