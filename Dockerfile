FROM python:3.10-slim

ENV URI_RCV="${URI_RCV}"
ENV URI_SEND="${URI_SEND}"
ENV SIZE_CHUNK="${SIZE_CHUNK}"
ENV KEY_FIELD="${KEY_FIELD}"

WORKDIR /app
COPY ws_message_sorter.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "ws_message_sorter.py"]