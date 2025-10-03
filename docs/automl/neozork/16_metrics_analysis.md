# 16. Метрики и анализ - Измерение производительности системы

**Цель:** Понять, как правильно измерять и анализировать производительность ML-системы для достижения доходности 100%+ в месяц.

## Почему метрики критически важны?

### Проблемы без правильных метрик

1. **Ложное чувство успеха** - система кажется прибыльной, но на самом деле проигрывает
2. **Неправильная оптимизация** - оптимизация не тех параметров
3. **Игнорирование рисков** - фокус только на прибыли, игнорирование рисков
4. **Отсутствие сравнения** - нет бенчмарков для сравнения
5. **Неправильные выводы** - принятие решений на основе неполных данных

### Наш подход к метрикам

**Мы используем:**
- Многоуровневые метрики
- Временные метрики
- Риск-скорректированные метрики
- Сравнительные метрики
- Прогнозные метрики

## Базовые метрики производительности

### 1. Метрики доходности

```python
class ReturnMetrics:
    """Метрики доходности"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_total_return(self, returns):
        """Расчет общей доходности"""
        total_return = np.sum(returns)
        return total_return
    
    def calculate_annualized_return(self, returns):
        """Расчет годовой доходности"""
        annualized_return = np.mean(returns) * 252  # 252 торговых дня в году
        return annualized_return
    
    def calculate_compound_annual_growth_rate(self, returns):
        """Расчет CAGR"""
        total_return = np.sum(returns)
        years = len(returns) / 252
        cagr = (1 + total_return) ** (1 / years) - 1
        return cagr
    
    def calculate_monthly_return(self, returns):
        """Расчет месячной доходности"""
        monthly_returns = returns.resample('M').sum()
        return monthly_returns
    
    def calculate_weekly_return(self, returns):
        """Расчет недельной доходности"""
        weekly_returns = returns.resample('W').sum()
        return weekly_returns
    
    def calculate_daily_return(self, returns):
        """Расчет дневной доходности"""
        daily_returns = returns.resample('D').sum()
        return daily_returns
```

### 2. Метрики риска

```python
class RiskMetrics:
    """Метрики риска"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_volatility(self, returns):
        """Расчет волатильности"""
        volatility = np.std(returns) * np.sqrt(252)
        return volatility
    
    def calculate_max_drawdown(self, returns):
        """Расчет максимальной просадки"""
        cumulative_returns = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = cumulative_returns - running_max
        max_drawdown = np.min(drawdown)
        return max_drawdown
    
    def calculate_value_at_risk(self, returns, confidence_level=0.05):
        """Расчет VaR"""
        var = np.percentile(returns, confidence_level * 100)
        return var
    
    def calculate_conditional_var(self, returns, confidence_level=0.05):
        """Расчет CVaR"""
        var = self.calculate_value_at_risk(returns, confidence_level)
        cvar = np.mean(returns[returns <= var])
        return cvar
    
    def calculate_downside_deviation(self, returns, target_return=0):
        """Расчет downside deviation"""
        downside_returns = returns[returns < target_return]
        downside_deviation = np.std(downside_returns)
        return downside_deviation
```

### 3. Метрики эффективности

```python
class EfficiencyMetrics:
    """Метрики эффективности"""
    
    def __init__(self, risk_free_rate=0.02):
        self.risk_free_rate = risk_free_rate
    
    def calculate_sharpe_ratio(self, returns):
        """Расчет Sharpe Ratio"""
        excess_return = np.mean(returns) - self.risk_free_rate
        volatility = np.std(returns)
        sharpe_ratio = excess_return / volatility if volatility > 0 else 0
        return sharpe_ratio
    
    def calculate_sortino_ratio(self, returns, target_return=0):
        """Расчет Sortino Ratio"""
        excess_return = np.mean(returns) - target_return
        downside_deviation = self.calculate_downside_deviation(returns, target_return)
        sortino_ratio = excess_return / downside_deviation if downside_deviation > 0 else 0
        return sortino_ratio
    
    def calculate_calmar_ratio(self, returns):
        """Расчет Calmar Ratio"""
        annualized_return = np.mean(returns) * 252
        max_drawdown = self.calculate_max_drawdown(returns)
        calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
        return calmar_ratio
    
    def calculate_information_ratio(self, returns, benchmark_returns):
        """Расчет Information Ratio"""
        excess_returns = returns - benchmark_returns
        tracking_error = np.std(excess_returns)
        information_ratio = np.mean(excess_returns) / tracking_error if tracking_error > 0 else 0
        return information_ratio
```

## Продвинутые метрики

### 1. Метрики стабильности

```python
class StabilityMetrics:
    """Метрики стабильности"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_consistency_ratio(self, returns):
        """Расчет коэффициента консистентности"""
        positive_returns = np.sum(returns > 0)
        total_returns = len(returns)
        consistency_ratio = positive_returns / total_returns
        return consistency_ratio
    
    def calculate_stability_ratio(self, returns):
        """Расчет коэффициента стабильности"""
        # Стабильность = 1 - коэффициент вариации
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        coefficient_of_variation = std_return / abs(mean_return) if mean_return != 0 else np.inf
        stability_ratio = 1 - coefficient_of_variation
        return max(0, stability_ratio)
    
    def calculate_win_loss_ratio(self, returns):
        """Расчет соотношения выигрышей к проигрышам"""
        winning_returns = returns[returns > 0]
        losing_returns = returns[returns < 0]
        
        if len(losing_returns) == 0:
            return np.inf
        
        avg_win = np.mean(winning_returns) if len(winning_returns) > 0 else 0
        avg_loss = abs(np.mean(losing_returns))
        
        win_loss_ratio = avg_win / avg_loss
        return win_loss_ratio
    
    def calculate_profit_factor(self, returns):
        """Расчет Profit Factor"""
        gross_profit = np.sum(returns[returns > 0])
        gross_loss = abs(np.sum(returns[returns < 0]))
        
        if gross_loss == 0:
            return np.inf
        
        profit_factor = gross_profit / gross_loss
        return profit_factor
```

### 2. Метрики адаптивности

```python
class AdaptabilityMetrics:
    """Метрики адаптивности"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_adaptation_speed(self, returns, window=252):
        """Расчет скорости адаптации"""
        # Скользящие метрики
        rolling_returns = returns.rolling(window)
        rolling_mean = rolling_returns.mean()
        rolling_std = rolling_returns.std()
        
        # Изменения метрик
        mean_changes = rolling_mean.diff().abs()
        std_changes = rolling_std.diff().abs()
        
        # Скорость адаптации
        adaptation_speed = np.mean(mean_changes) + np.mean(std_changes)
        return adaptation_speed
    
    def calculate_regime_stability(self, returns, n_regimes=3):
        """Расчет стабильности режимов"""
        # Кластеризация режимов
        from sklearn.cluster import KMeans
        
        # Подготовка данных
        returns_reshaped = returns.values.reshape(-1, 1)
        
        # Кластеризация
        kmeans = KMeans(n_clusters=n_regimes, random_state=42)
        regime_labels = kmeans.fit_predict(returns_reshaped)
        
        # Расчет стабильности режимов
        regime_changes = np.sum(np.diff(regime_labels) != 0)
        regime_stability = 1 - (regime_changes / len(returns))
        
        return regime_stability
    
    def calculate_market_correlation_stability(self, returns, market_returns):
        """Расчет стабильности корреляции с рынком"""
        # Скользящая корреляция
        rolling_correlation = returns.rolling(252).corr(market_returns)
        
        # Стабильность корреляции
        correlation_std = rolling_correlation.std()
        correlation_stability = 1 - correlation_std
        
        return correlation_stability
```

### 3. Метрики предсказательной способности

```python
class PredictiveMetrics:
    """Метрики предсказательной способности"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_prediction_accuracy(self, predictions, actual):
        """Расчет точности предсказаний"""
        accuracy = np.mean(predictions == actual)
        return accuracy
    
    def calculate_directional_accuracy(self, predicted_returns, actual_returns):
        """Расчет точности направления"""
        predicted_direction = np.sign(predicted_returns)
        actual_direction = np.sign(actual_returns)
        
        directional_accuracy = np.mean(predicted_direction == actual_direction)
        return directional_accuracy
    
    def calculate_magnitude_accuracy(self, predicted_returns, actual_returns, tolerance=0.1):
        """Расчет точности величины"""
        relative_error = np.abs(predicted_returns - actual_returns) / np.abs(actual_returns)
        magnitude_accuracy = np.mean(relative_error <= tolerance)
        return magnitude_accuracy
    
    def calculate_forecast_skill(self, predicted_returns, actual_returns, benchmark_returns):
        """Расчет навыка прогнозирования"""
        # MSE модели
        model_mse = np.mean((predicted_returns - actual_returns) ** 2)
        
        # MSE бенчмарка
        benchmark_mse = np.mean((benchmark_returns - actual_returns) ** 2)
        
        # Навык прогнозирования
        forecast_skill = 1 - (model_mse / benchmark_mse)
        return forecast_skill
```

## Временные метрики

### 1. Метрики по периодам

```python
class TemporalMetrics:
    """Временные метрики"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_monthly_metrics(self, returns):
        """Расчет месячных метрик"""
        monthly_returns = returns.resample('M').sum()
        
        metrics = {
            'monthly_return': monthly_returns.mean(),
            'monthly_volatility': monthly_returns.std(),
            'monthly_sharpe': monthly_returns.mean() / monthly_returns.std(),
            'positive_months': np.sum(monthly_returns > 0) / len(monthly_returns),
            'best_month': monthly_returns.max(),
            'worst_month': monthly_returns.min()
        }
        
        return metrics
    
    def calculate_quarterly_metrics(self, returns):
        """Расчет квартальных метрик"""
        quarterly_returns = returns.resample('Q').sum()
        
        metrics = {
            'quarterly_return': quarterly_returns.mean(),
            'quarterly_volatility': quarterly_returns.std(),
            'quarterly_sharpe': quarterly_returns.mean() / quarterly_returns.std(),
            'positive_quarters': np.sum(quarterly_returns > 0) / len(quarterly_returns),
            'best_quarter': quarterly_returns.max(),
            'worst_quarter': quarterly_returns.min()
        }
        
        return metrics
    
    def calculate_yearly_metrics(self, returns):
        """Расчет годовых метрик"""
        yearly_returns = returns.resample('Y').sum()
        
        metrics = {
            'yearly_return': yearly_returns.mean(),
            'yearly_volatility': yearly_returns.std(),
            'yearly_sharpe': yearly_returns.mean() / yearly_returns.std(),
            'positive_years': np.sum(yearly_returns > 0) / len(yearly_returns),
            'best_year': yearly_returns.max(),
            'worst_year': yearly_returns.min()
        }
        
        return metrics
```

### 2. Метрики сезонности

```python
class SeasonalityMetrics:
    """Метрики сезонности"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_monthly_seasonality(self, returns):
        """Расчет месячной сезонности"""
        monthly_returns = returns.groupby(returns.index.month)
        
        seasonality = {}
        for month in range(1, 13):
            month_returns = monthly_returns.get_group(month)
            seasonality[month] = {
                'mean_return': month_returns.mean(),
                'volatility': month_returns.std(),
                'positive_months': np.sum(month_returns > 0) / len(month_returns)
            }
        
        return seasonality
    
    def calculate_quarterly_seasonality(self, returns):
        """Расчет квартальной сезонности"""
        quarterly_returns = returns.groupby(returns.index.quarter)
        
        seasonality = {}
        for quarter in range(1, 5):
            quarter_returns = quarterly_returns.get_group(quarter)
            seasonality[quarter] = {
                'mean_return': quarter_returns.mean(),
                'volatility': quarter_returns.std(),
                'positive_quarters': np.sum(quarter_returns > 0) / len(quarter_returns)
            }
        
        return seasonality
    
    def calculate_weekly_seasonality(self, returns):
        """Расчет недельной сезонности"""
        weekly_returns = returns.groupby(returns.index.dayofweek)
        
        seasonality = {}
        for day in range(7):
            day_returns = weekly_returns.get_group(day)
            seasonality[day] = {
                'mean_return': day_returns.mean(),
                'volatility': day_returns.std(),
                'positive_days': np.sum(day_returns > 0) / len(day_returns)
            }
        
        return seasonality
```

## Сравнительные метрики

### 1. Бенчмарк сравнение

```python
class BenchmarkComparison:
    """Сравнение с бенчмарками"""
    
    def __init__(self, benchmark_returns):
        self.benchmark_returns = benchmark_returns
    
    def calculate_alpha(self, returns):
        """Расчет Alpha"""
        # Регрессия доходности на бенчмарк
        from sklearn.linear_model import LinearRegression
        
        X = self.benchmark_returns.values.reshape(-1, 1)
        y = returns.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Alpha = intercept
        alpha = model.intercept_
        return alpha
    
    def calculate_beta(self, returns):
        """Расчет Beta"""
        # Регрессия доходности на бенчмарк
        from sklearn.linear_model import LinearRegression
        
        X = self.benchmark_returns.values.reshape(-1, 1)
        y = returns.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Beta = coefficient
        beta = model.coef_[0]
        return beta
    
    def calculate_tracking_error(self, returns):
        """Расчет Tracking Error"""
        excess_returns = returns - self.benchmark_returns
        tracking_error = np.std(excess_returns)
        return tracking_error
    
    def calculate_information_ratio(self, returns):
        """Расчет Information Ratio"""
        excess_returns = returns - self.benchmark_returns
        tracking_error = np.std(excess_returns)
        information_ratio = np.mean(excess_returns) / tracking_error if tracking_error > 0 else 0
        return information_ratio
```

### 2. Peer сравнение

```python
class PeerComparison:
    """Сравнение с аналогами"""
    
    def __init__(self, peer_returns):
        self.peer_returns = peer_returns
    
    def calculate_percentile_rank(self, returns):
        """Расчет процентильного ранга"""
        # Сравнение с аналогами
        percentile_ranks = {}
        
        for metric_name, peer_metric in self.peer_returns.items():
            # Расчет метрики для нашей системы
            our_metric = self._calculate_metric(returns, metric_name)
            
            # Расчет процентильного ранга
            percentile_rank = np.percentile(peer_metric, our_metric)
            percentile_ranks[metric_name] = percentile_rank
        
        return percentile_ranks
    
    def calculate_relative_performance(self, returns):
        """Расчет относительной производительности"""
        relative_performance = {}
        
        for metric_name, peer_metric in self.peer_returns.items():
            # Расчет метрики для нашей системы
            our_metric = self._calculate_metric(returns, metric_name)
            
            # Расчет относительной производительности
            peer_mean = np.mean(peer_metric)
            relative_performance[metric_name] = our_metric / peer_mean
        
        return relative_performance
```

## Прогнозные метрики

### 1. Метрики прогнозирования

```python
class ForecastingMetrics:
    """Метрики прогнозирования"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_mape(self, predicted, actual):
        """Расчет MAPE"""
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        return mape
    
    def calculate_rmse(self, predicted, actual):
        """Расчет RMSE"""
        rmse = np.sqrt(np.mean((predicted - actual) ** 2))
        return rmse
    
    def calculate_mae(self, predicted, actual):
        """Расчет MAE"""
        mae = np.mean(np.abs(predicted - actual))
        return mae
    
    def calculate_r2_score(self, predicted, actual):
        """Расчет R²"""
        from sklearn.metrics import r2_score
        r2 = r2_score(actual, predicted)
        return r2
```

### 2. Метрики стабильности прогнозов

```python
class ForecastStabilityMetrics:
    """Метрики стабильности прогнозов"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_forecast_stability(self, predictions):
        """Расчет стабильности прогнозов"""
        # Изменения прогнозов
        prediction_changes = np.diff(predictions)
        
        # Стабильность = 1 - стандартное отклонение изменений
        stability = 1 - np.std(prediction_changes)
        return stability
    
    def calculate_forecast_consistency(self, predictions, actual):
        """Расчет консистентности прогнозов"""
        # Ошибки прогнозов
        errors = predictions - actual
        
        # Консистентность = 1 - коэффициент вариации ошибок
        mean_error = np.mean(errors)
        std_error = np.std(errors)
        
        if mean_error == 0:
            consistency = 1 - std_error
        else:
            consistency = 1 - (std_error / abs(mean_error))
        
        return max(0, consistency)
```

## Автоматический анализ метрик

### 1. Система мониторинга метрик

```python
class MetricsMonitor:
    """Мониторинг метрик"""
    
    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            'sharpe_ratio': 1.0,
            'max_drawdown': 0.15,
            'volatility': 0.3,
            'accuracy': 0.7
        }
        self.alerts = []
    
    def monitor_metrics(self, returns, predictions=None):
        """Мониторинг метрик"""
        # Расчет метрик
        metrics = self._calculate_all_metrics(returns, predictions)
        
        # Сохранение истории
        self.metrics_history.append({
            'timestamp': datetime.now(),
            'metrics': metrics
        })
        
        # Проверка алертов
        alerts = self._check_metric_alerts(metrics)
        
        return {
            'metrics': metrics,
            'alerts': alerts
        }
    
    def _calculate_all_metrics(self, returns, predictions=None):
        """Расчет всех метрик"""
        metrics = {}
        
        # Базовые метрики
        return_metrics = ReturnMetrics()
        risk_metrics = RiskMetrics()
        efficiency_metrics = EfficiencyMetrics()
        
        metrics.update({
            'total_return': return_metrics.calculate_total_return(returns),
            'annualized_return': return_metrics.calculate_annualized_return(returns),
            'volatility': risk_metrics.calculate_volatility(returns),
            'max_drawdown': risk_metrics.calculate_max_drawdown(returns),
            'sharpe_ratio': efficiency_metrics.calculate_sharpe_ratio(returns)
        })
        
        # Метрики прогнозирования
        if predictions is not None:
            forecasting_metrics = ForecastingMetrics()
            metrics.update({
                'mape': forecasting_metrics.calculate_mape(predictions, returns),
                'rmse': forecasting_metrics.calculate_rmse(predictions, returns),
                'r2_score': forecasting_metrics.calculate_r2_score(predictions, returns)
            })
        
        return metrics
    
    def _check_metric_alerts(self, metrics):
        """Проверка алертов метрик"""
        alerts = []
        
        for metric_name, threshold in self.alert_thresholds.items():
            if metric_name in metrics:
                if metrics[metric_name] < threshold:
                    alerts.append({
                        'metric': metric_name,
                        'value': metrics[metric_name],
                        'threshold': threshold,
                        'severity': 'high' if metric_name in ['sharpe_ratio', 'accuracy'] else 'medium'
                    })
        
        return alerts
```

### 2. Автоматическая отчетность

```python
class MetricsReporter:
    """Автоматическая отчетность по метрикам"""
    
    def __init__(self):
        self.report_templates = {}
        self.report_schedules = {
            'daily': self._generate_daily_report,
            'weekly': self._generate_weekly_report,
            'monthly': self._generate_monthly_report
        }
    
    def generate_report(self, metrics, report_type='daily'):
        """Генерация отчета"""
        if report_type in self.report_schedules:
            return self.report_schedules[report_type](metrics)
        else:
            return self._generate_custom_report(metrics)
    
    def _generate_daily_report(self, metrics):
        """Генерация дневного отчета"""
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'daily',
            'summary': {
                'total_return': metrics.get('total_return', 0),
                'volatility': metrics.get('volatility', 0),
                'sharpe_ratio': metrics.get('sharpe_ratio', 0)
            },
            'alerts': metrics.get('alerts', [])
        }
        
        return report
    
    def _generate_weekly_report(self, metrics):
        """Генерация недельного отчета"""
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'weekly',
            'summary': {
                'weekly_return': metrics.get('weekly_return', 0),
                'max_drawdown': metrics.get('max_drawdown', 0),
                'consistency_ratio': metrics.get('consistency_ratio', 0)
            },
            'trends': self._analyze_trends(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }
        
        return report
    
    def _generate_monthly_report(self, metrics):
        """Генерация месячного отчета"""
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'monthly',
            'summary': {
                'monthly_return': metrics.get('monthly_return', 0),
                'annualized_return': metrics.get('annualized_return', 0),
                'volatility': metrics.get('volatility', 0),
                'sharpe_ratio': metrics.get('sharpe_ratio', 0)
            },
            'performance_analysis': self._analyze_performance(metrics),
            'risk_analysis': self._analyze_risks(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }
        
        return report
```

## Следующие шаги

После изучения метрик и анализа переходите к:
- **[17_examples.md](17_examples.md)** - Практические примеры

## Ключевые выводы

1. **Многоуровневые метрики** - измерение на разных уровнях
2. **Временные метрики** - анализ по периодам
3. **Сравнительные метрики** - сравнение с бенчмарками
4. **Прогнозные метрики** - оценка предсказательной способности
5. **Автоматический мониторинг** - непрерывный контроль метрик
6. **Автоматическая отчетность** - регулярные отчеты

---

**Важно:** Правильные метрики - это основа для принятия решений. Выбирайте метрики, которые соответствуют вашим целям и стратегии.
