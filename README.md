# Запуск проекта локально в Docker
В системе должнен быть установлены Docker актуальной версии!


### 1.Собираем и запускаем проект
```bash
docker compose up -d
```
### 2.Заполняем БД из дампа dump1.sql дамп можно перезаписать но лучше изменить название
```bash
docker exec -i automation_cabinet-postgres-1 psql -U postgres -d postgres < dump1.sql
```
### Чтобы остановить контейнеры, нужно выполнить
```bash
docker compose stop
```
### Чтобы удалить контейнеры, нужно выполнить
```bash
docker compose down
```
### Чтобы провести миграции в бд 
```bash
docker exec -it automation_cabinet-automation_cabinet-1 python manage.py migrate
```

### Если вы добавили что-то в бд то сохраните дамп:
```bash
docker exec -i automation_cabinet-postgres-1 pg_dump -U postgres -d postgres > dump1.sql
```