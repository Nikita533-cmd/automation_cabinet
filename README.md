# Запуск проекта локально в Docker
В системе должнен быть установлены Docker актуальной версии!


<!-- ### 1. Клонируем себе репозиторий
```bash
git clone git@github.com:SamoilenkoLev/spec-auto.git
cd spec-auto
``` -->

### 2. Линтим docker-compose.yml с docker-compose.dev.yml

```bash
ln -s etc/docker-compose.yaml ./
```

### 3.Собираем и запускаем проект
```bash
./run.sh start
```

### 4. Миграции
```bash

### 4.1 Заполнение БД
```bash

docker exec -i automation_cabinet-postgres-1 psql -U postgres -d postgres < dump1.sql
```

### 5.Запуск дев сервера
```bash
./run.sh runserver
```

Чтобы остановить контейнеры, нужно выполнить
```bash
./run.sh stop
```
Если вы добавили что-то в бд то сохраните дамп:
docker exec -i automation_cabinet-postgres-1 pg_dump -U postgres -d postgres > dump1.sql