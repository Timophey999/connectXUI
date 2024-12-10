# asynxui

`asynxui` - это пакет Python для взаимодействия с API XUI, предназначенный для управления входящими соединениями и клиентами.

## Установка

Установить пакет можно с помощью pip:

```bash
pip install xui_api
```

## Использование

```python
from xui_api import Async3xui


async def main():
    api = Async3xui(
        host="http://example.com",
        username="user",
        password="pass"
    )
    await api.login()
    # Примеры взаимодействия с API

```

## Вклад

Если вы хотите внести вклад, пожалуйста, создайте pull request или сообщите о проблеме.