# inventory_api

Тестовое задание. Разработка API для управления складом
## Запуск
- склонируйте репозиторий
```bash
    git clone https://github.com/Dzhegutin/inventory_api.git
```
- в корне проекта создайте файл ".env" и пропишите необходимые настройки для подключение к Postgres
```bash
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASS=your_db_password
    TEST_DB_NAME=your_test_db_name
    DB_URL=postgresql+asyncpg://your_db_user:your_db_password@db:5432/your_db_name
    DB_TEST_URL=postgresql+asyncpg://your_db_user:your_db_password@db:5432/your_test_db_name
```
- выполните команды (должен быть запущен Docker):
```bash
#добавить в файл alembic.ini подключение к БД
sqlalchemy.url = postgresql+asyncpg://your_db_user:your_db_password@db:5432/your_db_name
# смонтировать контейнер и запустить контейнер:
docker-compose up --build -d
# остановить контейнер (по необходимости):
docker-compose down
#просмотреть созданные контейнеры
docker-compose ps
# подключиться к контейнеру с postgres
docker exec -it <container_name> psql -U your_db_user
#создать базу данных для тестов
CREATE DATABASE your_test_db_name;
#убедиться в создании бд для тестов
\l
#отключиться от бд
\q
# если в код были внесены изменения, необходимо заново смонтировать контейнер
```

## Миграции
Команды выполняются при запущенном контейнере
```bash
#инициализация alembic (по необходимости)
docker exec -it inventory_api-web-1 alembic init alembic
# создание миграций
docker exec -it <container_name> alembic revision --autogenerate -m "your comment"
# применение миграций
docker exec -it <container_name> alembic upgrade head
#запуск тестов
docker-compose up tests 

```
