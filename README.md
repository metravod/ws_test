### Вебсокет-клиент для ретрансляции отсортированных сообщений

Клиент подключается к вебсокету, который направляет данные в реальном времени, собирает 
определённое количество сообщений в один кусок, сортирует его по указанному полю и направляет
в другой вебсокет.

#### Ожидаемый формат данных
```python
{"id": int, "text": int}
```

#### Настройка
URI вебсокетов, размер chunk'а данных и ключевое поле для сортировки указываются в файле **settings**

#### Запуск
```commandline
docker build -t 'ws' . 
docker run -d 'ws'
```
