# 18.4. Мониторинг и метрики для достижения 100% прибыли

## 📊 Система мониторинга производительности

```python
# src/monitoring/performance.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

class PerformanceMonitor:
    """Мониторинг производительности системы"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.metrics_history = []
        self.alerts = []
        self.monthly_target = 1.0  # 100% в месяц
        self.daily_target = 0.033  # ~3.3% в день
        
    def calculate_metrics(self, positions: List[Dict], current_balance: float, initial_balance: float) -> Dict:
        """Расчет всех метрик производительности"""
        try:
            metrics = {}
            
            # Базовые метрики
            metrics['total_return'] = (current_balance - initial_balance) / initial_balance
            metrics['current_balance'] = current_balance
            metrics['initial_balance'] = initial_balance
            
            # Временные метрики
            metrics['daily_return'] = self._calculate_daily_return(positions)
            metrics['weekly_return'] = self._calculate_weekly_return(positions)
            metrics['monthly_return'] = self._calculate_monthly_return(positions)
            metrics['annualized_return'] = self._calculate_annualized_return(positions)
            
            # Риск-метрики
            metrics['sharpe_ratio'] = self._calculate_sharpe_ratio(positions)
            metrics['max_drawdown'] = self._calculate_max_drawdown(positions)
            metrics['var_95'] = self._calculate_var(positions, 0.95)
            metrics['var_99'] = self._calculate_var(positions, 0.99)
            
            # Торговые метрики
            metrics['win_rate'] = self._calculate_win_rate(positions)
            metrics['profit_factor'] = self._calculate_profit_factor(positions)
            metrics['avg_win'] = self._calculate_avg_win(positions)
            metrics['avg_loss'] = self._calculate_avg_loss(positions)
            
            # Метрики робастности
            metrics['consistency'] = self._calculate_consistency(positions)
            metrics['stability'] = self._calculate_stability(positions)
            metrics['adaptability'] = self._calculate_adaptability(positions)
            
            # Целевые метрики
            metrics['target_achievement'] = self._calculate_target_achievement(metrics)
            metrics['performance_score'] = self._calculate_performance_score(metrics)
            
            # Временные метки
            metrics['timestamp'] = datetime.now()
            metrics['calculation_time'] = datetime.now()
            
            # Сохранение в историю
            self.metrics_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            return {}
    
    def _calculate_daily_return(self, positions: List[Dict]) -> float:
        """Расчет дневной доходности"""
        try:
            if not positions:
                return 0.0
            
            # Получение позиций за последний день
            yesterday = datetime.now() - timedelta(days=1)
            daily_positions = [p for p in positions if p['timestamp'] >= yesterday]
            
            if not daily_positions:
                return 0.0
            
            # Расчет доходности
            total_pnl = sum(p['pnl'] for p in daily_positions if 'pnl' in p)
            return total_pnl
            
        except Exception as e:
            self.logger.error(f"Error calculating daily return: {e}")
            return 0.0
    
    def _calculate_weekly_return(self, positions: List[Dict]) -> float:
        """Расчет недельной доходности"""
        try:
            if not positions:
                return 0.0
            
            # Получение позиций за последнюю неделю
            week_ago = datetime.now() - timedelta(weeks=1)
            weekly_positions = [p for p in positions if p['timestamp'] >= week_ago]
            
            if not weekly_positions:
                return 0.0
            
            # Расчет доходности
            total_pnl = sum(p['pnl'] for p in weekly_positions if 'pnl' in p)
            return total_pnl
            
        except Exception as e:
            self.logger.error(f"Error calculating weekly return: {e}")
            return 0.0
    
    def _calculate_monthly_return(self, positions: List[Dict]) -> float:
        """Расчет месячной доходности"""
        try:
            if not positions:
                return 0.0
            
            # Получение позиций за последний месяц
            month_ago = datetime.now() - timedelta(days=30)
            monthly_positions = [p for p in positions if p['timestamp'] >= month_ago]
            
            if not monthly_positions:
                return 0.0
            
            # Расчет доходности
            total_pnl = sum(p['pnl'] for p in monthly_positions if 'pnl' in p)
            return total_pnl
            
        except Exception as e:
            self.logger.error(f"Error calculating monthly return: {e}")
            return 0.0
    
    def _calculate_annualized_return(self, positions: List[Dict]) -> float:
        """Расчет годовой доходности"""
        try:
            if not positions:
                return 0.0
            
            # Получение всех позиций
            all_positions = [p for p in positions if 'pnl' in p]
            
            if not all_positions:
                return 0.0
            
            # Расчет общего PnL
            total_pnl = sum(p['pnl'] for p in all_positions)
            
            # Расчет времени
            if len(all_positions) > 1:
                start_time = min(p['timestamp'] for p in all_positions)
                end_time = max(p['timestamp'] for p in all_positions)
                time_diff = (end_time - start_time).days / 365.25
                
                if time_diff > 0:
                    annualized_return = total_pnl / time_diff
                    return annualized_return
            
            return total_pnl
            
        except Exception as e:
            self.logger.error(f"Error calculating annualized return: {e}")
            return 0.0
    
    def _calculate_sharpe_ratio(self, positions: List[Dict]) -> float:
        """Расчет коэффициента Шарпа"""
        try:
            if not positions:
                return 0.0
            
            # Получение доходностей
            returns = [p['pnl'] for p in positions if 'pnl' in p]
            
            if len(returns) < 2:
                return 0.0
            
            # Расчет среднего и стандартного отклонения
            mean_return = np.mean(returns)
            std_return = np.std(returns)
            
            if std_return == 0:
                return 0.0
            
            # Коэффициент Шарпа (предполагаем безрисковую ставку = 0)
            sharpe_ratio = mean_return / std_return
            return sharpe_ratio
            
        except Exception as e:
            self.logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, positions: List[Dict]) -> float:
        """Расчет максимальной просадки"""
        try:
            if not positions:
                return 0.0
            
            # Получение кумулятивных доходностей
            returns = [p['pnl'] for p in positions if 'pnl' in p]
            
            if not returns:
                return 0.0
            
            # Расчет кумулятивных доходностей
            cumulative_returns = np.cumsum(returns)
            
            # Расчет максимальной просадки
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdowns = cumulative_returns - running_max
            max_drawdown = np.min(drawdowns)
            
            return abs(max_drawdown)
            
        except Exception as e:
            self.logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def _calculate_var(self, positions: List[Dict], confidence_level: float) -> float:
        """Расчет Value at Risk"""
        try:
            if not positions:
                return 0.0
            
            # Получение доходностей
            returns = [p['pnl'] for p in positions if 'pnl' in p]
            
            if not returns:
                return 0.0
            
            # Расчет VaR
            var = np.percentile(returns, (1 - confidence_level) * 100)
            return abs(var)
            
        except Exception as e:
            self.logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def _calculate_win_rate(self, positions: List[Dict]) -> float:
        """Расчет процента выигрышных сделок"""
        try:
            if not positions:
                return 0.0
            
            # Получение PnL
            pnls = [p['pnl'] for p in positions if 'pnl' in p]
            
            if not pnls:
                return 0.0
            
            # Подсчет выигрышных сделок
            winning_trades = sum(1 for pnl in pnls if pnl > 0)
            total_trades = len(pnls)
            
            win_rate = winning_trades / total_trades if total_trades > 0 else 0.0
            return win_rate
            
        except Exception as e:
            self.logger.error(f"Error calculating win rate: {e}")
            return 0.0
    
    def _calculate_profit_factor(self, positions: List[Dict]) -> float:
        """Расчет фактора прибыли"""
        try:
            if not positions:
                return 0.0
            
            # Получение PnL
            pnls = [p['pnl'] for p in positions if 'pnl' in p]
            
            if not pnls:
                return 0.0
            
            # Разделение на прибыльные и убыточные
            profits = [pnl for pnl in pnls if pnl > 0]
            losses = [abs(pnl) for pnl in pnls if pnl < 0]
            
            total_profit = sum(profits) if profits else 0
            total_loss = sum(losses) if losses else 0
            
            if total_loss == 0:
                return float('inf') if total_profit > 0 else 0.0
            
            profit_factor = total_profit / total_loss
            return profit_factor
            
        except Exception as e:
            self.logger.error(f"Error calculating profit factor: {e}")
            return 0.0
    
    def _calculate_avg_win(self, positions: List[Dict]) -> float:
        """Расчет средней прибыли"""
        try:
            if not positions:
                return 0.0
            
            # Получение прибыльных PnL
            profits = [p['pnl'] for p in positions if 'pnl' in p and p['pnl'] > 0]
            
            if not profits:
                return 0.0
            
            avg_win = np.mean(profits)
            return avg_win
            
        except Exception as e:
            self.logger.error(f"Error calculating average win: {e}")
            return 0.0
    
    def _calculate_avg_loss(self, positions: List[Dict]) -> float:
        """Расчет среднего убытка"""
        try:
            if not positions:
                return 0.0
            
            # Получение убыточных PnL
            losses = [p['pnl'] for p in positions if 'pnl' in p and p['pnl'] < 0]
            
            if not losses:
                return 0.0
            
            avg_loss = np.mean(losses)
            return avg_loss
            
        except Exception as e:
            self.logger.error(f"Error calculating average loss: {e}")
            return 0.0
    
    def _calculate_consistency(self, positions: List[Dict]) -> float:
        """Расчет консистентности"""
        try:
            if not positions:
                return 0.0
            
            # Получение доходностей
            returns = [p['pnl'] for p in positions if 'pnl' in p]
            
            if len(returns) < 2:
                return 0.0
            
            # Расчет коэффициента вариации
            mean_return = np.mean(returns)
            std_return = np.std(returns)
            
            if mean_return == 0:
                return 0.0
            
            consistency = 1 - (std_return / abs(mean_return))
            return max(0, consistency)
            
        except Exception as e:
            self.logger.error(f"Error calculating consistency: {e}")
            return 0.0
    
    def _calculate_stability(self, positions: List[Dict]) -> float:
        """Расчет стабильности"""
        try:
            if not positions:
                return 0.0
            
            # Получение доходностей
            returns = [p['pnl'] for p in positions if 'pnl' in p]
            
            if len(returns) < 2:
                return 0.0
            
            # Расчет стабильности как обратная величина волатильности
            volatility = np.std(returns)
            stability = 1 / (1 + volatility)
            
            return stability
            
        except Exception as e:
            self.logger.error(f"Error calculating stability: {e}")
            return 0.0
    
    def _calculate_adaptability(self, positions: List[Dict]) -> float:
        """Расчет адаптивности"""
        try:
            if not positions:
                return 0.0
            
            # Получение доходностей
            returns = [p['pnl'] for p in positions if 'pnl' in p]
            
            if len(returns) < 10:
                return 0.0
            
            # Расчет адаптивности как способность к обучению
            # Используем корреляцию между последовательными периодами
            half_len = len(returns) // 2
            first_half = returns[:half_len]
            second_half = returns[half_len:]
            
            if len(first_half) > 1 and len(second_half) > 1:
                correlation = np.corrcoef(first_half, second_half)[0, 1]
                adaptability = abs(correlation)
            else:
                adaptability = 0.0
            
            return adaptability
            
        except Exception as e:
            self.logger.error(f"Error calculating adaptability: {e}")
            return 0.0
    
    def _calculate_target_achievement(self, metrics: Dict) -> float:
        """Расчет достижения целей"""
        try:
            # Проверка месячной цели
            monthly_return = metrics.get('monthly_return', 0)
            monthly_achievement = min(monthly_return / self.monthly_target, 1.0)
            
            # Проверка дневной цели
            daily_return = metrics.get('daily_return', 0)
            daily_achievement = min(daily_return / self.daily_target, 1.0)
            
            # Общее достижение целей
            target_achievement = (monthly_achievement + daily_achievement) / 2
            
            return target_achievement
            
        except Exception as e:
            self.logger.error(f"Error calculating target achievement: {e}")
            return 0.0
    
    def _calculate_performance_score(self, metrics: Dict) -> float:
        """Расчет общего балла производительности"""
        try:
            # Веса для разных метрик
            weights = {
                'total_return': 0.3,
                'sharpe_ratio': 0.2,
                'win_rate': 0.15,
                'profit_factor': 0.15,
                'consistency': 0.1,
                'stability': 0.1
            }
            
            # Нормализация метрик
            normalized_metrics = {}
            
            # Общая доходность (0-1)
            total_return = metrics.get('total_return', 0)
            normalized_metrics['total_return'] = min(total_return / 2.0, 1.0)  # 200% = 1.0
            
            # Коэффициент Шарпа (0-1)
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            normalized_metrics['sharpe_ratio'] = min(sharpe_ratio / 3.0, 1.0)  # 3.0 = 1.0
            
            # Процент выигрышных сделок (0-1)
            win_rate = metrics.get('win_rate', 0)
            normalized_metrics['win_rate'] = win_rate
            
            # Фактор прибыли (0-1)
            profit_factor = metrics.get('profit_factor', 0)
            normalized_metrics['profit_factor'] = min(profit_factor / 3.0, 1.0)  # 3.0 = 1.0
            
            # Консистентность (0-1)
            consistency = metrics.get('consistency', 0)
            normalized_metrics['consistency'] = consistency
            
            # Стабильность (0-1)
            stability = metrics.get('stability', 0)
            normalized_metrics['stability'] = stability
            
            # Расчет взвешенного балла
            performance_score = sum(
                weights[metric] * normalized_metrics[metric]
                for metric in weights
            )
            
            return performance_score
            
        except Exception as e:
            self.logger.error(f"Error calculating performance score: {e}")
            return 0.0
    
    def check_alerts(self, metrics: Dict) -> List[Dict]:
        """Проверка алертов"""
        alerts = []
        
        try:
            # Алерт по достижению месячной цели
            monthly_return = metrics.get('monthly_return', 0)
            if monthly_return >= self.monthly_target:
                alerts.append({
                    'type': 'success',
                    'message': f'Monthly target achieved: {monthly_return:.2%}',
                    'timestamp': datetime.now()
                })
            
            # Алерт по превышению максимальной просадки
            max_drawdown = metrics.get('max_drawdown', 0)
            if max_drawdown > 0.2:  # 20%
                alerts.append({
                    'type': 'warning',
                    'message': f'Max drawdown exceeded: {max_drawdown:.2%}',
                    'timestamp': datetime.now()
                })
            
            # Алерт по низкому коэффициенту Шарпа
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            if sharpe_ratio < 1.0:
                alerts.append({
                    'type': 'warning',
                    'message': f'Low Sharpe ratio: {sharpe_ratio:.2f}',
                    'timestamp': datetime.now()
                })
            
            # Алерт по низкому проценту выигрышных сделок
            win_rate = metrics.get('win_rate', 0)
            if win_rate < 0.5:
                alerts.append({
                    'type': 'warning',
                    'message': f'Low win rate: {win_rate:.2%}',
                    'timestamp': datetime.now()
                })
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
            return []
    
    def generate_report(self, metrics: Dict) -> str:
        """Генерация отчета"""
        try:
            report = f"""
# NeoZorK 100% System Performance Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Key Metrics

### Returns
- **Total Return**: {metrics.get('total_return', 0):.2%}
- **Daily Return**: {metrics.get('daily_return', 0):.2%}
- **Weekly Return**: {metrics.get('weekly_return', 0):.2%}
- **Monthly Return**: {metrics.get('monthly_return', 0):.2%}
- **Annualized Return**: {metrics.get('annualized_return', 0):.2%}

### Risk Metrics
- **Sharpe Ratio**: {metrics.get('sharpe_ratio', 0):.2f}
- **Max Drawdown**: {metrics.get('max_drawdown', 0):.2%}
- **VaR 95%**: {metrics.get('var_95', 0):.2%}
- **VaR 99%**: {metrics.get('var_99', 0):.2%}

### Trading Metrics
- **Win Rate**: {metrics.get('win_rate', 0):.2%}
- **Profit Factor**: {metrics.get('profit_factor', 0):.2f}
- **Average Win**: {metrics.get('avg_win', 0):.2f}
- **Average Loss**: {metrics.get('avg_loss', 0):.2f}

### Robustness Metrics
- **Consistency**: {metrics.get('consistency', 0):.2f}
- **Stability**: {metrics.get('stability', 0):.2f}
- **Adaptability**: {metrics.get('adaptability', 0):.2f}

### Target Achievement
- **Target Achievement**: {metrics.get('target_achievement', 0):.2%}
- **Performance Score**: {metrics.get('performance_score', 0):.2f}

## 🎯 Status
"""
            
            # Добавление статуса
            performance_score = metrics.get('performance_score', 0)
            if performance_score >= 0.8:
                report += "🟢 **EXCELLENT** - System performing above expectations\n"
            elif performance_score >= 0.6:
                report += "🟡 **GOOD** - System performing well\n"
            elif performance_score >= 0.4:
                report += "🟠 **FAIR** - System needs improvement\n"
            else:
                report += "🔴 **POOR** - System requires immediate attention\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return "Error generating report"
    
    def create_dashboard(self, metrics: Dict) -> go.Figure:
        """Создание дашборда"""
        try:
            # Создание субплотов
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=('Returns Over Time', 'Risk Metrics', 'Trading Performance', 'Robustness Metrics', 'Target Achievement', 'Performance Score'),
                specs=[[{"type": "scatter"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "indicator"}]]
            )
            
            # График доходности
            if self.metrics_history:
                timestamps = [m['timestamp'] for m in self.metrics_history]
                returns = [m['total_return'] for m in self.metrics_history]
                
                fig.add_trace(
                    go.Scatter(x=timestamps, y=returns, name='Total Return', line=dict(color='blue')),
                    row=1, col=1
                )
            
            # Метрики риска
            risk_metrics = ['sharpe_ratio', 'max_drawdown', 'var_95', 'var_99']
            risk_values = [metrics.get(m, 0) for m in risk_metrics]
            
            fig.add_trace(
                go.Bar(x=risk_metrics, y=risk_values, name='Risk Metrics', marker_color='red'),
                row=1, col=2
            )
            
            # Торговые метрики
            trading_metrics = ['win_rate', 'profit_factor', 'avg_win', 'avg_loss']
            trading_values = [metrics.get(m, 0) for m in trading_metrics]
            
            fig.add_trace(
                go.Bar(x=trading_metrics, y=trading_values, name='Trading Metrics', marker_color='green'),
                row=2, col=1
            )
            
            # Метрики робастности
            robustness_metrics = ['consistency', 'stability', 'adaptability']
            robustness_values = [metrics.get(m, 0) for m in robustness_metrics]
            
            fig.add_trace(
                go.Bar(x=robustness_metrics, y=robustness_values, name='Robustness Metrics', marker_color='orange'),
                row=2, col=2
            )
            
            # Достижение целей
            target_metrics = ['monthly_target', 'daily_target']
            target_values = [self.monthly_target, self.daily_target]
            achievement_values = [metrics.get('monthly_return', 0), metrics.get('daily_return', 0)]
            
            fig.add_trace(
                go.Bar(x=target_metrics, y=target_values, name='Targets', marker_color='lightblue'),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Bar(x=target_metrics, y=achievement_values, name='Achievement', marker_color='darkblue'),
                row=3, col=1
            )
            
            # Индикатор производительности
            performance_score = metrics.get('performance_score', 0)
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=performance_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Performance Score"},
                    gauge={'axis': {'range': [None, 1]},
                           'bar': {'color': "darkblue"},
                           'steps': [{'range': [0, 0.4], 'color': "lightgray"},
                                   {'range': [0.4, 0.6], 'color': "yellow"},
                                   {'range': [0.6, 0.8], 'color': "orange"},
                                   {'range': [0.8, 1], 'color': "green"}],
                           'threshold': {'line': {'color': "red", 'width': 4},
                                       'thickness': 0.75, 'value': 0.8}}
                ),
                row=3, col=2
            )
            
            # Обновление макета
            fig.update_layout(
                title_text="NeoZorK 100% System Dashboard",
                showlegend=True,
                height=800
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating dashboard: {e}")
            return go.Figure()
```

## 🚨 Система алертов

```python
# src/monitoring/alerts.py
import smtplib
import requests
import logging
from datetime import datetime
from typing import Dict, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertManager:
    """Менеджер алертов для системы"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.alert_history = []
        
    def send_alert(self, alert: Dict):
        """Отправка алерта"""
        try:
            # Добавление в историю
            self.alert_history.append(alert)
            
            # Отправка через разные каналы
            self._send_email_alert(alert)
            self._send_telegram_alert(alert)
            self._send_discord_alert(alert)
            
            self.logger.info(f"Alert sent: {alert['message']}")
            
        except Exception as e:
            self.logger.error(f"Error sending alert: {e}")
    
    def _send_email_alert(self, alert: Dict):
        """Отправка email алерта"""
        try:
            email_config = self.config.get('monitoring', {}).get('email', {})
            
            if not email_config.get('enabled', False):
                return
            
            # Создание сообщения
            msg = MIMEMultipart()
            msg['From'] = email_config['email']
            msg['To'] = email_config['email']
            msg['Subject'] = f"NeoZorK 100% System Alert - {alert['type'].upper()}"
            
            # Тело сообщения
            body = f"""
            Alert Type: {alert['type']}
            Message: {alert['message']}
            Timestamp: {alert['timestamp']}
            
            Please check the system immediately.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Отправка
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['email'], email_config['password'])
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            self.logger.error(f"Error sending email alert: {e}")
    
    def _send_telegram_alert(self, alert: Dict):
        """Отправка Telegram алерта"""
        try:
            telegram_config = self.config.get('monitoring', {}).get('telegram', {})
            
            if not telegram_config.get('enabled', False):
                return
            
            # Формирование сообщения
            message = f"""
            🚨 **NeoZorK 100% System Alert**
            
            **Type**: {alert['type'].upper()}
            **Message**: {alert['message']}
            **Time**: {alert['timestamp']}
            
            Please check the system immediately.
            """
            
            # Отправка
            url = f"https://api.telegram.org/bot{telegram_config['bot_token']}/sendMessage"
            data = {
                'chat_id': telegram_config['chat_id'],
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
        except Exception as e:
            self.logger.error(f"Error sending Telegram alert: {e}")
    
    def _send_discord_alert(self, alert: Dict):
        """Отправка Discord алерта"""
        try:
            discord_config = self.config.get('monitoring', {}).get('discord', {})
            
            if not discord_config.get('enabled', False):
                return
            
            # Формирование сообщения
            message = {
                "content": f"🚨 **NeoZorK 100% System Alert**",
                "embeds": [{
                    "title": f"Alert Type: {alert['type'].upper()}",
                    "description": alert['message'],
                    "color": 0xff0000 if alert['type'] == 'error' else 0xffa500,
                    "timestamp": alert['timestamp'].isoformat(),
                    "fields": [
                        {"name": "Type", "value": alert['type'], "inline": True},
                        {"name": "Time", "value": alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S'), "inline": True}
                    ]
                }]
            }
            
            # Отправка
            response = requests.post(discord_config['webhook_url'], json=message)
            response.raise_for_status()
            
        except Exception as e:
            self.logger.error(f"Error sending Discord alert: {e}")
    
    def send_trade_alert(self, trade: Dict):
        """Отправка алерта о сделке"""
        try:
            alert = {
                'type': 'trade',
                'message': f"Trade executed: {trade['type']} {trade['amount']} at {trade['price']}",
                'timestamp': datetime.now()
            }
            
            self.send_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Error sending trade alert: {e}")
    
    def send_risk_alert(self, risk_status: Dict):
        """Отправка алерта о рисках"""
        try:
            alert = {
                'type': 'risk',
                'message': f"Risk limits exceeded: {risk_status['message']}",
                'timestamp': datetime.now()
            }
            
            self.send_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Error sending risk alert: {e}")
    
    def send_performance_alert(self, performance: Dict):
        """Отправка алерта о производительности"""
        try:
            performance_score = performance.get('performance_score', 0)
            
            if performance_score < 0.4:
                alert = {
                    'type': 'performance',
                    'message': f"Low performance score: {performance_score:.2f}",
                    'timestamp': datetime.now()
                }
                
                self.send_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Error sending performance alert: {e}")
```

## 📈 Система логирования

```python
# src/monitoring/logging_system.py
import logging
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class LoggingSystem:
    """Система логирования для NeoZorK 100% System"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Настройка логирования
        self._setup_logging()
        
    def _setup_logging(self):
        """Настройка системы логирования"""
        # Основной логгер
        main_logger = logging.getLogger('neozork_100_percent')
        main_logger.setLevel(logging.INFO)
        
        # Обработчик файла
        file_handler = logging.FileHandler(self.log_dir / 'neozork_100_percent.log')
        file_handler.setLevel(logging.INFO)
        
        # Обработчик консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Форматтер
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Добавление обработчиков
        main_logger.addHandler(file_handler)
        main_logger.addHandler(console_handler)
        
        # Логгер для торговых операций
        trade_logger = logging.getLogger('neozork_trades')
        trade_logger.setLevel(logging.INFO)
        
        trade_handler = logging.FileHandler(self.log_dir / 'trades.log')
        trade_handler.setLevel(logging.INFO)
        trade_handler.setFormatter(formatter)
        trade_logger.addHandler(trade_handler)
        
        # Логгер для производительности
        perf_logger = logging.getLogger('neozork_performance')
        perf_logger.setLevel(logging.INFO)
        
        perf_handler = logging.FileHandler(self.log_dir / 'performance.log')
        perf_handler.setLevel(logging.INFO)
        perf_handler.setFormatter(formatter)
        perf_logger.addHandler(perf_handler)
        
    def log_trade(self, trade: Dict):
        """Логирование торговой операции"""
        try:
            trade_logger = logging.getLogger('neozork_trades')
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'trade',
                'data': trade
            }
            
            trade_logger.info(json.dumps(log_entry))
            
        except Exception as e:
            self.logger.error(f"Error logging trade: {e}")
    
    def log_performance(self, performance: Dict):
        """Логирование производительности"""
        try:
            perf_logger = logging.getLogger('neozork_performance')
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'performance',
                'data': performance
            }
            
            perf_logger.info(json.dumps(log_entry))
            
        except Exception as e:
            self.logger.error(f"Error logging performance: {e}")
    
    def log_error(self, error: Exception, context: str = ""):
        """Логирование ошибок"""
        try:
            error_logger = logging.getLogger('neozork_100_percent')
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'error',
                'context': context,
                'error': str(error),
                'traceback': str(error.__traceback__)
            }
            
            error_logger.error(json.dumps(log_entry))
            
        except Exception as e:
            self.logger.error(f"Error logging error: {e}")
    
    def log_system_event(self, event: str, data: Dict = None):
        """Логирование системных событий"""
        try:
            system_logger = logging.getLogger('neozork_100_percent')
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'system_event',
                'event': event,
                'data': data or {}
            }
            
            system_logger.info(json.dumps(log_entry))
            
        except Exception as e:
            self.logger.error(f"Error logging system event: {e}")
    
    def get_logs(self, log_type: str = None, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """Получение логов"""
        try:
            logs = []
            
            # Определение файла лога
            if log_type == 'trades':
                log_file = self.log_dir / 'trades.log'
            elif log_type == 'performance':
                log_file = self.log_dir / 'performance.log'
            else:
                log_file = self.log_dir / 'neozork_100_percent.log'
            
            if not log_file.exists():
                return logs
            
            # Чтение логов
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        
                        # Фильтрация по дате
                        if start_date or end_date:
                            log_timestamp = datetime.fromisoformat(log_entry['timestamp'])
                            
                            if start_date and log_timestamp < start_date:
                                continue
                            if end_date and log_timestamp > end_date:
                                continue
                        
                        logs.append(log_entry)
                        
                    except json.JSONDecodeError:
                        continue
            
            return logs
            
        except Exception as e:
            self.logger.error(f"Error getting logs: {e}")
            return []
    
    def export_logs(self, log_type: str = None, start_date: datetime = None, end_date: datetime = None, format: str = 'json') -> str:
        """Экспорт логов"""
        try:
            logs = self.get_logs(log_type, start_date, end_date)
            
            if format == 'json':
                return json.dumps(logs, indent=2)
            elif format == 'csv':
                df = pd.DataFrame(logs)
                return df.to_csv(index=False)
            else:
                return str(logs)
                
        except Exception as e:
            self.logger.error(f"Error exporting logs: {e}")
            return ""
```

Это полная система мониторинга и метрик для достижения 100% прибыли в месяц с детальным отслеживанием всех показателей!
