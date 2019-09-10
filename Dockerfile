FROM python:3.6.9-alpine

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

ENTRYPOINT ["python3", "extract_dicom_tags.py" ]
CMD ["", "/input/input.dcm"]
