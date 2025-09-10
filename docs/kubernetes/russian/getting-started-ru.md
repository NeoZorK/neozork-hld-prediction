# Начало работы с Kubernetes - Русский

Это руководство поможет вам начать работу с развертыванием проекта Neozork HLD Prediction на Kubernetes.

## Предварительные требования

### Системные требования
- Кластер Kubernetes (версия 1.20 или выше)
- Настроенный инструмент командной строки kubectl
- Docker образы, собранные и доступные в реестре контейнеров
- Минимум 4 ядра CPU и 8GB RAM для кластера

### Необходимые инструменты
```bash
# Установка kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Проверка установки
kubectl version --client
```

### Доступ к кластеру
Убедитесь, что ваш kubectl настроен для доступа к кластеру Kubernetes:
```bash
# Проверка подключения к кластеру
kubectl cluster-info

# Проверка возможности листинга узлов
kubectl get nodes
```

## Быстрый старт

### 1. Сборка и отправка Docker образов

Сначала соберите Docker образы для вашей платформы:

```bash
# Для Apple Silicon (ARM64)
docker build -f Dockerfile.apple -t neozork-interactive:apple-latest .

# Для x86 (AMD64)
docker build -f Dockerfile -t neozork-interactive:latest .

# Отправка в ваш реестр (замените на ваш реестр)
docker tag neozork-interactive:apple-latest your-registry/neozork-interactive:apple-latest
docker tag neozork-interactive:latest your-registry/neozork-interactive:latest

docker push your-registry/neozork-interactive:apple-latest
docker push your-registry/neozork-interactive:latest
```

### 2. Развертывание в Kubernetes

Примените манифесты Kubernetes:

```bash
# Развертывание приложения
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Проверка статуса развертывания
kubectl get deployments
kubectl get pods -l app=neozork-interactive
kubectl get services
```

### 3. Проверка развертывания

Убедитесь, что все компоненты работают:

```bash
# Проверка статуса подов
kubectl get pods -l app=neozork-interactive

# Проверка конечных точек сервиса
kubectl get endpoints

# Просмотр логов подов
kubectl logs -l app=neozork-interactive --tail=50
```

### 4. Доступ к приложению

Перенаправление портов для локального доступа к приложению:

```bash
# Перенаправление порта 8080 на сервис
kubectl port-forward service/neozork-interactive-service 8080:80

# Доступ к приложению
curl http://localhost:8080/health
```

## Конфигурация

### Переменные окружения

Развертывание использует несколько переменных окружения, которые можно настроить:

- `PYTHONPATH`: Установлено в "/app" для правильного разрешения Python модулей
- `APPLE_SILICON`: Установлено в "true" для оптимизаций Apple Silicon
- `MLX_ENABLED`: Включение фреймворка MLX для Apple Silicon

### Требования к ресурсам

Развертывание включает запросы и ограничения ресурсов:

**Apple Silicon:**
- CPU: запрос 1000m, лимит 2000m
- Память: запрос 2Gi, лимит 4Gi

**x86:**
- CPU: запрос 500m, лимит 1000m
- Память: запрос 1Gi, лимит 2Gi

### Постоянные тома

Развертывание создает четыре запроса на постоянные тома:

1. **Том данных** (10Gi): Хранилище данных приложения
2. **Том логов** (5Gi): Логи приложения
3. **Том графиков** (5Gi): Сгенерированные графики и диаграммы
4. **Том результатов** (10Gi): Результаты анализа

## Проверки здоровья

Развертывание включает комплексные проверки здоровья:

### Проверка жизнеспособности
- **Путь**: `/health`
- **Порт**: 8080
- **Начальная задержка**: 30 секунд
- **Период**: 10 секунд

### Проверка готовности
- **Путь**: `/ready`
- **Порт**: 8080
- **Начальная задержка**: 5 секунд
- **Период**: 5 секунд

## Конфигурация сервиса

Развертывание создает сервис LoadBalancer, который:
- Предоставляет приложение на порту 80
- Направляет трафик на порт контейнера 8080
- Обеспечивает внешний доступ к приложению

## Следующие шаги

После успешного развертывания:

1. **Настройка мониторинга**: Настройка Prometheus и Grafana для наблюдаемости
2. **Настройка Ingress**: Конфигурация внешнего доступа с SSL/TLS
3. **Масштабирование приложения**: Настройка количества реплик в зависимости от нагрузки
4. **Стратегия резервного копирования**: Реализация резервного копирования данных для постоянных томов

## Устранение неполадок

### Частые проблемы

**Поды не запускаются:**
```bash
# Проверка событий пода
kubectl describe pod <pod-name>

# Проверка логов пода
kubectl logs <pod-name>
```

**Сервис недоступен:**
```bash
# Проверка конечных точек сервиса
kubectl get endpoints

# Проверка конфигурации сервиса
kubectl describe service neozork-interactive-service
```

**Проблемы с постоянными томами:**
```bash
# Проверка статуса PVC
kubectl get pvc

# Проверка статуса PV
kubectl get pv
```

### Получение помощи

- Ознакомьтесь с [Руководством по устранению неполадок](./troubleshooting-ru.md) для подробных решений
- Изучите [Справочник конфигурации](./configuration-reference-ru.md) для всех опций
- Откройте issue в репозитории проекта для получения поддержки
