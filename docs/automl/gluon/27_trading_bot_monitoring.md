# Мониторинг торгового бота - Лучшие практики

**Автор:** NeoZorK (Shcherbyna Rostyslav)  
**Дата:** 2025  
**Местоположение:** Ukraine, Zaporizhzhya  
**Версия:** 1.0  

## Почему мониторинг торгового бота критически важен

**Почему 90% торговых ботов теряют деньги без правильного мониторинга?** Потому что они работают в слепую, не понимая, что происходит с их системой. Это как вождение автомобиля без приборной панели.

### Проблемы без мониторинга
- **Слепая торговля**: Не знают, что происходит с ботом
- **Позднее обнаружение проблем**: Узнают о проблемах, когда уже поздно
- **Потеря денег**: Бот может торговать против тренда часами
- **Стресс и тревога**: Постоянное беспокойство о работе бота

### Преимущества правильного мониторинга
- **Полный контроль**: Понимают, что происходит с ботом
- **Быстрое обнаружение проблем**: Решают проблемы до потери денег
- **Оптимизация производительности**: Постоянно улучшают работу бота
- **Спокойствие**: Уверены в работе системы

## Введение

**Почему мониторинг - это глаза и уши торгового бота?** Потому что без него вы не знаете, что происходит с вашей системой, и не можете принимать правильные решения.

Мониторинг торгового бота - это критически важный аспект поддержания стабильной и прибыльной торговой системы. Этот раздел посвящен лучшим практикам мониторинга, которые помогут вам быстро выявлять проблемы, оптимизировать производительность и обеспечивать непрерывную работу торгового бота.

## Архитектура системы мониторинга

**Почему архитектура мониторинга критически важна?** Потому что неправильная архитектура может привести к пропуску критических проблем и потере денег.

### 1. Компоненты системы мониторинга

**Почему нужны все компоненты мониторинга?** Потому что каждый компонент решает свою задачу, а вместе они создают полную картину работы бота.

```python
class TradingBotMonitoringSystem:
    """Система мониторинга торгового бота - комплексное решение"""
    
    def __init__(self):
        # Сбор метрик - что происходит с ботом
        self.metrics_collector = MetricsCollector()
        # Управление уведомлениями - когда что-то идет не так
        self.alert_manager = AlertManager()
        # Дашборд - визуализация данных
        self.dashboard = MonitoringDashboard()
        # Анализ логов - поиск проблем
        self.log_analyzer = LogAnalyzer()
        # Отслеживание производительности - как работает бот
        self.performance_tracker = PerformanceTracker()
        # Проверка здоровья - все ли в порядке
        self.health_checker = HealthChecker()
    
    def start_monitoring(self):
        """Запуск системы мониторинга"""
        
        # Инициализация компонентов
        self.metrics_collector.start()
        self.alert_manager.start()
        self.dashboard.start()
        self.log_analyzer.start()
        self.performance_tracker.start()
        self.health_checker.start()
        
        print("✅ Система мониторинга запущена")
    
    def stop_monitoring(self):
        """Остановка системы мониторинга"""
        
        # Остановка компонентов
        self.metrics_collector.stop()
        self.alert_manager.stop()
        self.dashboard.stop()
        self.log_analyzer.stop()
        self.performance_tracker.stop()
        self.health_checker.stop()
        
        print("⏹️ Система мониторинга остановлена")
```

### 2. Сбор метрик

```python
class MetricsCollector:
    """Сборщик метрик торгового бота"""
    
    def __init__(self):
        self.metrics = {}
        self.collection_interval = 60  # секунд
        self.metrics_storage = MetricsStorage()
    
    def collect_trading_metrics(self, bot_state):
        """Сбор торговых метрик"""
        
        trading_metrics = {
            # Производительность
            'total_trades': bot_state.get('total_trades', 0),
            'winning_trades': bot_state.get('winning_trades', 0),
            'losing_trades': bot_state.get('losing_trades', 0),
            'win_rate': self.calculate_win_rate(bot_state),
            'profit_loss': bot_state.get('profit_loss', 0),
            'max_drawdown': bot_state.get('max_drawdown', 0),
            'sharpe_ratio': self.calculate_sharpe_ratio(bot_state),
            
            # Активность
            'trades_per_hour': self.calculate_trades_per_hour(bot_state),
            'last_trade_time': bot_state.get('last_trade_time'),
            'active_positions': bot_state.get('active_positions', 0),
            'pending_orders': bot_state.get('pending_orders', 0),
            
            # Риски
            'current_exposure': bot_state.get('current_exposure', 0),
            'risk_utilization': self.calculate_risk_utilization(bot_state),
            'var_95': self.calculate_var_95(bot_state),
            'expected_shortfall': self.calculate_expected_shortfall(bot_state),
            
            # Технические
            'cpu_usage': bot_state.get('cpu_usage', 0),
            'memory_usage': bot_state.get('memory_usage', 0),
            'disk_usage': bot_state.get('disk_usage', 0),
            'network_latency': bot_state.get('network_latency', 0),
            'api_calls_per_minute': bot_state.get('api_calls_per_minute', 0),
            'error_rate': bot_state.get('error_rate', 0),
            
            # Временные метки
            'timestamp': datetime.now().isoformat(),
            'uptime': self.calculate_uptime(bot_state)
        }
        
        return trading_metrics
    
    def collect_model_metrics(self, model_state):
        """Сбор метрик ML-модели"""
        
        model_metrics = {
            # Точность модели
            'model_accuracy': model_state.get('accuracy', 0),
            'model_precision': model_state.get('precision', 0),
            'model_recall': model_state.get('recall', 0),
            'model_f1_score': model_state.get('f1_score', 0),
            'model_auc': model_state.get('auc', 0),
            
            # Прогнозирование
            'prediction_confidence': model_state.get('prediction_confidence', 0),
            'prediction_uncertainty': model_state.get('prediction_uncertainty', 0),
            'last_prediction_time': model_state.get('last_prediction_time'),
            'predictions_per_hour': model_state.get('predictions_per_hour', 0),
            
            # Дрифт модели
            'model_drift_detected': model_state.get('drift_detected', False),
            'drift_score': model_state.get('drift_score', 0),
            'last_retraining': model_state.get('last_retraining'),
            'retraining_frequency': model_state.get('retraining_frequency', 0),
            
            # Качество данных
            'data_quality_score': model_state.get('data_quality_score', 0),
            'missing_data_rate': model_state.get('missing_data_rate', 0),
            'outlier_rate': model_state.get('outlier_rate', 0),
            'data_freshness': model_state.get('data_freshness', 0),
            
            # Временные метки
            'timestamp': datetime.now().isoformat()
        }
        
        return model_metrics
    
    def collect_market_metrics(self, market_data):
        """Сбор рыночных метрик"""
        
        market_metrics = {
            # Рыночные условия
            'market_volatility': market_data.get('volatility', 0),
            'market_trend': market_data.get('trend', 'unknown'),
            'market_regime': market_data.get('regime', 'unknown'),
            'liquidity_score': market_data.get('liquidity_score', 0),
            
            # Ценовые метрики
            'price_change_1h': market_data.get('price_change_1h', 0),
            'price_change_24h': market_data.get('price_change_24h', 0),
            'volume_24h': market_data.get('volume_24h', 0),
            'volume_change_24h': market_data.get('volume_change_24h', 0),
            
            # Технические индикаторы
            'rsi': market_data.get('rsi', 50),
            'macd': market_data.get('macd', 0),
            'bollinger_position': market_data.get('bollinger_position', 0.5),
            'support_resistance_strength': market_data.get('support_resistance_strength', 0),
            
            # Временные метки
            'timestamp': datetime.now().isoformat()
        }
        
        return market_metrics
```

### 3. Система алертов

```python
class AlertManager:
    """Менеджер алертов"""
    
    def __init__(self):
        self.alert_rules = {}
        self.alert_channels = {}
        self.alert_history = []
        self.alert_cooldown = {}
    
    def setup_alert_rules(self):
        """Настройка правил алертов"""
        
        self.alert_rules = {
            # Критические алерты
            'critical': {
                'bot_down': {
                    'condition': lambda metrics: metrics.get('uptime', 0) == 0,
                    'message': '🚨 КРИТИЧНО: Торговый бот остановлен!',
                    'channels': ['email', 'sms', 'telegram', 'slack'],
                    'cooldown': 300  # 5 минут
                },
                'high_drawdown': {
                    'condition': lambda metrics: metrics.get('max_drawdown', 0) > 0.1,
                    'message': '🚨 КРИТИЧНО: Высокая просадка {max_drawdown:.2%}!',
                    'channels': ['email', 'sms', 'telegram'],
                    'cooldown': 600  # 10 минут
                },
                'api_error_rate': {
                    'condition': lambda metrics: metrics.get('error_rate', 0) > 0.05,
                    'message': '🚨 КРИТИЧНО: Высокий уровень ошибок API {error_rate:.2%}!',
                    'channels': ['email', 'telegram'],
                    'cooldown': 300
                }
            },
            
            # Предупреждения
            'warning': {
                'low_win_rate': {
                    'condition': lambda metrics: metrics.get('win_rate', 0) < 0.4,
                    'message': '⚠️ ПРЕДУПРЕЖДЕНИЕ: Низкий процент выигрышных сделок {win_rate:.2%}',
                    'channels': ['email', 'telegram'],
                    'cooldown': 1800  # 30 минут
                },
                'model_drift': {
                    'condition': lambda metrics: metrics.get('model_drift_detected', False),
                    'message': '⚠️ ПРЕДУПРЕЖДЕНИЕ: Обнаружен дрифт модели!',
                    'channels': ['email', 'telegram'],
                    'cooldown': 3600  # 1 час
                },
                'high_latency': {
                    'condition': lambda metrics: metrics.get('network_latency', 0) > 1000,
                    'message': '⚠️ ПРЕДУПРЕЖДЕНИЕ: Высокая задержка сети {latency}ms',
                    'channels': ['telegram'],
                    'cooldown': 900  # 15 минут
                }
            },
            
            # Информационные
            'info': {
                'daily_summary': {
                    'condition': lambda metrics: self.is_daily_summary_time(),
                    'message': '📊 Ежедневный отчет: P&L: {profit_loss:.2f}, Сделки: {total_trades}',
                    'channels': ['email', 'telegram'],
                    'cooldown': 86400  # 24 часа
                },
                'milestone_reached': {
                    'condition': lambda metrics: self.is_milestone_reached(metrics),
                    'message': '🎉 ДОСТИЖЕНИЕ: {milestone_message}',
                    'channels': ['telegram'],
                    'cooldown': 3600
                }
            }
        }
    
    def check_alerts(self, metrics):
        """Проверка алертов"""
        
        for severity, rules in self.alert_rules.items():
            for rule_name, rule in rules.items():
                try:
                    # Проверка условия
                    if rule['condition'](metrics):
                        # Проверка кулдауна
                        if self.is_cooldown_active(rule_name):
                            continue
                        
                        # Отправка алерта
                        self.send_alert(rule_name, rule, metrics)
                        
                        # Установка кулдауна
                        self.set_cooldown(rule_name, rule['cooldown'])
                        
                except Exception as e:
                    print(f"Ошибка при проверке алерта {rule_name}: {e}")
    
    def send_alert(self, rule_name, rule, metrics):
        """Отправка алерта"""
        
        # Форматирование сообщения
        message = rule['message'].format(**metrics)
        
        # Отправка по каналам
        for channel in rule['channels']:
            try:
                self.send_to_channel(channel, message, metrics)
            except Exception as e:
                print(f"Ошибка отправки в {channel}: {e}")
        
        # Сохранение в историю
        self.alert_history.append({
            'timestamp': datetime.now().isoformat(),
            'rule': rule_name,
            'message': message,
            'metrics': metrics
        })
    
    def send_to_channel(self, channel, message, metrics):
        """Отправка в конкретный канал"""
        
        if channel == 'email':
            self.send_email_alert(message, metrics)
        elif channel == 'sms':
            self.send_sms_alert(message, metrics)
        elif channel == 'telegram':
            self.send_telegram_alert(message, metrics)
        elif channel == 'slack':
            self.send_slack_alert(message, metrics)
    
    def send_telegram_alert(self, message, metrics):
        """Отправка алерта в Telegram"""
        
        import requests
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            return
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        # Форматирование сообщения для Telegram
        formatted_message = f"🤖 *Торговый Бот*\n\n{message}\n\n"
        formatted_message += f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted_message += f"📊 P&L: {metrics.get('profit_loss', 0):.2f}\n"
        formatted_message += f"📈 Сделки: {metrics.get('total_trades', 0)}\n"
        formatted_message += f"🎯 Win Rate: {metrics.get('win_rate', 0):.2%}"
        
        payload = {
            'chat_id': chat_id,
            'text': formatted_message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        return response.status_code == 200
```

### 4. Дашборд мониторинга

```python
class MonitoringDashboard:
    """Дашборд мониторинга"""
    
    def __init__(self):
        self.dashboard_data = {}
        self.charts = {}
        self.widgets = {}
    
    def create_dashboard(self):
        """Создание дашборда"""
        
        # Основные виджеты
        self.widgets = {
            'overview': self.create_overview_widget(),
            'performance': self.create_performance_widget(),
            'trading_activity': self.create_trading_activity_widget(),
            'risk_metrics': self.create_risk_metrics_widget(),
            'system_health': self.create_system_health_widget(),
            'model_metrics': self.create_model_metrics_widget(),
            'market_conditions': self.create_market_conditions_widget()
        }
        
        return self.widgets
    
    def create_overview_widget(self):
        """Виджет обзора"""
        
        return {
            'type': 'overview',
            'title': 'Общий обзор',
            'metrics': [
                {'name': 'P&L', 'value': 'profit_loss', 'format': 'currency'},
                {'name': 'Win Rate', 'value': 'win_rate', 'format': 'percentage'},
                {'name': 'Активных позиций', 'value': 'active_positions', 'format': 'number'},
                {'name': 'Время работы', 'value': 'uptime', 'format': 'duration'},
                {'name': 'Статус', 'value': 'status', 'format': 'status'}
            ]
        }
    
    def create_performance_widget(self):
        """Виджет производительности"""
        
        return {
            'type': 'performance',
            'title': 'Производительность',
            'charts': [
                {
                    'type': 'line',
                    'title': 'P&L во времени',
                    'data': 'profit_loss_history',
                    'x_axis': 'timestamp',
                    'y_axis': 'profit_loss'
                },
                {
                    'type': 'bar',
                    'title': 'Сделки по дням',
                    'data': 'trades_by_day',
                    'x_axis': 'date',
                    'y_axis': 'trade_count'
                },
                {
                    'type': 'pie',
                    'title': 'Распределение сделок',
                    'data': 'trade_distribution',
                    'labels': ['Выигрышные', 'Проигрышные'],
                    'values': ['winning_trades', 'losing_trades']
                }
            ]
        }
    
    def create_risk_metrics_widget(self):
        """Виджет метрик риска"""
        
        return {
            'type': 'risk_metrics',
            'title': 'Метрики риска',
            'metrics': [
                {'name': 'Максимальная просадка', 'value': 'max_drawdown', 'format': 'percentage'},
                {'name': 'Sharpe Ratio', 'value': 'sharpe_ratio', 'format': 'number'},
                {'name': 'VaR 95%', 'value': 'var_95', 'format': 'currency'},
                {'name': 'Текущая экспозиция', 'value': 'current_exposure', 'format': 'currency'},
                {'name': 'Использование риска', 'value': 'risk_utilization', 'format': 'percentage'}
            ],
            'charts': [
                {
                    'type': 'line',
                    'title': 'Просадка во времени',
                    'data': 'drawdown_history',
                    'x_axis': 'timestamp',
                    'y_axis': 'drawdown'
                }
            ]
        }
    
    def create_system_health_widget(self):
        """Виджет здоровья системы"""
        
        return {
            'type': 'system_health',
            'title': 'Здоровье системы',
            'metrics': [
                {'name': 'CPU', 'value': 'cpu_usage', 'format': 'percentage'},
                {'name': 'Память', 'value': 'memory_usage', 'format': 'percentage'},
                {'name': 'Диск', 'value': 'disk_usage', 'format': 'percentage'},
                {'name': 'Задержка сети', 'value': 'network_latency', 'format': 'duration'},
                {'name': 'Ошибки API', 'value': 'error_rate', 'format': 'percentage'}
            ],
            'charts': [
                {
                    'type': 'gauge',
                    'title': 'Использование ресурсов',
                    'data': 'resource_usage',
                    'max_value': 100
                }
            ]
        }
```

### 5. Анализ логов

```python
class LogAnalyzer:
    """Анализатор логов"""
    
    def __init__(self):
        self.log_patterns = {}
        self.error_patterns = {}
        self.performance_patterns = {}
    
    def analyze_logs(self, log_file):
        """Анализ логов"""
        
        analysis_results = {
            'errors': self.analyze_errors(log_file),
            'performance_issues': self.analyze_performance_issues(log_file),
            'trading_patterns': self.analyze_trading_patterns(log_file),
            'system_issues': self.analyze_system_issues(log_file)
        }
        
        return analysis_results
    
    def analyze_errors(self, log_file):
        """Анализ ошибок"""
        
        error_patterns = [
            r'ERROR: (.+)',
            r'EXCEPTION: (.+)',
            r'CRITICAL: (.+)',
            r'Failed to (.+)',
            r'Connection error: (.+)',
            r'API error: (.+)'
        ]
        
        errors = []
        
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in error_patterns:
                    match = re.search(pattern, line)
                    if match:
                        errors.append({
                            'line': line_num,
                            'error': match.group(1),
                            'timestamp': self.extract_timestamp(line),
                            'severity': self.classify_error_severity(match.group(1))
                        })
        
        return errors
    
    def analyze_performance_issues(self, log_file):
        """Анализ проблем производительности"""
        
        performance_patterns = [
            r'Slow operation: (.+) took (\d+)ms',
            r'High memory usage: (\d+)MB',
            r'CPU spike detected: (\d+)%',
            r'Network timeout: (.+)',
            r'Database slow query: (.+)'
        ]
        
        performance_issues = []
        
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in performance_patterns:
                    match = re.search(pattern, line)
                    if match:
                        performance_issues.append({
                            'line': line_num,
                            'issue': match.group(1),
                            'value': match.group(2) if len(match.groups()) > 1 else None,
                            'timestamp': self.extract_timestamp(line)
                        })
        
        return performance_issues
    
    def analyze_trading_patterns(self, log_file):
        """Анализ торговых паттернов"""
        
        trading_patterns = [
            r'Trade executed: (.+)',
            r'Order placed: (.+)',
            r'Position opened: (.+)',
            r'Position closed: (.+)',
            r'Stop loss triggered: (.+)',
            r'Take profit triggered: (.+)'
        ]
        
        trading_events = []
        
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in trading_patterns:
                    match = re.search(pattern, line)
                    if match:
                        trading_events.append({
                            'line': line_num,
                            'event': match.group(1),
                            'timestamp': self.extract_timestamp(line),
                            'type': self.classify_trading_event(match.group(1))
                        })
        
        return trading_events
```

### 6. Отслеживание производительности

```python
class PerformanceTracker:
    """Отслеживание производительности"""
    
    def __init__(self):
        self.performance_metrics = {}
        self.benchmarks = {}
        self.optimization_suggestions = {}
    
    def track_performance(self, metrics):
        """Отслеживание производительности"""
        
        # Расчет ключевых метрик
        performance_score = self.calculate_performance_score(metrics)
        
        # Сравнение с бенчмарками
        benchmark_comparison = self.compare_with_benchmarks(metrics)
        
        # Генерация предложений по оптимизации
        optimization_suggestions = self.generate_optimization_suggestions(metrics)
        
        return {
            'performance_score': performance_score,
            'benchmark_comparison': benchmark_comparison,
            'optimization_suggestions': optimization_suggestions,
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_performance_score(self, metrics):
        """Расчет оценки производительности"""
        
        # Веса для различных метрик
        weights = {
            'win_rate': 0.25,
            'sharpe_ratio': 0.20,
            'max_drawdown': 0.15,
            'profit_loss': 0.15,
            'trades_per_hour': 0.10,
            'error_rate': 0.10,
            'uptime': 0.05
        }
        
        # Нормализация метрик
        normalized_metrics = self.normalize_metrics(metrics)
        
        # Расчет взвешенной оценки
        performance_score = sum(
            normalized_metrics[metric] * weight 
            for metric, weight in weights.items()
        )
        
        return performance_score
    
    def generate_optimization_suggestions(self, metrics):
        """Генерация предложений по оптимизации"""
        
        suggestions = []
        
        # Анализ win rate
        if metrics.get('win_rate', 0) < 0.5:
            suggestions.append({
                'category': 'trading_strategy',
                'priority': 'high',
                'suggestion': 'Низкий процент выигрышных сделок. Рассмотрите пересмотр торговой стратегии.',
                'action': 'analyze_losing_trades'
            })
        
        # Анализ просадки
        if metrics.get('max_drawdown', 0) > 0.1:
            suggestions.append({
                'category': 'risk_management',
                'priority': 'high',
                'suggestion': 'Высокая просадка. Улучшите управление рисками.',
                'action': 'reduce_position_sizes'
            })
        
        # Анализ ошибок
        if metrics.get('error_rate', 0) > 0.02:
            suggestions.append({
                'category': 'system_stability',
                'priority': 'medium',
                'suggestion': 'Высокий уровень ошибок. Проверьте стабильность системы.',
                'action': 'review_error_logs'
            })
        
        # Анализ производительности
        if metrics.get('trades_per_hour', 0) < 1:
            suggestions.append({
                'category': 'trading_activity',
                'priority': 'low',
                'suggestion': 'Низкая торговая активность. Проверьте условия входа.',
                'action': 'review_entry_conditions'
            })
        
        return suggestions
```

### 7. Проверка здоровья системы

```python
class HealthChecker:
    """Проверка здоровья системы"""
    
    def __init__(self):
        self.health_checks = {}
        self.health_status = {}
    
    def perform_health_checks(self, system_state):
        """Выполнение проверок здоровья"""
        
        health_checks = {
            'bot_running': self.check_bot_running(system_state),
            'api_connectivity': self.check_api_connectivity(system_state),
            'model_loaded': self.check_model_loaded(system_state),
            'data_freshness': self.check_data_freshness(system_state),
            'memory_usage': self.check_memory_usage(system_state),
            'disk_space': self.check_disk_space(system_state),
            'network_connectivity': self.check_network_connectivity(system_state)
        }
        
        # Общий статус здоровья
        overall_health = self.calculate_overall_health(health_checks)
        
        return {
            'overall_health': overall_health,
            'individual_checks': health_checks,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_bot_running(self, system_state):
        """Проверка работы бота"""
        
        uptime = system_state.get('uptime', 0)
        last_activity = system_state.get('last_activity', 0)
        
        # Бот считается работающим, если время работы > 0 и последняя активность < 5 минут
        is_running = uptime > 0 and (time.time() - last_activity) < 300
        
        return {
            'status': 'healthy' if is_running else 'unhealthy',
            'message': 'Бот работает' if is_running else 'Бот не работает',
            'details': {
                'uptime': uptime,
                'last_activity': last_activity
            }
        }
    
    def check_api_connectivity(self, system_state):
        """Проверка подключения к API"""
        
        api_latency = system_state.get('api_latency', 0)
        api_error_rate = system_state.get('api_error_rate', 0)
        
        # API считается здоровым, если задержка < 1000ms и ошибок < 5%
        is_healthy = api_latency < 1000 and api_error_rate < 0.05
        
        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'message': 'API подключение стабильно' if is_healthy else 'Проблемы с API',
            'details': {
                'latency': api_latency,
                'error_rate': api_error_rate
            }
        }
    
    def check_model_loaded(self, system_state):
        """Проверка загрузки модели"""
        
        model_loaded = system_state.get('model_loaded', False)
        model_accuracy = system_state.get('model_accuracy', 0)
        
        # Модель считается здоровой, если загружена и точность > 0.7
        is_healthy = model_loaded and model_accuracy > 0.7
        
        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'message': 'Модель загружена и работает' if is_healthy else 'Проблемы с моделью',
            'details': {
                'loaded': model_loaded,
                'accuracy': model_accuracy
            }
        }
```

## Лучшие практики мониторинга

### 1. Настройка алертов

```python
class AlertBestPractices:
    """Лучшие практики настройки алертов"""
    
    def __init__(self):
        self.alert_hierarchy = {}
        self.escalation_rules = {}
    
    def setup_alert_hierarchy(self):
        """Настройка иерархии алертов"""
        
        self.alert_hierarchy = {
            'critical': {
                'response_time': 5,  # минут
                'escalation_time': 15,  # минут
                'channels': ['sms', 'phone', 'email', 'telegram'],
                'auto_actions': ['restart_bot', 'close_positions']
            },
            'warning': {
                'response_time': 30,  # минут
                'escalation_time': 60,  # минут
                'channels': ['email', 'telegram'],
                'auto_actions': ['log_issue', 'notify_admin']
            },
            'info': {
                'response_time': 120,  # минут
                'escalation_time': 240,  # минут
                'channels': ['telegram'],
                'auto_actions': ['log_event']
            }
        }
    
    def setup_escalation_rules(self):
        """Настройка правил эскалации"""
        
        self.escalation_rules = {
            'no_response': {
                'condition': 'no_response_for_30_minutes',
                'action': 'escalate_to_manager',
                'channels': ['phone', 'sms']
            },
            'repeated_alerts': {
                'condition': 'same_alert_3_times_in_1_hour',
                'action': 'escalate_to_technical_lead',
                'channels': ['phone', 'email']
            },
            'system_down': {
                'condition': 'bot_down_for_10_minutes',
                'action': 'escalate_to_emergency_contact',
                'channels': ['phone', 'sms', 'email']
            }
        }
```

### 2. Ротация логов

```python
class LogRotation:
    """Ротация логов"""
    
    def __init__(self):
        self.rotation_config = {}
        self.compression_config = {}
        self.retention_config = {}
    
    def setup_log_rotation(self):
        """Настройка ротации логов"""
        
        self.rotation_config = {
            'max_size': '100MB',
            'max_files': 10,
            'rotation_time': 'daily',
            'compression': True,
            'retention_days': 30
        }
    
    def rotate_logs(self, log_file):
        """Ротация логов"""
        
        import shutil
        import gzip
        from datetime import datetime
        
        # Создание резервной копии
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{log_file}.{timestamp}"
        shutil.copy2(log_file, backup_file)
        
        # Сжатие старого лога
        if self.rotation_config['compression']:
            with open(backup_file, 'rb') as f_in:
                with gzip.open(f"{backup_file}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(backup_file)
            backup_file = f"{backup_file}.gz"
        
        # Очистка текущего лога
        with open(log_file, 'w') as f:
            f.write('')
        
        # Удаление старых логов
        self.cleanup_old_logs(log_file)
        
        return backup_file
    
    def cleanup_old_logs(self, log_file):
        """Очистка старых логов"""
        
        import glob
        import os
        from datetime import datetime, timedelta
        
        log_dir = os.path.dirname(log_file)
        log_pattern = f"{log_file}.*"
        
        # Получение всех логов
        log_files = glob.glob(log_pattern)
        
        # Фильтрация по возрасту
        cutoff_date = datetime.now() - timedelta(days=self.retention_config['retention_days'])
        
        for file_path in log_files:
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if file_time < cutoff_date:
                os.remove(file_path)
```

### 3. Метрики производительности

```python
class PerformanceMetrics:
    """Метрики производительности"""
    
    def __init__(self):
        self.metrics_definitions = {}
        self.benchmarks = {}
        self.sla_targets = {}
    
    def define_metrics(self):
        """Определение метрик"""
        
        self.metrics_definitions = {
            'availability': {
                'description': 'Доступность системы',
                'calculation': 'uptime / total_time',
                'target': 0.999,  # 99.9%
                'unit': 'percentage'
            },
            'response_time': {
                'description': 'Время отклика',
                'calculation': 'average_response_time',
                'target': 1000,  # 1 секунда
                'unit': 'milliseconds'
            },
            'error_rate': {
                'description': 'Частота ошибок',
                'calculation': 'errors / total_requests',
                'target': 0.001,  # 0.1%
                'unit': 'percentage'
            },
            'throughput': {
                'description': 'Пропускная способность',
                'calculation': 'requests_per_second',
                'target': 100,  # 100 RPS
                'unit': 'requests_per_second'
            }
        }
    
    def setup_sla_targets(self):
        """Настройка SLA целей"""
        
        self.sla_targets = {
            'availability': 0.999,  # 99.9%
            'response_time_p95': 2000,  # 2 секунды
            'response_time_p99': 5000,  # 5 секунд
            'error_rate': 0.001,  # 0.1%
            'data_freshness': 300,  # 5 минут
            'model_accuracy': 0.8  # 80%
        }
    
    def calculate_sla_compliance(self, metrics):
        """Расчет соответствия SLA"""
        
        compliance = {}
        
        for metric, target in self.sla_targets.items():
            current_value = metrics.get(metric, 0)
            
            if metric in ['availability', 'model_accuracy']:
                # Для метрик "больше лучше"
                compliance[metric] = current_value >= target
            else:
                # Для метрик "меньше лучше"
                compliance[metric] = current_value <= target
        
        # Общее соответствие SLA
        overall_compliance = all(compliance.values())
        
        return {
            'overall_compliance': overall_compliance,
            'individual_compliance': compliance,
            'sla_score': sum(compliance.values()) / len(compliance)
        }
```

## Автоматизация мониторинга

### 1. Автоматические действия

```python
class AutomatedActions:
    """Автоматические действия"""
    
    def __init__(self):
        self.action_rules = {}
        self.action_history = []
    
    def setup_automated_actions(self):
        """Настройка автоматических действий"""
        
        self.action_rules = {
            'restart_bot': {
                'trigger': 'bot_down_for_5_minutes',
                'action': self.restart_bot,
                'max_attempts': 3,
                'cooldown': 300  # 5 минут
            },
            'close_all_positions': {
                'trigger': 'max_drawdown_exceeded',
                'action': self.close_all_positions,
                'max_attempts': 1,
                'cooldown': 0
            },
            'reduce_position_sizes': {
                'trigger': 'high_volatility_detected',
                'action': self.reduce_position_sizes,
                'max_attempts': 5,
                'cooldown': 3600  # 1 час
            },
            'retrain_model': {
                'trigger': 'model_drift_detected',
                'action': self.retrain_model,
                'max_attempts': 1,
                'cooldown': 86400  # 24 часа
            }
        }
    
    def execute_automated_action(self, action_name, trigger_data):
        """Выполнение автоматического действия"""
        
        if action_name not in self.action_rules:
            return False
        
        rule = self.action_rules[action_name]
        
        # Проверка кулдауна
        if self.is_action_in_cooldown(action_name):
            return False
        
        # Проверка максимального количества попыток
        if self.get_action_attempts(action_name) >= rule['max_attempts']:
            return False
        
        try:
            # Выполнение действия
            result = rule['action'](trigger_data)
            
            # Запись в историю
            self.action_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': action_name,
                'trigger': trigger_data,
                'result': result,
                'success': result.get('success', False)
            })
            
            # Установка кулдауна
            if result.get('success', False):
                self.set_action_cooldown(action_name, rule['cooldown'])
            
            return result
            
        except Exception as e:
            print(f"Ошибка выполнения действия {action_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def restart_bot(self, trigger_data):
        """Перезапуск бота"""
        
        try:
            # Остановка бота
            self.stop_bot()
            
            # Ожидание
            time.sleep(10)
            
            # Запуск бота
            self.start_bot()
            
            return {'success': True, 'message': 'Бот перезапущен'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def close_all_positions(self, trigger_data):
        """Закрытие всех позиций"""
        
        try:
            # Получение активных позиций
            active_positions = self.get_active_positions()
            
            # Закрытие позиций
            closed_positions = []
            for position in active_positions:
                result = self.close_position(position['id'])
                if result['success']:
                    closed_positions.append(position['id'])
            
            return {
                'success': True, 
                'message': f'Закрыто позиций: {len(closed_positions)}',
                'closed_positions': closed_positions
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
```

### 2. Интеграция с внешними системами

```python
class ExternalIntegrations:
    """Интеграция с внешними системами"""
    
    def __init__(self):
        self.integrations = {}
        self.webhook_endpoints = {}
    
    def setup_integrations(self):
        """Настройка интеграций"""
        
        self.integrations = {
            'prometheus': self.setup_prometheus_integration(),
            'grafana': self.setup_grafana_integration(),
            'datadog': self.setup_datadog_integration(),
            'new_relic': self.setup_new_relic_integration(),
            'webhooks': self.setup_webhook_integration()
        }
    
    def setup_prometheus_integration(self):
        """Интеграция с Prometheus"""
        
        from prometheus_client import Counter, Histogram, Gauge, start_http_server
        
        # Метрики
        self.prometheus_metrics = {
            'trades_total': Counter('trading_bot_trades_total', 'Total number of trades'),
            'profit_loss': Gauge('trading_bot_profit_loss', 'Current profit/loss'),
            'win_rate': Gauge('trading_bot_win_rate', 'Current win rate'),
            'response_time': Histogram('trading_bot_response_time', 'Response time'),
            'error_rate': Gauge('trading_bot_error_rate', 'Current error rate')
        }
        
        # Запуск HTTP сервера для метрик
        start_http_server(8000)
        
        return True
    
    def setup_grafana_integration(self):
        """Интеграция с Grafana"""
        
        # Настройка дашборда Grafana
        grafana_config = {
            'datasource': 'prometheus',
            'dashboard_url': 'http://grafana:3000/d/trading-bot',
            'panels': [
                {
                    'title': 'Trading Performance',
                    'type': 'graph',
                    'targets': [
                        'trading_bot_profit_loss',
                        'trading_bot_win_rate'
                    ]
                },
                {
                    'title': 'System Health',
                    'type': 'singlestat',
                    'targets': [
                        'trading_bot_error_rate'
                    ]
                }
            ]
        }
        
        return grafana_config
    
    def setup_webhook_integration(self):
        """Интеграция с webhooks"""
        
        self.webhook_endpoints = {
            'trading_events': 'https://api.example.com/webhooks/trading',
            'system_alerts': 'https://api.example.com/webhooks/alerts',
            'performance_reports': 'https://api.example.com/webhooks/performance'
        }
        
        return True
    
    def send_webhook(self, endpoint, data):
        """Отправка webhook"""
        
        import requests
        
        if endpoint not in self.webhook_endpoints:
            return False
        
        url = self.webhook_endpoints[endpoint]
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Ошибка отправки webhook: {e}")
            return False
```

## Заключение

Мониторинг торгового бота - это критически важный аспект поддержания стабильной и прибыльной торговой системы. Следуя лучшим практикам, описанным в этом разделе, вы сможете:

1. **Быстро выявлять проблемы** - с помощью системы алертов и проверок здоровья
2. **Оптимизировать производительность** - через анализ метрик и предложения по улучшению
3. **Обеспечивать непрерывную работу** - с помощью автоматических действий и восстановления
4. **Интегрироваться с внешними системами** - для расширенного мониторинга и анализа

Помните: хороший мониторинг - это залог успешной торговой системы! 🚀
