# Правильное использование вероятностей в ML-моделях

**Автор:** NeoZorK (Shcherbyna Rostyslav)  
**Дата:** 2025  
**Местоположение:** Ukraine, Zaporizhzhya  
**Версия:** 1.0  

## Введение

Правильное использование вероятностей - это ключ к созданию робастных и прибыльных ML-моделей. Этот раздел посвящен глубокому пониманию того, как работать с вероятностями в AutoML Gluon и создавать на их основе эффективные торговые системы.

## Что такое вероятности в ML?

### Определение

Вероятности в машинном обучении - это численные оценки уверенности модели в своих предсказаниях. Они показывают, насколько модель уверена в правильности своего ответа.

### Типы вероятностей

```python
# Пример получения вероятностей в AutoML Gluon
from autogluon.tabular import TabularPredictor

# Создание предиктора
predictor = TabularPredictor(label='target', problem_type='binary')

# Обучение модели
predictor.fit(train_data)

# Получение предсказаний
predictions = predictor.predict(test_data)

# Получение вероятностей
probabilities = predictor.predict_proba(test_data)

print("Предсказания:", predictions)
print("Вероятности:", probabilities)
```

## Сильные стороны использования вероятностей

### 1. Калибровка уверенности

```python
class ProbabilityCalibration:
    """Калибровка вероятностей для повышения точности"""
    
    def __init__(self):
        self.calibration_methods = {}
    
    def calibrate_probabilities(self, probabilities, true_labels):
        """Калибровка вероятностей"""
        
        # Platt Scaling
        platt_calibrated = self.platt_scaling(probabilities, true_labels)
        
        # Isotonic Regression
        isotonic_calibrated = self.isotonic_regression(probabilities, true_labels)
        
        # Temperature Scaling
        temperature_calibrated = self.temperature_scaling(probabilities, true_labels)
        
        return {
            'platt': platt_calibrated,
            'isotonic': isotonic_calibrated,
            'temperature': temperature_calibrated
        }
    
    def platt_scaling(self, probabilities, true_labels):
        """Platt Scaling для калибровки"""
        
        from sklearn.calibration import CalibratedClassifierCV
        
        # Создание калиброванного классификатора
        calibrated_clf = CalibratedClassifierCV(
            base_estimator=None,  # AutoML Gluon модель
            method='sigmoid',
            cv=5
        )
        
        # Калибровка
        calibrated_clf.fit(probabilities.reshape(-1, 1), true_labels)
        calibrated_probs = calibrated_clf.predict_proba(probabilities.reshape(-1, 1))
        
        return calibrated_probs
    
    def isotonic_regression(self, probabilities, true_labels):
        """Isotonic Regression для калибровки"""
        
        from sklearn.isotonic import IsotonicRegression
        
        # Создание изотонической регрессии
        isotonic_reg = IsotonicRegression(out_of_bounds='clip')
        
        # Обучение на вероятностях
        isotonic_reg.fit(probabilities, true_labels)
        calibrated_probs = isotonic_reg.transform(probabilities)
        
        return calibrated_probs
    
    def temperature_scaling(self, probabilities, true_labels):
        """Temperature Scaling для калибровки"""
        
        import torch
        import torch.nn as nn
        
        # Temperature Scaling
        temperature = nn.Parameter(torch.ones(1) * 1.5)
        
        # Оптимизация температуры
        optimizer = torch.optim.LBFGS([temperature], lr=0.01, max_iter=50)
        
        def eval_loss():
            loss = nn.CrossEntropyLoss()(
                probabilities / temperature, 
                true_labels
            )
            loss.backward()
            return loss
        
        optimizer.step(eval_loss)
        
        # Применение температуры
        calibrated_probs = torch.softmax(probabilities / temperature, dim=1)
        
        return calibrated_probs.detach().numpy()
```

### 2. Адаптивное управление рисками

```python
class AdaptiveRiskManagement:
    """Адаптивное управление рисками на основе вероятностей"""
    
    def __init__(self):
        self.risk_thresholds = {}
        self.position_sizing = {}
    
    def calculate_position_size(self, probability, confidence_threshold=0.7):
        """Расчет размера позиции на основе вероятности"""
        
        # Базовый размер позиции
        base_size = 0.1  # 10% от капитала
        
        # Корректировка на основе вероятности
        if probability > confidence_threshold:
            # Высокая уверенность - увеличиваем размер
            position_size = base_size * (probability / confidence_threshold)
        else:
            # Низкая уверенность - уменьшаем размер
            position_size = base_size * (probability / confidence_threshold) * 0.5
        
        # Ограничение максимального размера
        position_size = min(position_size, 0.2)  # Максимум 20%
        
        return position_size
    
    def dynamic_stop_loss(self, probability, entry_price, volatility):
        """Динамический стоп-лосс на основе вероятности"""
        
        # Базовый стоп-лосс
        base_stop = entry_price * 0.95  # 5% стоп-лосс
        
        # Корректировка на основе вероятности
        if probability > 0.8:
            # Высокая уверенность - более широкий стоп-лосс
            stop_loss = entry_price * (1 - 0.03 * (1 - probability))
        else:
            # Низкая уверенность - более узкий стоп-лосс
            stop_loss = entry_price * (1 - 0.05 * (1 - probability))
        
        # Учет волатильности
        volatility_adjustment = 1 + volatility * 0.5
        stop_loss = stop_loss * volatility_adjustment
        
        return stop_loss
    
    def probability_based_hedging(self, probabilities, market_conditions):
        """Хеджирование на основе вероятностей"""
        
        # Анализ распределения вероятностей
        prob_distribution = self.analyze_probability_distribution(probabilities)
        
        # Определение необходимости хеджирования
        hedging_needed = self.determine_hedging_need(prob_distribution, market_conditions)
        
        if hedging_needed:
            # Расчет размера хеджа
            hedge_size = self.calculate_hedge_size(prob_distribution)
            
            # Выбор инструментов хеджирования
            hedge_instruments = self.select_hedge_instruments(market_conditions)
            
            return {
                'hedge_needed': True,
                'hedge_size': hedge_size,
                'instruments': hedge_instruments
            }
        
        return {'hedge_needed': False}
```

### 3. Ансамблирование на основе вероятностей

```python
class ProbabilityEnsemble:
    """Ансамблирование на основе вероятностей"""
    
    def __init__(self):
        self.ensemble_methods = {}
        self.weight_calculation = {}
    
    def weighted_ensemble(self, model_probabilities, model_weights):
        """Взвешенный ансамбль на основе вероятностей"""
        
        # Нормализация весов
        normalized_weights = model_weights / model_weights.sum()
        
        # Взвешенное объединение вероятностей
        ensemble_probability = np.average(
            model_probabilities, 
            weights=normalized_weights, 
            axis=0
        )
        
        return ensemble_probability
    
    def confidence_weighted_ensemble(self, model_probabilities, model_confidences):
        """Ансамбль с весами на основе уверенности"""
        
        # Расчет весов на основе уверенности
        confidence_weights = self.calculate_confidence_weights(model_confidences)
        
        # Взвешенное объединение
        ensemble_probability = np.average(
            model_probabilities,
            weights=confidence_weights,
            axis=0
        )
        
        return ensemble_probability
    
    def bayesian_ensemble(self, model_probabilities, model_uncertainties):
        """Байесовский ансамбль"""
        
        # Байесовское объединение
        bayesian_weights = self.calculate_bayesian_weights(model_uncertainties)
        
        # Объединение с учетом неопределенности
        ensemble_probability = np.average(
            model_probabilities,
            weights=bayesian_weights,
            axis=0
        )
        
        # Добавление неопределенности
        ensemble_uncertainty = self.calculate_ensemble_uncertainty(
            model_probabilities, 
            model_uncertainties
        )
        
        return {
            'probability': ensemble_probability,
            'uncertainty': ensemble_uncertainty
        }
```

### 4. Мониторинг дрифта вероятностей

```python
class ProbabilityDriftMonitor:
    """Мониторинг дрифта вероятностей"""
    
    def __init__(self):
        self.drift_detectors = {}
        self.baseline_distribution = None
    
    def detect_probability_drift(self, current_probabilities, baseline_probabilities):
        """Обнаружение дрифта вероятностей"""
        
        # Статистические тесты
        statistical_drift = self.statistical_drift_test(
            current_probabilities, 
            baseline_probabilities
        )
        
        # Тест Колмогорова-Смирнова
        ks_drift = self.ks_drift_test(
            current_probabilities, 
            baseline_probabilities
        )
        
        # Тест Вассерштейна
        wasserstein_drift = self.wasserstein_drift_test(
            current_probabilities, 
            baseline_probabilities
        )
        
        # Объединение результатов
        drift_detected = any([
            statistical_drift,
            ks_drift,
            wasserstein_drift
        ])
        
        return {
            'drift_detected': drift_detected,
            'statistical': statistical_drift,
            'ks': ks_drift,
            'wasserstein': wasserstein_drift
        }
    
    def statistical_drift_test(self, current, baseline):
        """Статистический тест дрифта"""
        
        from scipy import stats
        
        # t-тест для средних
        t_stat, t_pvalue = stats.ttest_ind(current, baseline)
        
        # Тест Манна-Уитни
        u_stat, u_pvalue = stats.mannwhitneyu(current, baseline)
        
        # Критерий дрифта
        drift_threshold = 0.05
        drift_detected = (t_pvalue < drift_threshold) or (u_pvalue < drift_threshold)
        
        return drift_detected
    
    def ks_drift_test(self, current, baseline):
        """Тест Колмогорова-Смирнова"""
        
        from scipy import stats
        
        # KS тест
        ks_stat, ks_pvalue = stats.ks_2samp(current, baseline)
        
        # Критерий дрифта
        drift_detected = ks_pvalue < 0.05
        
        return drift_detected
```

## Слабые стороны использования вероятностей

### 1. Переобучение на вероятностях

```python
class ProbabilityOverfittingPrevention:
    """Предотвращение переобучения на вероятностях"""
    
    def __init__(self):
        self.regularization_methods = {}
    
    def prevent_overfitting(self, probabilities, true_labels):
        """Предотвращение переобучения"""
        
        # L1 регуляризация
        l1_regularized = self.l1_regularization(probabilities, true_labels)
        
        # L2 регуляризация
        l2_regularized = self.l2_regularization(probabilities, true_labels)
        
        # Dropout для вероятностей
        dropout_regularized = self.dropout_regularization(probabilities, true_labels)
        
        return {
            'l1': l1_regularized,
            'l2': l2_regularized,
            'dropout': dropout_regularized
        }
    
    def l1_regularization(self, probabilities, true_labels):
        """L1 регуляризация"""
        
        # Добавление L1 штрафа
        l1_penalty = np.sum(np.abs(probabilities))
        
        # Обновление вероятностей
        regularized_probs = probabilities - 0.01 * l1_penalty
        
        return regularized_probs
    
    def dropout_regularization(self, probabilities, true_labels):
        """Dropout регуляризация"""
        
        # Случайное обнуление части вероятностей
        dropout_mask = np.random.binomial(1, 0.5, probabilities.shape)
        regularized_probs = probabilities * dropout_mask
        
        return regularized_probs
```

### 2. Неправильная интерпретация вероятностей

```python
class ProbabilityInterpretation:
    """Правильная интерпретация вероятностей"""
    
    def __init__(self):
        self.interpretation_guidelines = {}
    
    def interpret_probabilities(self, probabilities, context):
        """Правильная интерпретация вероятностей"""
        
        # Анализ контекста
        context_analysis = self.analyze_context(context)
        
        # Корректировка интерпретации
        corrected_interpretation = self.correct_interpretation(
            probabilities, 
            context_analysis
        )
        
        return corrected_interpretation
    
    def analyze_context(self, context):
        """Анализ контекста для интерпретации"""
        
        # Рыночные условия
        market_conditions = context.get('market_conditions', {})
        
        # Временные факторы
        temporal_factors = context.get('temporal_factors', {})
        
        # Внешние факторы
        external_factors = context.get('external_factors', {})
        
        return {
            'market': market_conditions,
            'temporal': temporal_factors,
            'external': external_factors
        }
    
    def correct_interpretation(self, probabilities, context_analysis):
        """Корректировка интерпретации"""
        
        # Корректировка на основе рыночных условий
        market_corrected = self.market_correction(probabilities, context_analysis['market'])
        
        # Корректировка на основе временных факторов
        temporal_corrected = self.temporal_correction(market_corrected, context_analysis['temporal'])
        
        # Корректировка на основе внешних факторов
        external_corrected = self.external_correction(temporal_corrected, context_analysis['external'])
        
        return external_corrected
```

### 3. Проблемы с калибровкой

```python
class CalibrationIssues:
    """Проблемы с калибровкой вероятностей"""
    
    def __init__(self):
        self.calibration_problems = {}
    
    def identify_calibration_issues(self, probabilities, true_labels):
        """Идентификация проблем калибровки"""
        
        # Анализ калибровочной кривой
        calibration_curve = self.analyze_calibration_curve(probabilities, true_labels)
        
        # Анализ надежности
        reliability_analysis = self.analyze_reliability(probabilities, true_labels)
        
        # Анализ резолюции
        resolution_analysis = self.analyze_resolution(probabilities, true_labels)
        
        return {
            'calibration_curve': calibration_curve,
            'reliability': reliability_analysis,
            'resolution': resolution_analysis
        }
    
    def analyze_calibration_curve(self, probabilities, true_labels):
        """Анализ калибровочной кривой"""
        
        from sklearn.calibration import calibration_curve
        
        # Построение калибровочной кривой
        fraction_of_positives, mean_predicted_value = calibration_curve(
            true_labels, 
            probabilities, 
            n_bins=10
        )
        
        # Анализ отклонений
        deviations = np.abs(fraction_of_positives - mean_predicted_value)
        
        # Критерий плохой калибровки
        bad_calibration = np.mean(deviations) > 0.1
        
        return {
            'curve': (fraction_of_positives, mean_predicted_value),
            'deviations': deviations,
            'bad_calibration': bad_calibration
        }
```

## Лучшие практики использования вероятностей

### 1. Валидация вероятностей

```python
class ProbabilityValidation:
    """Валидация вероятностей"""
    
    def __init__(self):
        self.validation_methods = {}
    
    def validate_probabilities(self, probabilities, true_labels):
        """Валидация вероятностей"""
        
        # Кросс-валидация
        cv_validation = self.cross_validation(probabilities, true_labels)
        
        # Временная валидация
        temporal_validation = self.temporal_validation(probabilities, true_labels)
        
        # Стохастическая валидация
        stochastic_validation = self.stochastic_validation(probabilities, true_labels)
        
        return {
            'cv': cv_validation,
            'temporal': temporal_validation,
            'stochastic': stochastic_validation
        }
    
    def cross_validation(self, probabilities, true_labels):
        """Кросс-валидация вероятностей"""
        
        from sklearn.model_selection import cross_val_score
        
        # Кросс-валидация с калибровкой
        cv_scores = cross_val_score(
            probabilities, 
            true_labels, 
            cv=5, 
            scoring='neg_log_loss'
        )
        
        return {
            'scores': cv_scores,
            'mean_score': np.mean(cv_scores),
            'std_score': np.std(cv_scores)
        }
```

### 2. Мониторинг производительности

```python
class ProbabilityMonitoring:
    """Мониторинг производительности вероятностей"""
    
    def __init__(self):
        self.monitoring_metrics = {}
    
    def monitor_performance(self, probabilities, true_labels):
        """Мониторинг производительности"""
        
        # Логарифмическая потеря
        log_loss = self.calculate_log_loss(probabilities, true_labels)
        
        # Brier Score
        brier_score = self.calculate_brier_score(probabilities, true_labels)
        
        # Калибровочная ошибка
        calibration_error = self.calculate_calibration_error(probabilities, true_labels)
        
        return {
            'log_loss': log_loss,
            'brier_score': brier_score,
            'calibration_error': calibration_error
        }
    
    def calculate_log_loss(self, probabilities, true_labels):
        """Расчет логарифмической потери"""
        
        from sklearn.metrics import log_loss
        
        # Логарифмическая потеря
        loss = log_loss(true_labels, probabilities)
        
        return loss
    
    def calculate_brier_score(self, probabilities, true_labels):
        """Расчет Brier Score"""
        
        from sklearn.metrics import brier_score_loss
        
        # Brier Score
        score = brier_score_loss(true_labels, probabilities)
        
        return score
```

## Практические примеры

### 1. Торговая система на вероятностях

```python
class ProbabilityTradingSystem:
    """Торговая система на основе вероятностей"""
    
    def __init__(self):
        self.probability_thresholds = {}
        self.risk_management = {}
    
    def generate_trading_signals(self, probabilities, market_data):
        """Генерация торговых сигналов"""
        
        # Анализ вероятностей
        prob_analysis = self.analyze_probabilities(probabilities)
        
        # Генерация сигналов
        signals = self.generate_signals(prob_analysis, market_data)
        
        # Управление рисками
        risk_adjusted_signals = self.adjust_for_risk(signals, probabilities)
        
        return risk_adjusted_signals
    
    def analyze_probabilities(self, probabilities):
        """Анализ вероятностей"""
        
        # Статистические характеристики
        mean_prob = np.mean(probabilities)
        std_prob = np.std(probabilities)
        max_prob = np.max(probabilities)
        min_prob = np.min(probabilities)
        
        # Распределение вероятностей
        prob_distribution = self.analyze_distribution(probabilities)
        
        return {
            'mean': mean_prob,
            'std': std_prob,
            'max': max_prob,
            'min': min_prob,
            'distribution': prob_distribution
        }
    
    def generate_signals(self, prob_analysis, market_data):
        """Генерация сигналов"""
        
        signals = []
        
        for i, prob in enumerate(prob_analysis['probabilities']):
            if prob > 0.8:
                # Высокая уверенность - сильный сигнал
                signal = {
                    'type': 'BUY',
                    'strength': 'STRONG',
                    'confidence': prob,
                    'timestamp': market_data[i]['timestamp']
                }
            elif prob > 0.6:
                # Средняя уверенность - умеренный сигнал
                signal = {
                    'type': 'BUY',
                    'strength': 'MODERATE',
                    'confidence': prob,
                    'timestamp': market_data[i]['timestamp']
                }
            elif prob < 0.2:
                # Низкая уверенность - сигнал продажи
                signal = {
                    'type': 'SELL',
                    'strength': 'STRONG',
                    'confidence': 1 - prob,
                    'timestamp': market_data[i]['timestamp']
                }
            else:
                # Неопределенность - отсутствие сигнала
                signal = {
                    'type': 'HOLD',
                    'strength': 'NONE',
                    'confidence': 0.5,
                    'timestamp': market_data[i]['timestamp']
                }
            
            signals.append(signal)
        
        return signals
```

### 2. Портфельное управление

```python
class ProbabilityPortfolioManagement:
    """Управление портфелем на основе вероятностей"""
    
    def __init__(self):
        self.portfolio_weights = {}
        self.risk_budget = {}
    
    def optimize_portfolio(self, asset_probabilities, risk_budget):
        """Оптимизация портфеля"""
        
        # Расчет весов на основе вероятностей
        weights = self.calculate_weights(asset_probabilities)
        
        # Корректировка на риск
        risk_adjusted_weights = self.adjust_for_risk(weights, risk_budget)
        
        # Оптимизация распределения
        optimized_weights = self.optimize_allocation(risk_adjusted_weights)
        
        return optimized_weights
    
    def calculate_weights(self, asset_probabilities):
        """Расчет весов на основе вероятностей"""
        
        # Нормализация вероятностей
        normalized_probs = asset_probabilities / np.sum(asset_probabilities)
        
        # Корректировка на дисперсию
        variance_adjusted = self.adjust_for_variance(normalized_probs)
        
        return variance_adjusted
    
    def adjust_for_risk(self, weights, risk_budget):
        """Корректировка на риск"""
        
        # Расчет риска портфеля
        portfolio_risk = self.calculate_portfolio_risk(weights)
        
        # Корректировка весов
        if portfolio_risk > risk_budget:
            # Уменьшение весов
            adjustment_factor = risk_budget / portfolio_risk
            adjusted_weights = weights * adjustment_factor
        else:
            adjusted_weights = weights
        
        return adjusted_weights
```

## Заключение

Правильное использование вероятностей - это ключ к созданию робастных и прибыльных ML-моделей. Понимание сильных и слабых сторон позволяет создавать более эффективные торговые системы.

### Ключевые принципы:

1. **Калибровка** - всегда калибруйте вероятности
2. **Валидация** - проверяйте качество вероятностей
3. **Мониторинг** - отслеживайте дрифт вероятностей
4. **Интерпретация** - правильно интерпретируйте результаты
5. **Риск-менеджмент** - используйте вероятности для управления рисками

Следуя этим принципам, вы сможете создавать более точные и прибыльные торговые системы.
