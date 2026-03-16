FROM python:3.11-slim

WORKDIR /app

COPY students_part_1/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY students_part_1/ .

CMD ["python","simulator.py"]