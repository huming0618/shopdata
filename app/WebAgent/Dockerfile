FROM python:3
COPY . .
RUN pip install requests
RUN pip install pytesseract
RUN pip install PyExecJS

CMD [ "python", "./WebAgent.py" ]