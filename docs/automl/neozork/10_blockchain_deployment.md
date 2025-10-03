# 10. Деплой на блокчейне - Создание прибыльного DeFi бота

**Цель:** Создать и задеплоить ML-модель на блокчейне для автоматической торговли с доходностью 100%+ в месяц.

## Почему блокчейн-деплой критически важен?

### Преимущества блокчейн-деплоя

1. **Децентрализация** - нет единой точки отказа
2. **Прозрачность** - все транзакции видны
3. **Автоматизация** - смарт-контракты выполняются автоматически
4. **Доступность** - работают 24/7 без перерывов
5. **Интеграция с DeFi** - доступ к множеству протоколов

### Наш подход

**Мы используем:**
- Смарт-контракты для логики
- ML-модели для предсказаний
- DeFi протоколы для торговли
- Автоматическое управление рисками

## Архитектура блокчейн-системы

### 1. Компоненты системы

```python
class BlockchainTradingSystem:
    """Блокчейн торговая система"""
    
    def __init__(self, web3_provider, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = self.web3.eth.account.from_key(private_key)
        self.contracts = {}
        self.models = {}
        self.defi_protocols = {}
        
    def setup_contracts(self, contract_addresses):
        """Настройка контрактов"""
        for name, address in contract_addresses.items():
            abi = self._load_contract_abi(name)
            contract = self.web3.eth.contract(address=address, abi=abi)
            self.contracts[name] = contract
    
    def setup_models(self, model_paths):
        """Настройка ML моделей"""
        for name, path in model_paths.items():
            model = joblib.load(path)
            self.models[name] = model
    
    def setup_defi_protocols(self, protocol_configs):
        """Настройка DeFi протоколов"""
        for name, config in protocol_configs.items():
            protocol = DeFiProtocol(name, config)
            self.defi_protocols[name] = protocol
```

### 2. Смарт-контракт для торговли

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MLTradingBot {
    address public owner;
    address public mlOracle;
    
    struct Trade {
        address token;
        uint256 amount;
        uint256 price;
        uint256 timestamp;
        bool executed;
    }
    
    mapping(uint256 => Trade) public trades;
    uint256 public tradeCounter;
    
    event TradeExecuted(uint256 tradeId, address token, uint256 amount, uint256 price);
    event MLPredictionReceived(uint256 prediction, uint256 confidence);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    modifier onlyMLOracle() {
        require(msg.sender == mlOracle, "Not ML Oracle");
        _;
    }
    
    constructor(address _mlOracle) {
        owner = msg.sender;
        mlOracle = _mlOracle;
    }
    
    function executeTrade(
        address token,
        uint256 amount,
        uint256 price,
        uint256 prediction,
        uint256 confidence
    ) external onlyMLOracle {
        require(confidence > 70, "Confidence too low");
        require(prediction > 0, "Invalid prediction");
        
        // Создание сделки
        uint256 tradeId = tradeCounter++;
        trades[tradeId] = Trade({
            token: token,
            amount: amount,
            price: price,
            timestamp: block.timestamp,
            executed: false
        });
        
        // Выполнение сделки
        _executeTrade(tradeId);
        
        emit TradeExecuted(tradeId, token, amount, price);
        emit MLPredictionReceived(prediction, confidence);
    }
    
    function _executeTrade(uint256 tradeId) internal {
        Trade storage trade = trades[tradeId];
        
        // Логика выполнения сделки
        // Интеграция с DEX (Uniswap, SushiSwap и т.д.)
        
        trade.executed = true;
    }
    
    function updateMLOracle(address _newOracle) external onlyOwner {
        mlOracle = _newOracle;
    }
    
    function emergencyStop() external onlyOwner {
        // Остановка системы в случае экстренной ситуации
        selfdestruct(payable(owner));
    }
}
```

### 3. ML Oracle для предсказаний

```python
class MLOracle:
    """ML Oracle для блокчейна"""
    
    def __init__(self, web3_provider, contract_address, private_key):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.account = self.web3.eth.account.from_key(private_key)
        self.contract = self.web3.eth.contract(
            address=contract_address,
            abi=self._load_contract_abi()
        )
        self.models = {}
        self.data_sources = {}
        
    def setup_models(self, model_configs):
        """Настройка ML моделей"""
        for name, config in model_configs.items():
            model = self._load_model(config['path'])
            self.models[name] = model
    
    def setup_data_sources(self, data_configs):
        """Настройка источников данных"""
        for name, config in data_configs.items():
            source = DataSource(name, config)
            self.data_sources[name] = source
    
    def get_prediction(self, market_data):
        """Получение предсказания"""
        # Сбор данных
        all_data = {}
        for name, source in self.data_sources.items():
            data = source.get_data()
            all_data[name] = data
        
        # Объединение данных
        combined_data = self._combine_data(all_data)
        
        # Предсказания от всех моделей
        predictions = {}
        for name, model in self.models.items():
            pred = model.predict(combined_data)
            predictions[name] = pred
        
        # Ансамблевое предсказание
        ensemble_pred = self._ensemble_predict(predictions)
        
        return ensemble_pred
    
    def submit_prediction(self, prediction, confidence):
        """Отправка предсказания в смарт-контракт"""
        try:
            # Подготовка транзакции
            transaction = self.contract.functions.executeTrade(
                prediction['token'],
                prediction['amount'],
                prediction['price'],
                prediction['direction'],
                confidence
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            # Подписание и отправка
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error submitting prediction: {e}")
            return None
    
    def run_oracle(self):
        """Запуск Oracle"""
        while True:
            try:
                # Получение рыночных данных
                market_data = self._get_market_data()
                
                # Получение предсказания
                prediction = self.get_prediction(market_data)
                
                # Отправка предсказания
                if prediction['confidence'] > 0.7:
                    tx_hash = self.submit_prediction(prediction, prediction['confidence'])
                    if tx_hash:
                        print(f"Prediction submitted: {tx_hash}")
                
                # Пауза между предсказаниями
                time.sleep(60)  # 1 минута
                
            except Exception as e:
                print(f"Error in oracle: {e}")
                time.sleep(60)
```

## DeFi интеграция

### 1. Uniswap V2 интеграция

```python
class UniswapV2Integration:
    """Интеграция с Uniswap V2"""
    
    def __init__(self, web3_provider, router_address, factory_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.router = self.web3.eth.contract(
            address=router_address,
            abi=self._load_uniswap_router_abi()
        )
        self.factory = self.web3.eth.contract(
            address=factory_address,
            abi=self._load_uniswap_factory_abi()
        )
    
    def get_token_price(self, token0, token1):
        """Получение цены токена"""
        try:
            # Получение адреса пула
            pool_address = self.factory.functions.getPair(token0, token1).call()
            
            if pool_address == '0x0000000000000000000000000000000000000000':
                return None
            
            # Получение резервов
            pool_contract = self.web3.eth.contract(
                address=pool_address,
                abi=self._load_uniswap_pair_abi()
            )
            
            reserves = pool_contract.functions.getReserves().call()
            
            # Расчет цены
            if reserves[0] > 0 and reserves[1] > 0:
                price = reserves[1] / reserves[0]
                return price
            
            return None
            
        except Exception as e:
            print(f"Error getting token price: {e}")
            return None
    
    def swap_tokens(self, token_in, token_out, amount_in, min_amount_out, deadline):
        """Обмен токенов"""
        try:
            # Получение пути обмена
            path = [token_in, token_out]
            
            # Параметры транзакции
            transaction = self.router.functions.swapExactTokensForTokens(
                amount_in,
                min_amount_out,
                path,
                self.account.address,
                deadline
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            # Подписание и отправка
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error swapping tokens: {e}")
            return None
    
    def add_liquidity(self, token0, token1, amount0, amount1, min_amount0, min_amount1, deadline):
        """Добавление ликвидности"""
        try:
            transaction = self.router.functions.addLiquidity(
                token0,
                token1,
                amount0,
                amount1,
                min_amount0,
                min_amount1,
                self.account.address,
                deadline
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error adding liquidity: {e}")
            return None
```

### 2. Compound интеграция

```python
class CompoundIntegration:
    """Интеграция с Compound"""
    
    def __init__(self, web3_provider, comptroller_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.comptroller = self.web3.eth.contract(
            address=comptroller_address,
            abi=self._load_compound_comptroller_abi()
        )
        self.c_tokens = {}
    
    def setup_c_tokens(self, c_token_configs):
        """Настройка c-токенов"""
        for name, config in c_token_configs.items():
            c_token = self.web3.eth.contract(
                address=config['address'],
                abi=self._load_compound_c_token_abi()
            )
            self.c_tokens[name] = c_token
    
    def supply_asset(self, c_token_name, amount):
        """Предоставление актива"""
        try:
            c_token = self.c_tokens[c_token_name]
            
            transaction = c_token.functions.mint(amount).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error supplying asset: {e}")
            return None
    
    def borrow_asset(self, c_token_name, amount):
        """Заимствование актива"""
        try:
            c_token = self.c_tokens[c_token_name]
            
            transaction = c_token.functions.borrow(amount).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error borrowing asset: {e}")
            return None
    
    def get_supply_apy(self, c_token_name):
        """Получение APY для предоставления"""
        try:
            c_token = self.c_tokens[c_token_name]
            
            # Получение supply rate
            supply_rate = c_token.functions.supplyRatePerBlock().call()
            
            # Расчет APY
            blocks_per_year = 2102400  # Примерно для Ethereum
            apy = supply_rate * blocks_per_year
            
            return apy
            
        except Exception as e:
            print(f"Error getting supply APY: {e}")
            return None
```

### 3. Aave интеграция

```python
class AaveIntegration:
    """Интеграция с Aave"""
    
    def __init__(self, web3_provider, lending_pool_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.lending_pool = self.web3.eth.contract(
            address=lending_pool_address,
            abi=self._load_aave_lending_pool_abi()
        )
        self.a_tokens = {}
    
    def setup_a_tokens(self, a_token_configs):
        """Настройка a-токенов"""
        for name, config in a_token_configs.items():
            a_token = self.web3.eth.contract(
                address=config['address'],
                abi=self._load_aave_a_token_abi()
            )
            self.a_tokens[name] = a_token
    
    def deposit_asset(self, asset, amount, on_behalf_of=None):
        """Депозит актива"""
        try:
            if on_behalf_of is None:
                on_behalf_of = self.account.address
            
            transaction = self.lending_pool.functions.deposit(
                asset,
                amount,
                on_behalf_of,
                0  # referral code
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error depositing asset: {e}")
            return None
    
    def withdraw_asset(self, asset, amount, to=None):
        """Вывод актива"""
        try:
            if to is None:
                to = self.account.address
            
            transaction = self.lending_pool.functions.withdraw(
                asset,
                amount,
                to
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error withdrawing asset: {e}")
            return None
```

## Автоматическое управление рисками

### 1. Смарт-контракт для риск-менеджмента

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RiskManager {
    address public owner;
    address public tradingBot;
    
    struct RiskLimits {
        uint256 maxPositionSize;
        uint256 maxDailyLoss;
        uint256 maxDrawdown;
        uint256 maxLeverage;
    }
    
    RiskLimits public riskLimits;
    
    mapping(address => uint256) public positionSizes;
    mapping(address => uint256) public dailyLosses;
    uint256 public totalDrawdown;
    
    event RiskLimitExceeded(string limit, uint256 value, uint256 limit);
    event PositionSizeUpdated(address token, uint256 size);
    
    modifier onlyTradingBot() {
        require(msg.sender == tradingBot, "Not trading bot");
        _;
    }
    
    constructor(address _tradingBot) {
        owner = msg.sender;
        tradingBot = _tradingBot;
        
        // Установка лимитов риска
        riskLimits = RiskLimits({
            maxPositionSize: 1000 * 10**18,  // 1000 токенов
            maxDailyLoss: 100 * 10**18,      // 100 токенов
            maxDrawdown: 500 * 10**18,       // 500 токенов
            maxLeverage: 3 * 10**18          // 3x
        });
    }
    
    function checkPositionSize(address token, uint256 amount) external view returns (bool) {
        return amount <= riskLimits.maxPositionSize;
    }
    
    function checkDailyLoss(address token, uint256 loss) external view returns (bool) {
        return dailyLosses[token] + loss <= riskLimits.maxDailyLoss;
    }
    
    function checkDrawdown(uint256 newDrawdown) external view returns (bool) {
        return newDrawdown <= riskLimits.maxDrawdown;
    }
    
    function updatePositionSize(address token, uint256 size) external onlyTradingBot {
        require(size <= riskLimits.maxPositionSize, "Position size exceeds limit");
        
        positionSizes[token] = size;
        emit PositionSizeUpdated(token, size);
    }
    
    function updateDailyLoss(address token, uint256 loss) external onlyTradingBot {
        require(dailyLosses[token] + loss <= riskLimits.maxDailyLoss, "Daily loss exceeds limit");
        
        dailyLosses[token] += loss;
    }
    
    function updateDrawdown(uint256 drawdown) external onlyTradingBot {
        require(drawdown <= riskLimits.maxDrawdown, "Drawdown exceeds limit");
        
        totalDrawdown = drawdown;
    }
    
    function emergencyStop() external onlyTradingBot {
        // Остановка торговли при превышении лимитов
        // Уведомление владельца
    }
}
```

### 2. Python интеграция с риск-менеджментом

```python
class BlockchainRiskManager:
    """Блокчейн риск-менеджер"""
    
    def __init__(self, web3_provider, risk_manager_address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.risk_manager = self.web3.eth.contract(
            address=risk_manager_address,
            abi=self._load_risk_manager_abi()
        )
    
    def check_position_size(self, token, amount):
        """Проверка размера позиции"""
        try:
            result = self.risk_manager.functions.checkPositionSize(token, amount).call()
            return result
        except Exception as e:
            print(f"Error checking position size: {e}")
            return False
    
    def check_daily_loss(self, token, loss):
        """Проверка дневных потерь"""
        try:
            result = self.risk_manager.functions.checkDailyLoss(token, loss).call()
            return result
        except Exception as e:
            print(f"Error checking daily loss: {e}")
            return False
    
    def check_drawdown(self, drawdown):
        """Проверка просадки"""
        try:
            result = self.risk_manager.functions.checkDrawdown(drawdown).call()
            return result
        except Exception as e:
            print(f"Error checking drawdown: {e}")
            return False
    
    def update_position_size(self, token, size):
        """Обновление размера позиции"""
        try:
            transaction = self.risk_manager.functions.updatePositionSize(token, size).build_transaction({
                'from': self.account.address,
                'gas': 100000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error updating position size: {e}")
            return None
```

## Мониторинг и алерты

### 1. Система мониторинга

```python
class BlockchainMonitor:
    """Мониторинг блокчейн системы"""
    
    def __init__(self, web3_provider, contract_addresses):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contracts = {}
        self.monitoring_data = {}
        
        # Настройка контрактов
        for name, address in contract_addresses.items():
            abi = self._load_contract_abi(name)
            contract = self.web3.eth.contract(address=address, abi=abi)
            self.contracts[name] = contract
    
    def monitor_trades(self):
        """Мониторинг сделок"""
        try:
            # Получение событий сделок
            trade_filter = self.contracts['trading_bot'].events.TradeExecuted.createFilter(
                fromBlock='latest'
            )
            
            for event in trade_filter.get_new_entries():
                trade_data = {
                    'trade_id': event.args.tradeId,
                    'token': event.args.token,
                    'amount': event.args.amount,
                    'price': event.args.price,
                    'timestamp': event.args.timestamp
                }
                
                self.monitoring_data['trades'].append(trade_data)
                
                # Проверка алертов
                self._check_trade_alerts(trade_data)
            
        except Exception as e:
            print(f"Error monitoring trades: {e}")
    
    def monitor_ml_predictions(self):
        """Мониторинг ML предсказаний"""
        try:
            # Получение событий предсказаний
            prediction_filter = self.contracts['trading_bot'].events.MLPredictionReceived.createFilter(
                fromBlock='latest'
            )
            
            for event in prediction_filter.get_new_entries():
                prediction_data = {
                    'prediction': event.args.prediction,
                    'confidence': event.args.confidence,
                    'timestamp': event.args.timestamp
                }
                
                self.monitoring_data['predictions'].append(prediction_data)
                
                # Проверка алертов
                self._check_prediction_alerts(prediction_data)
            
        except Exception as e:
            print(f"Error monitoring predictions: {e}")
    
    def _check_trade_alerts(self, trade_data):
        """Проверка алертов по сделкам"""
        # Проверка размера сделки
        if trade_data['amount'] > 1000:  # Большая сделка
            self._send_alert("Large trade detected", trade_data)
        
        # Проверка частоты сделок
        recent_trades = [t for t in self.monitoring_data['trades'] 
                        if t['timestamp'] > time.time() - 3600]  # Последний час
        
        if len(recent_trades) > 10:  # Слишком много сделок
            self._send_alert("High trading frequency", trade_data)
    
    def _check_prediction_alerts(self, prediction_data):
        """Проверка алертов по предсказаниям"""
        # Проверка уверенности
        if prediction_data['confidence'] < 0.5:  # Низкая уверенность
            self._send_alert("Low prediction confidence", prediction_data)
        
        # Проверка аномальных предсказаний
        if prediction_data['prediction'] > 1000:  # Аномальное предсказание
            self._send_alert("Anomalous prediction", prediction_data)
    
    def _send_alert(self, message, data):
        """Отправка алерта"""
        alert = {
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Отправка в Telegram, Discord, email и т.д.
        self._send_telegram_alert(alert)
        self._send_discord_alert(alert)
        self._send_email_alert(alert)
    
    def _send_telegram_alert(self, alert):
        """Отправка алерта в Telegram"""
        try:
            import requests
            
            bot_token = "YOUR_BOT_TOKEN"
            chat_id = "YOUR_CHAT_ID"
            
            message = f"🚨 Alert: {alert['message']}\nData: {alert['data']}"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message
            }
            
            requests.post(url, data=data)
            
        except Exception as e:
            print(f"Error sending Telegram alert: {e}")
    
    def _send_discord_alert(self, alert):
        """Отправка алерта в Discord"""
        try:
            import requests
            
            webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
            
            message = {
                'content': f"🚨 Alert: {alert['message']}",
                'embeds': [{
                    'title': 'Trading Bot Alert',
                    'description': f"Data: {alert['data']}",
                    'color': 16711680  # Red
                }]
            }
            
            requests.post(webhook_url, json=message)
            
        except Exception as e:
            print(f"Error sending Discord alert: {e}")
    
    def _send_email_alert(self, alert):
        """Отправка алерта по email"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            email = "your_email@gmail.com"
            password = "your_password"
            
            msg = MIMEText(f"Alert: {alert['message']}\nData: {alert['data']}")
            msg['Subject'] = "Trading Bot Alert"
            msg['From'] = email
            msg['To'] = email
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            print(f"Error sending email alert: {e}")
```

## Деплой и запуск

### 1. Docker контейнер для блокчейн системы

```dockerfile
# Dockerfile для блокчейн системы
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование кода
COPY src/ ./src/
COPY models/ ./models/
COPY contracts/ ./contracts/
COPY main.py .

# Настройка переменных окружения
ENV WEB3_PROVIDER=""
ENV PRIVATE_KEY=""
ENV CONTRACT_ADDRESSES=""

# Экспорт портов
EXPOSE 8000 8545

# Запуск приложения
CMD ["python", "main.py"]
```

### 2. Docker Compose для полной системы

```yaml
# docker-compose.yml
version: '3.8'

services:
  trading-bot:
    build: .
    environment:
      - WEB3_PROVIDER=${WEB3_PROVIDER}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - CONTRACT_ADDRESSES=${CONTRACT_ADDRESSES}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  ml-oracle:
    build: .
    command: python ml_oracle.py
    environment:
      - WEB3_PROVIDER=${WEB3_PROVIDER}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - CONTRACT_ADDRESSES=${CONTRACT_ADDRESSES}
    volumes:
      - ./models:/app/models
    depends_on:
      - postgres
    restart: unless-stopped

  risk-manager:
    build: .
    command: python risk_manager.py
    environment:
      - WEB3_PROVIDER=${WEB3_PROVIDER}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - CONTRACT_ADDRESSES=${CONTRACT_ADDRESSES}
    depends_on:
      - postgres
    restart: unless-stopped

  monitor:
    build: .
    command: python monitor.py
    environment:
      - WEB3_PROVIDER=${WEB3_PROVIDER}
      - CONTRACT_ADDRESSES=${CONTRACT_ADDRESSES}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=trading_bot
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:6
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 3. Скрипт деплоя

```bash
#!/bin/bash
# deploy.sh

echo "Deploying blockchain trading system..."

# Проверка переменных окружения
if [ -z "$WEB3_PROVIDER" ]; then
    echo "Error: WEB3_PROVIDER not set"
    exit 1
fi

if [ -z "$PRIVATE_KEY" ]; then
    echo "Error: PRIVATE_KEY not set"
    exit 1
fi

# Сборка Docker образов
echo "Building Docker images..."
docker-compose build

# Запуск системы
echo "Starting system..."
docker-compose up -d

# Проверка статуса
echo "Checking system status..."
docker-compose ps

# Проверка логов
echo "Checking logs..."
docker-compose logs trading-bot

echo "Deployment completed!"
```

## Следующие шаги

После изучения блокчейн-деплоя:

1. **Настройте тестовую сеть** для разработки
2. **Протестируйте смарт-контракты** на тестовой сети
3. **Задеплойте на mainnet** после тестирования
4. **Настройте мониторинг** и алерты
5. **Запустите систему** с небольшими суммами

## Ключевые выводы

1. **Смарт-контракты** - основа блокчейн системы
2. **ML Oracle** - мост между ML и блокчейном
3. **DeFi интеграция** - доступ к множеству протоколов
4. **Риск-менеджмент** - защита от потерь
5. **Мониторинг** - контроль системы
6. **Автоматизация** - полная автоматизация процесса

---

**Важно:** Блокчейн-деплой требует глубокого понимания смарт-контрактов и DeFi протоколов. Начните с тестовой сети и постепенно переходите к mainnet.
