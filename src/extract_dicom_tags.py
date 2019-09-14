
import sys
import pydicom
import json

tag = sys.argv[1]
inputfile = sys.argv[2]



# https://github.com/pydicom/pydicom/issues/319

def dicom_dataset_to_dict(dicom_header):
    dicom_dict = {}
    repr(dicom_header)
    for dicom_value in dicom_header.values():
        if dicom_value.tag == (0x7fe0, 0x0010):
            # discard pixel data
            continue
        if type(dicom_value.value) == pydicom.dataset.Dataset:
            dicom_dict[dicom_value.keyword] = dicom_dataset_to_dict(dicom_value.value)
        else:
            v = _convert_value(dicom_value.value)
            dicom_dict[dicom_value.keyword] = v
    return dicom_dict

def _sanitise_unicode(s):
    return s.replace(u"\u0000", "").strip()


def _convert_value(v):
    t = type(v)
    if t in (list, int, float):
        cv = v
    elif t == str:
        cv = _sanitise_unicode(v)
    elif t == bytes:
        s = v.decode('ascii', 'replace')
        cv = _sanitise_unicode(s)
    elif t == pydicom.valuerep.DSfloat:
        cv = float(v)
    elif t == pydicom.valuerep.IS:
        cv = int(v)
    elif t == pydicom.valuerep.PersonName3:
        cv = str(v)
    else:
        cv = repr(v)
    return cv

def dictify(ds):
    """Turn a pydicom Dataset into a dict with keys derived from the Element tags.

    Parameters
    ----------
    ds : pydicom.dataset.Dataset
        The Dataset to dictify

    Returns
    -------
    output : dict
    """
    output = dict()
    for elem in ds:
        if elem.VR != 'SQ':
            output[elem.name] = elem.value
        else:
            output[elem.name] = [dictify(item) for item in elem]
    return output

ds = pydicom.read_file(inputfile)

if tag == '--':
    # dict = dictify(ds)
    dict = dicom_dataset_to_dict(ds)
    js = json.dumps(dict)
    print(js)
if tag in ds:
    print(ds.data_element(tag).value)
else:
    print("")
