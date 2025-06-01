# Сервис прогноза погоды по названию города

Сервис показывает текущую погоду для выбранного города, а также на следующие 7 дней.
Городов с одним и тем же названием может быть много, сервис пока работает только для самого известного города.
Сервис хранит историю просмотра городов.


## Подготовка проекта

Для работы сервиса требуются:

- Python версии не ниже 3.10.
- установленное ПО для контейнеризации - [Docker](https://docs.docker.com/engine/install/).

## Запуск

Для запуска используйте следующую команду из пути, где находится файл docker-compose.yml
  ```shell
   docker-compose up
   
   ```
Выполните миграции
  ```shell
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

Для создания суперпользователя:
  ```shell
   docker-compose exec web python manage.py createcuperuser
   ```

