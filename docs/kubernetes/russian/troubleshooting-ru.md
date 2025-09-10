# Руководство по устранению неполадок Kubernetes - Русский

Это руководство предоставляет решения для частых проблем, возникающих при развертывании и управлении проектом Neozork HLD Prediction на Kubernetes.

## Содержание

1. [Проблемы с подами](#проблемы-с-подами)
2. [Подключение к сервису](#подключение-к-сервису)
3. [Проблемы с хранилищем](#проблемы-с-хранилищем)
4. [Ограничения ресурсов](#ограничения-ресурсов)
5. [Сетевые проблемы](#сетевые-проблемы)
6. [Проблемы конфигурации](#проблемы-конфигурации)
7. [Проблемы безопасности](#проблемы-безопасности)
8. [Мониторинг и логирование](#мониторинг-и-логирование)
9. [Платформо-специфичные проблемы](#платформо-специфичные-проблемы)
10. [Проблемы производительности](#проблемы-производительности)

## Проблемы с подами

### Поды не запускаются

**Симптомы:**
- Поды застряли в состоянии `Pending` или `ContainerCreating`
- Поды постоянно перезапускаются
- Поды не запускаются с сообщениями об ошибках

**Диагностика:**
```bash
# Проверка статуса подов
kubectl get pods -l app=neozork-interactive

# Описание пода для подробной информации
kubectl describe pod <pod-name>

# Проверка событий подов
kubectl get events --sort-by=.metadata.creationTimestamp

# Проверка логов подов
kubectl logs <pod-name> --previous
```

**Частые причины и решения:**

1. **Ошибки загрузки образа**
   ```bash
   # Проверка существования и доступности образа
   docker pull neozork-interactive:apple-latest
   
   # Проверка учетных данных реестра образов
   kubectl get secrets
   kubectl describe secret <registry-secret>
   ```

2. **Ограничения ресурсов**
   ```bash
   # Проверка ресурсов узлов
   kubectl top nodes
   kubectl describe nodes
   
   # Проверка запросов ресурсов подов против емкости узлов
   kubectl describe pod <pod-name> | grep -A 10 "Requests:"
   ```

3. **Проблемы с селектором узлов**
   ```bash
   # Проверка соответствия узлов селектору
   kubectl get nodes --show-labels
   
   # Проверка архитектуры узлов
   kubectl get nodes -o wide
   ```

### Циклы сбоев подов

**Симптомы:**
- Поды постоянно перезапускаются
- Высокий счетчик перезапусков
- Сбои приложения

**Диагностика:**
```bash
# Проверка счетчика перезапусков
kubectl get pods -l app=neozork-interactive

# Просмотр логов сбоев
kubectl logs <pod-name> --previous

# Проверка кодов выхода контейнеров
kubectl describe pod <pod-name> | grep -A 5 "Last State"
```

**Решения:**

1. **Ошибки приложения**
   ```bash
   # Проверка логов приложения
   kubectl logs <pod-name> --tail=100
   
   # Отладка с интерактивной оболочкой
   kubectl exec -it <pod-name> -- /bin/bash
   ```

2. **Проблемы конфигурации**
   ```bash
   # Проверка переменных окружения
   kubectl exec <pod-name> -- env
   
   # Проверка смонтированных томов
   kubectl exec <pod-name> -- ls -la /app/
   ```

3. **Лимиты ресурсов**
   ```bash
   # Проверка, убивается ли под из-за лимитов ресурсов
   kubectl describe pod <pod-name> | grep -A 10 "Events:"
   
   # Настройка лимитов ресурсов при необходимости
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"memory":"4Gi","cpu":"2000m"}}}]}}}}'
   ```

## Подключение к сервису

### Сервис недоступен

**Симптомы:**
- Невозможно подключиться к сервису извне кластера
- Конечные точки сервиса не найдены
- Таймауты подключения

**Диагностика:**
```bash
# Проверка статуса сервиса
kubectl get services

# Проверка конечных точек сервиса
kubectl get endpoints

# Тестирование подключения к сервису изнутри кластера
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -O- http://neozork-interactive-service:80/health
```

**Решения:**

1. **Проблемы с селектором сервиса**
   ```bash
   # Проверка соответствия селектора сервиса меткам подов
   kubectl get pods --show-labels
   kubectl describe service neozork-interactive-service
   ```

2. **Конфигурация портов**
   ```bash
   # Проверка правильности настройки портов
   kubectl describe service neozork-interactive-service
   
   # Проверка портов контейнера
   kubectl describe pod <pod-name> | grep -A 5 "Ports:"
   ```

3. **Проблемы с LoadBalancer**
   ```bash
   # Проверка статуса LoadBalancer
   kubectl get service neozork-interactive-service
   
   # Проверка назначения внешнего IP
   kubectl describe service neozork-interactive-service
   ```

### Проблемы разрешения DNS

**Симптомы:**
- Невозможно разрешить имена сервисов
- Сбои межсервисной связи

**Диагностика:**
```bash
# Тестирование разрешения DNS изнутри кластера
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup neozork-interactive-service

# Проверка статуса CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

**Решения:**
```bash
# Перезапуск CoreDNS при необходимости
kubectl delete pods -n kube-system -l k8s-app=kube-dns

# Проверка конфигурации CoreDNS
kubectl get configmap -n kube-system coredns -o yaml
```

## Проблемы с хранилищем

### Проблемы с постоянными томами

**Симптомы:**
- PVC застрял в состоянии `Pending`
- Поды не могут монтировать тома
- Потеря или повреждение данных

**Диагностика:**
```bash
# Проверка статуса PVC
kubectl get pvc

# Проверка статуса PV
kubectl get pv

# Проверка класса хранилища
kubectl get storageclass
```

**Решения:**

1. **Проблемы с классом хранилища**
   ```bash
   # Проверка существования класса хранилища
   kubectl get storageclass
   
   # Проверка конфигурации класса хранилища
   kubectl describe storageclass fast-ssd
   ```

2. **Проблемы с выделением томов**
   ```bash
   # Проверка ошибок провайдера
   kubectl get events --sort-by=.metadata.creationTimestamp | grep -i volume
   
   # Проверка статуса CSI драйвера
   kubectl get pods -n kube-system | grep -i csi
   ```

3. **Проблемы с монтированием томов**
   ```bash
   # Проверка монтирования томов в поде
   kubectl describe pod <pod-name> | grep -A 10 "Mounts:"
   
   # Проверка разрешений томов
   kubectl exec <pod-name> -- ls -la /app/data
   ```

### Повреждение данных

**Симптомы:**
- Ошибки приложения, связанные с доступом к данным
- Несогласованное состояние данных
- Ошибки файловой системы

**Решения:**
```bash
# Проверка целостности файловой системы
kubectl exec <pod-name> -- fsck /app/data

# Резервное копирование и восстановление данных
kubectl exec <pod-name> -- tar czf /tmp/backup.tar.gz /app/data
kubectl cp <pod-name>:/tmp/backup.tar.gz ./backup.tar.gz
```

## Ограничения ресурсов

### Проблемы с CPU и памятью

**Симптомы:**
- Поды убиваются из-за лимитов ресурсов
- Медленная производительность приложения
- Высокое использование ресурсов

**Диагностика:**
```bash
# Проверка использования ресурсов
kubectl top pods
kubectl top nodes

# Проверка запросов и лимитов ресурсов
kubectl describe pod <pod-name> | grep -A 10 "Requests:"
```

**Решения:**

1. **Настройка лимитов ресурсов**
   ```bash
   # Увеличение лимитов памяти
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"memory":"8Gi"}}}]}}}}'
   
   # Увеличение лимитов CPU
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"cpu":"4000m"}}}]}}}}'
   ```

2. **Оптимизация приложения**
   ```bash
   # Проверка утечек памяти
   kubectl exec <pod-name> -- ps aux
   
   # Мониторинг использования ресурсов во времени
   kubectl top pods --containers
   ```

### Исчерпание ресурсов узлов

**Симптомы:**
- Поды застряли в состоянии `Pending`
- Нет доступных узлов для планирования

**Решения:**
```bash
# Проверка емкости узлов
kubectl describe nodes

# Добавление большего количества узлов в кластер
# (Команды, специфичные для облачного провайдера)

# Реализация квот ресурсов
kubectl create quota neozork-quota --hard=cpu=4,memory=8Gi,pods=10
```

## Сетевые проблемы

### Проблемы с сетевыми политиками

**Симптомы:**
- Поды не могут связываться друг с другом
- Заблокирован внешний доступ
- Сбои разрешения DNS

**Диагностика:**
```bash
# Проверка сетевых политик
kubectl get networkpolicies

# Тестирование связности между подами
kubectl exec <pod-1> -- ping <pod-2-ip>
```

**Решения:**
```bash
# Временное отключение сетевых политик для тестирования
kubectl delete networkpolicy neozork-network-policy

# Обновление правил сетевой политики
kubectl apply -f network-policy.yaml
```

### Проблемы с Ingress

**Симптомы:**
- Невозможно получить доступ к приложению извне
- Ошибки SSL/TLS сертификатов
- Проблемы с маршрутизацией

**Диагностика:**
```bash
# Проверка статуса Ingress
kubectl get ingress

# Проверка контроллера Ingress
kubectl get pods -n ingress-nginx
```

**Решения:**
```bash
# Проверка логов контроллера Ingress
kubectl logs -n ingress-nginx <ingress-controller-pod>

# Проверка TLS сертификатов
kubectl describe secret neozork-tls
```

## Проблемы конфигурации

### Проблемы с переменными окружения

**Симптомы:**
- Приложение не запускается
- Неправильные значения конфигурации
- Отсутствующие переменные окружения

**Диагностика:**
```bash
# Проверка переменных окружения в поде
kubectl exec <pod-name> -- env

# Проверка ConfigMap
kubectl get configmap app-config -o yaml
```

**Решения:**
```bash
# Обновление ConfigMap
kubectl patch configmap app-config -p '{"data":{"LOG_LEVEL":"DEBUG"}}'

# Перезапуск развертывания для применения изменений
kubectl rollout restart deployment neozork-interactive-apple
```

### Проблемы управления секретами

**Симптомы:**
- Сбои аутентификации
- Ошибки подключения к базе данных
- Отсутствующие конфиденциальные данные

**Диагностика:**
```bash
# Проверка секретов
kubectl get secrets

# Проверка данных секрета (в кодировке base64)
kubectl get secret app-secrets -o yaml
```

**Решения:**
```bash
# Обновление секрета
kubectl create secret generic app-secrets \
  --from-literal=database-password=new-password \
  --dry-run=client -o yaml | kubectl apply -f -

# Перезапуск подов для применения новых секретов
kubectl rollout restart deployment neozork-interactive-apple
```

## Проблемы безопасности

### Проблемы с RBAC

**Симптомы:**
- Ошибки отказа в доступе
- Проблемы с учетной записью сервиса
- Сбои контроля доступа

**Диагностика:**
```bash
# Проверка учетной записи сервиса
kubectl get serviceaccount

# Проверка правил RBAC
kubectl get role,rolebinding,clusterrole,clusterrolebinding
```

**Решения:**
```bash
# Создание учетной записи сервиса с правильными разрешениями
kubectl create serviceaccount neozork-sa

# Создание роли и привязки роли
kubectl apply -f rbac.yaml
```

### Проблемы безопасности подов

**Симптомы:**
- Поды не запускаются из-за политик безопасности
- Ошибки отказа в доступе
- Нарушения контекста безопасности

**Решения:**
```bash
# Проверка политик безопасности подов
kubectl get psp

# Обновление контекста безопасности
kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"securityContext":{"runAsUser":1000,"runAsGroup":1000}}}}}'
```

## Мониторинг и логирование

### Проблемы сбора метрик

**Симптомы:**
- Метрики не появляются в Prometheus
- Дашборды Grafana не работают
- ServiceMonitor не обнаруживает цели

**Диагностика:**
```bash
# Проверка ServiceMonitor
kubectl get servicemonitor

# Проверка целей Prometheus
kubectl port-forward -n monitoring svc/prometheus-server 9090:80
# Открыть http://localhost:9090/targets
```

**Решения:**
```bash
# Проверка конечной точки метрик
kubectl exec <pod-name> -- curl http://localhost:8080/metrics

# Проверка конфигурации ServiceMonitor
kubectl describe servicemonitor neozork-metrics
```

### Проблемы логирования

**Симптомы:**
- Логи не появляются
- Сбои агрегации логов
- Проблемы ротации логов

**Решения:**
```bash
# Проверка монтирования томов логов
kubectl describe pod <pod-name> | grep -A 5 "Mounts:"

# Проверка разрешений директории логов
kubectl exec <pod-name> -- ls -la /app/logs

# Проверка конфигурации ротации логов
kubectl exec <pod-name> -- cat /etc/logrotate.conf
```

## Платформо-специфичные проблемы

### Проблемы Apple Silicon

**Симптомы:**
- Поды не планируются на узлах ARM64
- Проблемы производительности
- Ошибки фреймворка MLX

**Решения:**
```bash
# Проверка архитектуры узлов
kubectl get nodes -o wide

# Проверка меток узлов
kubectl get nodes --show-labels | grep arch

# Обновление селектора узлов
kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"nodeSelector":{"kubernetes.io/arch":"arm64"}}}}}'
```

### Проблемы совместимости x86

**Симптомы:**
- Проблемы совместимости образов
- Ошибки CUDA/OpenCL
- Деградация производительности

**Решения:**
```bash
# Проверка архитектуры образа
docker inspect neozork-interactive:latest | grep Architecture

# Проверка доступности CUDA
kubectl exec <pod-name> -- nvidia-smi

# Обновление переменных окружения
kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","env":[{"name":"CUDA_ENABLED","value":"true"}]}]}}}}'
```

## Проблемы производительности

### Медленная производительность приложения

**Симптомы:**
- Высокое время отклика
- Узкие места ресурсов
- Плохой пользовательский опыт

**Диагностика:**
```bash
# Проверка использования ресурсов
kubectl top pods --containers

# Проверка ограничения ресурсов
kubectl describe pod <pod-name> | grep -A 5 "Limits:"
```

**Решения:**

1. **Горизонтальное масштабирование**
   ```bash
   # Увеличение количества реплик
   kubectl scale deployment neozork-interactive-apple --replicas=5
   ```

2. **Вертикальное масштабирование**
   ```bash
   # Увеличение лимитов ресурсов
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"memory":"8Gi","cpu":"4000m"}}}]}}}}'
   ```

3. **Оптимизация приложения**
   ```bash
   # Включение профилирования производительности
   kubectl exec <pod-name> -- curl http://localhost:8080/debug/pprof/
   ```

### Производительность базы данных

**Симптомы:**
- Медленные запросы к базе данных
- Исчерпание пула подключений
- Высокое использование CPU базы данных

**Решения:**
```bash
# Проверка использования ресурсов базы данных
kubectl top pods -l app=postgres

# Масштабирование базы данных
kubectl scale deployment postgres-deployment --replicas=2

# Оптимизация конфигурации базы данных
kubectl exec <postgres-pod> -- psql -c "SHOW shared_buffers;"
```

## Процедуры экстренного восстановления

### Шаги быстрого восстановления

1. **Перезапуск развертывания**
   ```bash
   kubectl rollout restart deployment neozork-interactive-apple
   ```

2. **Масштабирование до нуля и обратно**
   ```bash
   kubectl scale deployment neozork-interactive-apple --replicas=0
   kubectl scale deployment neozork-interactive-apple --replicas=2
   ```

3. **Удаление и пересоздание**
   ```bash
   kubectl delete deployment neozork-interactive-apple
   kubectl apply -f k8s/neozork-apple-deployment.yaml
   ```

### Восстановление данных

```bash
# Резервное копирование текущих данных
kubectl exec <pod-name> -- tar czf /tmp/emergency-backup.tar.gz /app/data

# Копирование резервной копии на локальную машину
kubectl cp <pod-name>:/tmp/emergency-backup.tar.gz ./emergency-backup.tar.gz

# Восстановление из резервной копии
kubectl cp ./emergency-backup.tar.gz <new-pod>:/tmp/
kubectl exec <new-pod> -- tar xzf /tmp/emergency-backup.tar.gz -C /
```

## Получение помощи

### Сбор логов

```bash
# Сбор комплексных логов
kubectl logs -l app=neozork-interactive --all-containers=true > neozork-logs.txt
kubectl describe pods -l app=neozork-interactive > pod-descriptions.txt
kubectl get events --sort-by=.metadata.creationTimestamp > events.txt
```

### Ресурсы поддержки

- Ознакомьтесь со [Справочником конфигурации](./configuration-reference-ru.md) для всех доступных опций
- Изучите [Руководство по развертыванию](./deployment-guide-ru.md) для подробных инструкций по настройке
- Откройте issue в репозитории проекта с собранными логами и сообщениями об ошибках
- Обратитесь к документации Kubernetes для общих проблем Kubernetes

Это руководство по устранению неполадок должно помочь решить большинство частых проблем. Для сложных проблем рассмотрите возможность обращения к команде разработки с подробными логами и сообщениями об ошибках.
