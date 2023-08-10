FROM python:3.10-slim
RUN mkdir -p /usr/src/ws_message_sorter
WORKDIR /usr/src/ws_message_sorter
COPY . /usr/src/ws_message_sorter
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "ws_message_sorter.py"]