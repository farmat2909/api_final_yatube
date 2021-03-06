### API_Yatube

API данного проекта позволяет читать посты разных групп, создавать собственные посты, а так же подписываться на других авторов.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:farmat2909/api_final_yatube.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Документацию API и примеры выполнения запросов можно посмотреть по адресу:

```
http://127.0.0.1:8000/redoc/
```
