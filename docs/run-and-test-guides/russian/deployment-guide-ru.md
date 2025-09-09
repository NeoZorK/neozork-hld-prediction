# Руководство по развертыванию - NeoZork HLD Prediction

## 🚀 Обзор развертывания

Система NeoZork HLD Prediction поддерживает различные варианты развертывания:
- Локальное развертывание
- Docker контейнеры
- Apple Silicon нативные контейнеры
- Kubernetes кластеры
- Продакшн развертывание

## 🏠 Локальное развертывание

### Установка и настройка
```bash
# Клонирование репозитория
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Установка зависимостей
uv pip install -r requirements.txt

# Настройка окружения
cp env.example .env
nano .env
```

### Запуск сервисов
```bash
# SaaS платформа
uv run python run_saas.py

# Pocket Hedge Fund
uv run python run_pocket_hedge_fund.py

# Мониторинг
uv run python -m src.monitoring.system_monitor
```

## 🐳 Docker развертывание

### Docker Compose
```bash
# Запуск всех сервисов
docker-compose up -d

# Запуск с логированием
docker-compose up

# Остановка
docker-compose down
```

### Управление сервисами
```bash
# Перезапуск сервисов
docker-compose restart

# Просмотр логов
docker-compose logs -f neozork-hld

# Выполнение команд в контейнере
docker-compose exec neozork-hld bash
```

### Продакшн Docker
```bash
# Запуск продакшн сервисов
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

## 🍎 Apple Silicon нативные контейнеры

### Настройка нативного контейнера
```bash
# Интерактивный запуск
./scripts/native-container/native-container.sh

# Быстрый запуск
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Проверка статуса
./scripts/native-container/run.sh --status
```

### Управление нативным контейнером
```bash
# Остановка
./scripts/native-container/stop.sh

# Принудительный перезапуск
./scripts/native-container/force_restart.sh

# Очистка
./scripts/native-container/cleanup.sh --all --force

# Просмотр логов
./scripts/native-container/logs.sh
```

## ☸️ Kubernetes развертывание

### Применение манифестов
```bash
# Применение всех манифестов
kubectl apply -f k8s/

# Применение конкретного манифеста
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Проверка статуса
kubectl get pods
kubectl get services
kubectl get deployments
```

### Управление развертыванием
```bash
# Масштабирование
kubectl scale deployment neozork-app --replicas=3

# Обновление образа
kubectl set image deployment/neozork-app neozork-app=neozork:latest

# Откат
kubectl rollout undo deployment/neozork-app

# Просмотр статуса
kubectl rollout status deployment/neozork-app
```

## 🏭 Продакшн развертывание

### Настройка продакшн окружения
```bash
# Настройка продакшн конфигурации
python deploy/production_setup.py

# Проверка конфигурации
python deploy/production_setup.py --validate

# Создание продакшн окружения
python deploy/production_setup.py --create
```

### Продакшн контейнеры
```bash
# Запуск продакшн сервисов
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
```

### Мониторинг продакшна
```bash
# Health check
curl http://localhost:8080/health

# Prometheus метрики
curl http://localhost:9090/metrics

# Статус сервисов
kubectl get pods -o wide
```

## 🔧 Конфигурация

### Переменные окружения
```bash
# Основные настройки
export HOST=0.0.0.0
export PORT=8080
export DEBUG=false

# Настройки базы данных
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=neozork_fund
export DB_USER=neozork_user
export DB_PASSWORD=neozork_password

# JWT настройки
export JWT_SECRET=your-secret-key-change-in-production
```

### Конфигурационные файлы
```bash
# Docker конфигурация
docker-compose.yml
docker-compose.prod.yml
docker-compose.apple.yml

# Kubernetes манифесты
k8s/neozork-apple-deployment.yaml

# Продакшн настройки
deploy/production_setup.py
```

## 📊 Мониторинг и логи

### Просмотр логов
```bash
# Логи приложения
tail -f logs/pocket_hedge_fund.log
tail -f logs/saas_platform.log

# Docker логи
docker-compose logs -f neozork-hld

# Kubernetes логи
kubectl logs -f deployment/neozork-app
```

### Мониторинг системы
```bash
# Prometheus метрики
curl http://localhost:9090/metrics

# Health check
curl http://localhost:8080/health

# Статус сервисов
kubectl get pods
kubectl get services
```

## 🛠️ Обслуживание

### Обновление системы
```bash
# Обновление кода
git pull origin main

# Обновление зависимостей
uv pip install --upgrade -r requirements.txt

# Пересборка контейнеров
docker-compose build --no-cache

# Перезапуск сервисов
docker-compose restart
```

### Резервное копирование
```bash
# Резервное копирование данных
docker-compose exec neozork-hld pg_dump -U neozork_user neozork_fund > backup.sql

# Резервное копирование конфигурации
tar -czf config-backup.tar.gz .env docker-compose.yml k8s/
```

### Восстановление
```bash
# Восстановление данных
docker-compose exec neozork-hld psql -U neozork_user neozork_fund < backup.sql

# Восстановление конфигурации
tar -xzf config-backup.tar.gz
```

## 🆘 Устранение неполадок

### Частые проблемы
1. **Проблемы с портами**: Проверьте, что порты 8080, 3000, 9090 свободны
2. **Проблемы с Docker**: `docker system prune -a`
3. **Проблемы с Kubernetes**: `kubectl get events`
4. **Проблемы с базой данных**: Проверьте подключение к PostgreSQL

### Отладочные команды
```bash
# Проверка статуса Docker
docker-compose ps
docker images
docker volume ls

# Проверка статуса Kubernetes
kubectl get pods
kubectl get services
kubectl describe pod <pod-name>

# Проверка логов
docker-compose logs neozork-hld
kubectl logs <pod-name>
```

## 📚 Дополнительные ресурсы

- [Полное руководство](complete-manual-ru.md)
- [Быстрый старт](quick-start-ru.md)
- [Руководство по тестированию](testing-guide-ru.md)
