# Руководство по Production Deployment - Русский

## Обзор

Это подробное руководство покрывает production deployment для системы NeoZork HLD Prediction, включая множественные стратегии развертывания, мониторинг и лучшие практики.

## Содержание

1. [Предварительные требования](#предварительные-требования)
2. [Варианты развертывания](#варианты-развертывания)
3. [Docker развертывание](#docker-развертывание)
4. [Kubernetes развертывание](#kubernetes-развертывание)
5. [Управление конфигурацией](#управление-конфигурацией)
6. [Мониторинг и логирование](#мониторинг-и-логирование)
7. [Конфигурация безопасности](#конфигурация-безопасности)
8. [Резервное копирование и восстановление](#резервное-копирование-и-восстановление)
9. [Устранение неполадок](#устранение-неполадок)
10. [Лучшие практики](#лучшие-практики)

## Предварительные требования

### Системные требования

- **Операционная система**: Linux (Ubuntu 20.04+), macOS (Apple Silicon), или Windows с WSL2
- **Память**: Минимум 4GB RAM, рекомендуется 8GB+ RAM
- **Хранилище**: Минимум 20GB свободного места
- **CPU**: Рекомендуется 2+ ядра

### Программные зависимости

- **Docker**: Версия 20.10+
- **Docker Compose**: Версия 2.0+
- **Kubernetes**: Версия 1.20+ (для K8s развертывания)
- **Python**: Версия 3.11+ (для нативного развертывания)
- **UV Package Manager**: Последняя версия
- **PostgreSQL**: Версия 15+ (если не используется контейнеризированная версия)
- **Redis**: Версия 7+ (если не используется контейнеризированная версия)

### Сетевые требования

- **Порты**: 80, 443, 8000, 5432, 6379, 9090, 3000
- **SSL сертификаты**: Действующие SSL сертификаты для HTTPS
- **Домен**: Настроенное доменное имя для production доступа

## Варианты развертывания

### 1. Docker Compose развертывание (Рекомендуется для малого-среднего масштаба)

#### Быстрый старт

```bash
# Клонировать репозиторий
git clone <repository-url>
cd neozork-hld-prediction

# Копировать конфигурацию окружения
cp deployment/pocket_hedge_fund/env.prod.example .env.prod

# Редактировать переменные окружения
nano .env.prod

# Запустить production сервисы
docker-compose -f deployment/pocket_hedge_fund/docker-compose.prod.yml up -d
```

#### Включенные сервисы

| Сервис | Порт | Описание |
|---------|------|-------------|
| **API** | 8000 | FastAPI приложение |
| **PostgreSQL** | 5432 | Основная база данных |
| **Redis** | 6379 | Кэширование и сессии |
| **Nginx** | 80/443 | Обратный прокси и SSL терминация |
| **Prometheus** | 9090 | Сбор метрик |
| **Grafana** | 3000 | Дашборды мониторинга |

### 2. Kubernetes развертывание (Рекомендуется для крупного масштаба)

#### Предварительные требования

- Kubernetes кластер (1.20+)
- kubectl настроен
- Helm (опционально, для управления пакетами)

#### Шаги развертывания

```bash
# Применить Kubernetes манифесты
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Проверить статус развертывания
kubectl get pods -l app=neozork-interactive

# Доступ к сервисам
kubectl port-forward service/neozork-interactive-service 8080:80
```

#### Возможности

- **Автомасштабирование**: Horizontal Pod Autoscaler (HPA)
- **Балансировка нагрузки**: Kubernetes Service с LoadBalancer
- **Постоянное хранилище**: PVC для данных, логов и результатов
- **Проверки здоровья**: Liveness и readiness пробы
- **Управление ресурсами**: Ограничения CPU и памяти

### 3. Apple Silicon Native Container (только macOS)

#### Предварительные требования

- Apple Silicon Mac (M1/M2/M3)
- Установленный container runtime
- UV package manager

#### Развертывание

```bash
# Запустить скрипт развертывания
./scripts/deploy_apple_container.sh

# Доступ к приложению
open http://localhost:8080
```

#### Преимущества производительности

- **На 30-50% быстрее** чем Docker на Apple Silicon
- **Нативная поддержка MLX** для ускорения машинного обучения
- **Оптимизированное использование памяти** для архитектуры Apple Silicon

## Управление конфигурацией

### Переменные окружения

#### Обязательные переменные

```bash
# Конфигурация базы данных
POSTGRES_PASSWORD=your_secure_postgres_password_here
DATABASE_URL=postgresql://phf_user:password@postgres:5432/pocket_hedge_fund

# Конфигурация Redis
REDIS_PASSWORD=your_secure_redis_password_here
REDIS_URL=redis://:password@redis:6379/0

# JWT безопасность
JWT_SECRET_KEY=your_very_secure_jwt_secret_key_here_minimum_32_characters

# Конфигурация API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Окружение
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Опциональные переменные

```bash
# Конфигурация CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Ограничение скорости
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Мониторинг
GRAFANA_PASSWORD=your_secure_grafana_password_here

# Конфигурация SSL
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### Файлы конфигурации

#### Production конфигурация (`deployment/production/config.yaml`)

```yaml
# Системная конфигурация
system:
  id: "neozork-pocket-hedge-fund"
  version: "1.0.0"
  environment: "production"
  debug_mode: false
  log_level: "INFO"
  max_workers: 8

# Конфигурация базы данных
database:
  type: "postgresql"
  host: "postgres"
  port: 5432
  database: "neozork_hld_prediction"
  username: "neozork"
  password: "${POSTGRES_PASSWORD}"
  pool_size: 20
  max_overflow: 30

# Конфигурация безопасности
security:
  ssl:
    enabled: true
    cert_path: "/etc/ssl/certs/neozork.crt"
    key_path: "/etc/ssl/private/neozork.key"
  firewall:
    enabled: true
    allowed_ports: [80, 443, 8000]
```

## Мониторинг и логирование

### Prometheus метрики

#### Ключевые метрики

- **Метрики приложения**: Скорость запросов, время отклика, частота ошибок
- **Метрики базы данных**: Пул соединений, производительность запросов
- **Системные метрики**: CPU, использование памяти, использование диска
- **Бизнес метрики**: Торговые сигналы, точность прогнозов

#### Конфигурация

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'neozork-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

### Grafana дашборды

#### Предварительно настроенные дашборды

1. **Обзор системы**: CPU, память, использование диска
2. **Производительность приложения**: Метрики запросов, времена отклика
3. **Производительность базы данных**: Пулы соединений, времена запросов
4. **Бизнес метрики**: Торговые сигналы, прогнозы

#### Доступ

- **URL**: http://localhost:3000
- **Имя пользователя**: admin
- **Пароль**: Устанавливается через переменную окружения `GRAFANA_PASSWORD`

### Конфигурация логирования

#### Уровни логов

- **DEBUG**: Подробная информация для отладки
- **INFO**: Общая информация о потоке приложения
- **WARNING**: Предупреждающие сообщения о потенциальных проблемах
- **ERROR**: Сообщения об ошибках для неудачных операций
- **CRITICAL**: Критические ошибки, которые могут вызвать сбой приложения

#### Форматы логов

```python
# JSON формат для production
LOG_FORMAT = "json"

# Пример структурированного логирования
{
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "INFO",
    "service": "neozork-api",
    "message": "Request processed",
    "request_id": "req-123",
    "duration_ms": 150
}
```

## Конфигурация безопасности

### SSL/TLS конфигурация

#### Настройка Nginx SSL

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Аутентификация и авторизация

#### JWT конфигурация

```python
# JWT настройки
JWT_SECRET_KEY = "your-very-secure-secret-key"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
```

#### Ограничение скорости

```python
# Конфигурация ограничения скорости
RATE_LIMIT_REQUESTS = 100  # запросов в минуту
RATE_LIMIT_WINDOW = 60     # временное окно в секундах
```

### Заголовки безопасности

```python
# Заголовки безопасности
SECURE_HEADERS = True
HSTS_MAX_AGE = 31536000  # 1 год
CONTENT_SECURITY_POLICY = "default-src 'self'"
```

## Резервное копирование и восстановление

### Резервное копирование базы данных

#### Автоматизированный скрипт резервного копирования

```bash
#!/bin/bash
# Скрипт резервного копирования базы данных

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="neozork_backup_${DATE}.sql"

# Создать резервную копию
docker exec neozork-postgres pg_dump -U neozork neozork_hld_prediction > "${BACKUP_DIR}/${BACKUP_FILE}"

# Сжать резервную копию
gzip "${BACKUP_DIR}/${BACKUP_FILE}"

# Удалить старые резервные копии (хранить 30 дней)
find "${BACKUP_DIR}" -name "neozork_backup_*.sql.gz" -mtime +30 -delete
```

#### Расписание резервного копирования

```bash
# Добавить в crontab для ежедневного резервного копирования в 2:00
0 2 * * * /path/to/backup_script.sh
```

### Резервное копирование данных приложения

#### Стратегия резервного копирования

1. **База данных**: Ежедневные автоматизированные резервные копии
2. **Логи приложения**: Еженедельная ротация и архивирование
3. **Конфигурация**: Версионирование в Git
4. **Пользовательские данные**: Репликация в реальном времени на вторичное хранилище

### Процедуры восстановления

#### Восстановление базы данных

```bash
# Восстановить из резервной копии
gunzip -c backup_file.sql.gz | docker exec -i neozork-postgres psql -U neozork neozork_hld_prediction
```

#### Восстановление приложения

```bash
# Перезапустить сервисы
docker-compose -f deployment/pocket_hedge_fund/docker-compose.prod.yml restart

# Проверить здоровье сервисов
docker-compose -f deployment/pocket_hedge_fund/docker-compose.prod.yml ps
```

## Устранение неполадок

### Распространенные проблемы

#### 1. Проблемы с подключением к базе данных

**Симптомы**: Приложение не запускается, ошибки подключения к базе данных

**Решения**:
```bash
# Проверить статус базы данных
docker-compose logs postgres

# Проверить подключение к базе данных
docker exec -it neozork-postgres psql -U neozork -d neozork_hld_prediction

# Перезапустить сервис базы данных
docker-compose restart postgres
```

#### 2. Проблемы с памятью

**Симптомы**: Сбои приложения, ошибки нехватки памяти

**Решения**:
```bash
# Проверить использование памяти
docker stats

# Увеличить лимиты памяти в docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 1G
```

#### 3. Проблемы с SSL сертификатами

**Симптомы**: HTTPS не работает, ошибки сертификатов

**Решения**:
```bash
# Проверить файлы сертификатов
ls -la /etc/nginx/ssl/

# Проверить действительность сертификата
openssl x509 -in cert.pem -text -noout

# Перезапустить nginx
docker-compose restart nginx
```

### Проверки здоровья

#### Проверка здоровья приложения

```bash
# Проверить здоровье приложения
curl -f http://localhost:8000/health

# Проверить все сервисы
docker-compose ps
```

#### Проверка здоровья базы данных

```bash
# Проверить здоровье базы данных
docker exec neozork-postgres pg_isready -U neozork -d neozork_hld_prediction
```

### Анализ логов

#### Просмотр логов приложения

```bash
# Просмотр последних логов
docker-compose logs --tail=100 api

# Следовать логам в реальном времени
docker-compose logs -f api

# Просмотр логов конкретного сервиса
docker-compose logs postgres
```

#### Команды анализа логов

```bash
# Поиск ошибок
docker-compose logs api | grep -i error

# Подсчет вхождений ошибок
docker-compose logs api | grep -c "ERROR"

# Просмотр логов по временному диапазону
docker-compose logs --since="2024-01-15T10:00:00" api
```

## Лучшие практики

### Оптимизация производительности

#### 1. Выделение ресурсов

```yaml
# Оптимальное выделение ресурсов
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
    reservations:
      memory: 1G
      cpus: '0.5'
```

#### 2. Оптимизация базы данных

```sql
-- Запросы оптимизации базы данных
CREATE INDEX CONCURRENTLY idx_trades_timestamp ON trades(timestamp);
CREATE INDEX CONCURRENTLY idx_predictions_symbol ON predictions(symbol);
VACUUM ANALYZE;
```

#### 3. Стратегия кэширования

```python
# Конфигурация кэширования Redis
CACHE_TTL = 3600  # 1 час
SESSION_TIMEOUT = 1800  # 30 минут
MAX_CONNECTIONS = 1000
```

### Лучшие практики безопасности

#### 1. Переменные окружения

- Используйте надежные, уникальные пароли
- Регулярно меняйте секреты
- Никогда не коммитьте секреты в систему контроля версий
- Используйте конфигурации для конкретного окружения

#### 2. Сетевая безопасность

- Используйте HTTPS везде
- Реализуйте правильные правила файрвола
- Используйте VPN для административного доступа
- Регулярные обновления безопасности

#### 3. Безопасность приложения

- Регулярные обновления зависимостей
- Сканирование безопасности в CI/CD
- Валидация и санитизация входных данных
- Правильная обработка ошибок

### Лучшие практики мониторинга

#### 1. Сбор метрик

- Собирайте бизнес-метрики вместе с техническими метриками
- Настройте правильные пороги оповещений
- Используйте структурированное логирование
- Мониторьте внешние зависимости

#### 2. Оповещения

```yaml
# Пример правил оповещений
groups:
  - name: neozork-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Обнаружена высокая частота ошибок"
```

#### 3. Планирование мощности

- Мониторьте тенденции использования ресурсов
- Планируйте пики трафика
- Регулярное тестирование производительности
- Документируйте процедуры масштабирования

### Лучшие практики развертывания

#### 1. Blue-Green развертывание

```bash
# Пример blue-green развертывания
# Развернуть в green окружении
docker-compose -f docker-compose.green.yml up -d

# Тестировать green окружение
curl -f http://green.yourdomain.com/health

# Переключить трафик на green
# Обновить конфигурацию балансировщика нагрузки

# Вывести из эксплуатации blue окружение
docker-compose -f docker-compose.blue.yml down
```

#### 2. Rolling обновления

```bash
# Rolling обновление с нулевым временем простоя
docker-compose up -d --scale api=3
docker-compose up -d --no-deps api
```

#### 3. Проверки здоровья

```yaml
# Комплексные проверки здоровья
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Процедуры обслуживания

#### 1. Регулярные обновления

- Еженедельные обновления безопасности
- Ежемесячные обновления зависимостей
- Квартальные обновления основных версий
- Ежегодный обзор инфраструктуры

#### 2. Проверка резервных копий

- Еженедельные тесты восстановления резервных копий
- Ежемесячные учения по аварийному восстановлению
- Квартальный обзор стратегии резервного копирования

#### 3. Мониторинг производительности

- Ежедневный обзор метрик производительности
- Еженедельный обзор планирования мощности
- Ежемесячные возможности оптимизации

## Поддержка и ресурсы

### Документация

- [API Документация](http://localhost:8000/docs)
- [Справочник конфигурации](docs/configuration/)
- [Руководство по устранению неполадок](docs/troubleshooting/)

### Сообщество

- GitHub Issues: Сообщения об ошибках и запросы функций
- Документация: Вклад в документацию
- Обсуждения: Поддержка сообщества и обсуждения

### Профессиональная поддержка

Для корпоративной поддержки и консультационных услуг обращайтесь к команде разработки.

---

**Последнее обновление**: Январь 2024  
**Версия**: 1.0.0  
**Поддерживается**: Команда разработки NeoZork
