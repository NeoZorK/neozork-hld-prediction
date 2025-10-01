# Продвинутые темы AutoML

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему продвинутые темы критически важны

**Почему 95% ML-инженеров не знают о продвинутых техниках?** Потому что они фокусируются на базовых алгоритмах, не понимая, что современные методы могут дать в 10-100 раз лучшие результаты.

### Проблемы без знания продвинутых тем
- **Устаревшие методы**: Используют техники 5-летней давности
- **Плохие результаты**: Не могут достичь state-of-the-art производительности
- **Потеря конкурентоспособности**: Отстают от команд, использующих современные методы
- **Ограниченные возможности**: Не могут решать сложные задачи

### Преимущества знания продвинутых тем
- **Лучшие результаты**: State-of-the-art производительность
- **Конкурентоспособность**: Используют самые современные методы
- **Решение сложных задач**: Могут работать с мультимодальными данными
- **Инновации**: Могут создавать новые решения

## Введение в продвинутые темы

<img src="images/optimized/advanced_topics_overview.png" alt="Продвинутые темы AutoML" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.1: Обзор продвинутых тем и современных направлений в AutoML - основные категории и методы*

**Почему продвинутые темы - это будущее ML?** Потому что они решают проблемы, которые невозможно решить традиционными методами: автоматический дизайн архитектур, обучение на малых данных, мультимодальное понимание.

**Основные категории продвинутых тем:**
- **Neural Architecture Search (NAS)**: Автоматический поиск оптимальных архитектур нейросетей
- **Meta-Learning**: Обучение тому, как учиться на новых задачах
- **Multi-Modal Learning**: Работа с различными типами данных одновременно
- **Federated Learning**: Распределенное обучение с сохранением приватности
- **Continual Learning**: Непрерывное обучение без забывания предыдущих знаний
- **Quantum Machine Learning**: Использование квантовых вычислений для ML

Этот раздел охватывает передовые темы и современные направления в области автоматизированного машинного обучения, включая нейроархитектурный поиск, мета-обучение, мультимодальное обучение и другие cutting-edge технологии.

## Neural Architecture Search (NAS)

<img src="images/optimized/neural_architecture_search.png" alt="Neural Architecture Search" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.2: Neural Architecture Search - методы автоматического поиска архитектур нейросетей*

**Типы методов NAS:**
- **DARTS (Differentiable)**: Дифференцируемый поиск через градиентный спуск
- **ENAS (Efficient)**: Эффективный поиск через контроллер RNN
- **Random Search**: Случайный поиск в пространстве архитектур
- **Evolutionary Search**: Эволюционный поиск с генетическими алгоритмами
- **Reinforcement Learning**: Поиск через обучение с подкреплением
- **Bayesian Optimization**: Байесовская оптимизация архитектур

### 1. Differentiable Architecture Search (DARTS)

**Почему DARTS - это революция в дизайне нейросетей?** Потому что он позволяет искать архитектуры через градиентный спуск, что в 1000 раз быстрее традиционных методов поиска.

**Преимущества DARTS:**
- **Скорость**: В 1000 раз быстрее случайного поиска
- **Качество**: Находит архитектуры лучше созданных человеком
- **Гибкость**: Может искать любые типы операций
- **Масштабируемость**: Работает с большими датасетами

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DARTS(nn.Module):
    """Differentiable Architecture Search - автоматический дизайн нейросетей"""
    
    def __init__(self, input_channels, output_channels, num_ops=8):
        super(DARTS, self).__init__()
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.num_ops = num_ops
        
        # Операции - кандидаты для архитектуры
        self.ops = nn.ModuleList([
            nn.Conv2d(input_channels, output_channels, 1, bias=False),      # 1x1 conv
            nn.Conv2d(input_channels, output_channels, 3, padding=1, bias=False),  # 3x3 conv
            nn.Conv2d(input_channels, output_channels, 5, padding=2, bias=False),  # 5x5 conv
            nn.MaxPool2d(3, stride=1, padding=1),                          # Max pooling
            nn.AvgPool2d(3, stride=1, padding=1),                          # Average pooling
            nn.Identity() if input_channels == output_channels else None,  # Identity
            nn.Conv2d(input_channels, output_channels, 3, padding=1, dilation=2, bias=False),  # Dilated conv
            nn.Conv2d(input_channels, output_channels, 3, padding=1, dilation=3, bias=False)   # Dilated conv
        ])
        
        # Архитектурные веса - что оптимизируется
        self.alpha = nn.Parameter(torch.randn(num_ops))
        
    def forward(self, x):
        # Softmax для архитектурных весов - нормализация весов
        weights = F.softmax(self.alpha, dim=0)
        
        # Взвешенная сумма операций - комбинация всех операций
        output = sum(w * op(x) for w, op in zip(weights, self.ops) if op is not None)
        
        return output
```

**Детальные описания параметров DARTS:**

- **`input_channels`**: Количество входных каналов
  - `3`: RGB изображения (стандартно)
  - `1`: Grayscale изображения
  - `4`: RGBA изображения
  - `64`: Промежуточные слои
  - `256`: Глубокие слои
  - Применение: определение размерности входных данных

- **`output_channels`**: Количество выходных каналов
  - `64`: Стандартное количество для начальных слоев
  - `128`: Увеличенное количество для средних слоев
  - `256`: Большое количество для глубоких слоев
  - `512`: Очень большое количество для очень глубоких слоев
  - Применение: определение пропускной способности слоя

- **`num_ops=8`**: Количество операций-кандидатов
  - `8`: Стандартное количество (рекомендуется)
  - `4`: Минимальное количество (быстрое обучение)
  - `12`: Большое количество (детальный поиск)
  - `16`: Очень большое количество (очень детальный поиск)
  - Применение: разнообразие архитектурных вариантов

- **`nn.Conv2d(input_channels, output_channels, 1, bias=False)`**: 1x1 свертка
  - `1`: Размер ядра (1x1)
  - `bias=False`: Без смещения (рекомендуется)
  - Применение: точечная свертка для изменения каналов
  - Преимущества: быстрая, эффективная

- **`nn.Conv2d(input_channels, output_channels, 3, padding=1, bias=False)`**: 3x3 свертка
  - `3`: Размер ядра (3x3)
  - `padding=1`: Заполнение для сохранения размера
  - Применение: стандартная свертка для извлечения признаков
  - Преимущества: баланс между качеством и скоростью

- **`nn.Conv2d(input_channels, output_channels, 5, padding=2, bias=False)`**: 5x5 свертка
  - `5`: Размер ядра (5x5)
  - `padding=2`: Заполнение для сохранения размера
  - Применение: большая свертка для глобальных признаков
  - Преимущества: захват больших паттернов

- **`nn.MaxPool2d(3, stride=1, padding=1)`**: Max pooling
  - `3`: Размер окна (3x3)
  - `stride=1`: Шаг 1 для сохранения размера
  - `padding=1`: Заполнение для сохранения размера
  - Применение: извлечение максимальных значений
  - Преимущества: инвариантность к сдвигам

- **`nn.AvgPool2d(3, stride=1, padding=1)`**: Average pooling
  - `3`: Размер окна (3x3)
  - `stride=1`: Шаг 1 для сохранения размера
  - `padding=1`: Заполнение для сохранения размера
  - Применение: извлечение средних значений
  - Преимущества: сглаживание шума

- **`nn.Identity()`**: Тождественная операция
  - Применение: когда input_channels == output_channels
  - Преимущества: пропуск данных без изменений
  - Использование: для skip connections

- **`dilation=2`**: Дилатированная свертка
  - `2`: Коэффициент дилатации
  - Применение: увеличение рецептивного поля
  - Преимущества: захват больших паттернов без увеличения параметров

- **`dilation=3`**: Дилатированная свертка
  - `3`: Коэффициент дилатации
  - Применение: еще большее рецептивное поле
  - Преимущества: очень большие паттерны

- **`self.alpha = nn.Parameter(torch.randn(num_ops))`**: Архитектурные веса
  - `torch.randn(num_ops)`: Случайная инициализация
  - `nn.Parameter`: Обучаемые параметры
  - Применение: оптимизация архитектуры
  - Диапазон: от -∞ до +∞ (нормализуется через softmax)

- **`F.softmax(self.alpha, dim=0)`**: Нормализация весов
  - `dim=0`: Нормализация по операциям
  - Результат: веса от 0 до 1, сумма = 1
  - Применение: вероятностное распределение по операциям
  - Интерпретация: важность каждой операции

# Использование DARTS
def search_architecture(train_loader, val_loader, epochs=50):
    """Поиск архитектуры с помощью DARTS"""
    
    model = DARTS(input_channels=3, output_channels=64)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.025)
    
    for epoch in range(epochs):
        # Обновление архитектурных весов
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = F.cross_entropy(output, target)
            loss.backward()
            optimizer.step()
        
        # Валидация
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for data, target in val_loader:
                output = model(data)
                val_loss += F.cross_entropy(output, target).item()
        
        print(f'Epoch {epoch}, Validation Loss: {val_loss:.4f}')
    
    return model
```

**Детальные описания параметров поиска архитектуры:**

- **`train_loader`**: Загрузчик обучающих данных
  - Тип: DataLoader
  - Содержит: батчи (data, target)
  - Применение: обучение архитектурных весов
  - Рекомендация: сбалансированные батчи

- **`val_loader`**: Загрузчик валидационных данных
  - Тип: DataLoader
  - Содержит: батчи (data, target)
  - Применение: оценка качества архитектуры
  - Рекомендация: независимый от train_loader

- **`epochs=50`**: Количество эпох обучения
  - `50`: Стандартное количество (рекомендуется)
  - `25`: Быстрое обучение (менее точно)
  - `100`: Длительное обучение (более точно)
  - `200`: Очень длительное обучение (очень точно)
  - Применение: контроль времени обучения

- **`input_channels=3`**: Количество входных каналов
  - `3`: RGB изображения (стандартно)
  - `1`: Grayscale изображения
  - `4`: RGBA изображения
  - Применение: соответствие входным данным

- **`output_channels=64`**: Количество выходных каналов
  - `64`: Стандартное количество для начальных слоев
  - `32`: Меньше каналов (быстрее)
  - `128`: Больше каналов (качественнее)
  - `256`: Очень много каналов (очень качественно)
  - Применение: баланс между скоростью и качеством

- **`torch.optim.Adam(model.parameters(), lr=0.025)`**: Оптимизатор Adam
  - `model.parameters()`: Все параметры модели
  - `lr=0.025`: Learning rate (рекомендуется для DARTS)
  - `0.01`: Меньший learning rate (стабильнее)
  - `0.05`: Больший learning rate (быстрее)
  - `0.1`: Очень большой learning rate (может быть нестабильным)

- **`model.train()`**: Режим обучения
  - Включает: dropout, batch normalization в режиме обучения
  - Отключает: детерминированное поведение
  - Применение: активация обучающих компонентов

- **`optimizer.zero_grad()`**: Обнуление градиентов
  - Обнуляет: накопленные градиенты
  - Применение: предотвращение накопления градиентов
  - Обязательно: перед каждым backward pass

- **`F.cross_entropy(output, target)`**: Функция потерь
  - `output`: Предсказания модели
  - `target`: Истинные метки
  - Применение: классификация
  - Альтернативы: F.mse_loss для регрессии

- **`loss.backward()`**: Обратное распространение
  - Вычисляет: градиенты по всем параметрам
  - Применение: подготовка к обновлению весов
  - Обязательно: перед optimizer.step()

- **`optimizer.step()`**: Обновление параметров
  - Обновляет: все параметры модели
  - Применение: оптимизация архитектурных весов
  - Результат: улучшение архитектуры

- **`model.eval()`**: Режим оценки
  - Включает: детерминированное поведение
  - Отключает: dropout, batch normalization в режиме обучения
  - Применение: стабильная оценка на валидации

- **`torch.no_grad()`**: Отключение градиентов
  - Отключает: вычисление градиентов
  - Применение: ускорение валидации
  - Экономия: памяти и вычислений

- **`val_loss += F.cross_entropy(output, target).item()`**: Накопление потерь
  - `.item()`: Преобразование в Python float
  - Применение: избежание накопления градиентов
  - Результат: скалярное значение потерь
```

### 2. Efficient Neural Architecture Search (ENAS)

```python
class ENAS(nn.Module):
    """Efficient Neural Architecture Search"""
    
    def __init__(self, num_nodes=5, num_ops=8):
        super(ENAS, self).__init__()
        self.num_nodes = num_nodes
        self.num_ops = num_ops
        
        # Контроллер (RNN)
        self.controller = nn.LSTM(32, 32, num_layers=2, batch_first=True)
        self.controller_output = nn.Linear(32, num_nodes * num_ops)
        
        # Операции
        self.ops = nn.ModuleList([
            nn.Conv2d(3, 64, 3, padding=1),
            nn.Conv2d(3, 64, 5, padding=2),
            nn.MaxPool2d(3, stride=1, padding=1),
            nn.AvgPool2d(3, stride=1, padding=1),
            nn.Conv2d(3, 64, 1),
            nn.Conv2d(3, 64, 3, padding=1, dilation=2),
            nn.Conv2d(3, 64, 3, padding=1, dilation=3),
            nn.Identity()
        ])
        
    def sample_architecture(self):
        """Сэмплирование архитектуры"""
        # Генерация архитектуры через контроллер
        hidden = torch.zeros(2, 1, 32)  # LSTM hidden state
        outputs = []
        
        for i in range(self.num_nodes):
            output, hidden = self.controller(torch.randn(1, 1, 32), hidden)
            logits = self.controller_output(output)
            logits = logits.view(self.num_nodes, self.num_ops)
            probs = F.softmax(logits[i], dim=0)
            action = torch.multinomial(probs, 1)
            outputs.append(action.item())
        
        return outputs
    
    def forward(self, x, architecture=None):
        if architecture is None:
            architecture = self.sample_architecture()
        
        # Применение архитектуры
        for i, op_idx in enumerate(architecture):
            x = self.ops[op_idx](x)
        
        return x
```

**Детальные описания параметров ENAS:**

- **`num_nodes=5`**: Количество узлов в архитектуре
  - `5`: Стандартное количество (рекомендуется)
  - `3`: Простая архитектура (быстрее)
  - `8`: Сложная архитектура (качественнее)
  - `10`: Очень сложная архитектура (очень качественно)
  - Применение: контроль сложности архитектуры

- **`num_ops=8`**: Количество операций-кандидатов
  - `8`: Стандартное количество (рекомендуется)
  - `4`: Минимальное количество (быстрое обучение)
  - `12`: Большое количество (детальный поиск)
  - `16`: Очень большое количество (очень детальный поиск)
  - Применение: разнообразие архитектурных вариантов

- **`nn.LSTM(32, 32, num_layers=2, batch_first=True)`**: LSTM контроллер
  - `32`: Размер входа и скрытого состояния
  - `num_layers=2`: Количество слоев LSTM
  - `batch_first=True`: Первая размерность - batch
  - Применение: генерация архитектурных решений
  - Преимущества: учет последовательности решений

- **`nn.Linear(32, num_nodes * num_ops)`**: Выходной слой контроллера
  - `32`: Размер входа (размер скрытого состояния LSTM)
  - `num_nodes * num_ops`: Размер выхода (все возможные решения)
  - Применение: преобразование скрытого состояния в логиты
  - Результат: вероятности для каждой операции в каждом узле

- **`torch.zeros(2, 1, 32)`**: Инициализация скрытого состояния LSTM
  - `2`: Количество слоев LSTM
  - `1`: Batch size (один образец)
  - `32`: Размер скрытого состояния
  - Применение: начальное состояние для генерации
  - Результат: детерминированная инициализация

- **`torch.randn(1, 1, 32)`**: Входной тензор для LSTM
  - `1`: Batch size
  - `1`: Sequence length
  - `32`: Feature dimension
  - Применение: входные данные для контроллера
  - Альтернативы: можно использовать learnable embeddings

- **`logits.view(self.num_nodes, self.num_ops)`**: Изменение формы логитов
  - `num_nodes`: Количество узлов
  - `num_ops`: Количество операций
  - Применение: группировка логитов по узлам
  - Результат: матрица (num_nodes, num_ops)

- **`F.softmax(logits[i], dim=0)`**: Нормализация вероятностей
  - `logits[i]`: Логиты для i-го узла
  - `dim=0`: Нормализация по операциям
  - Результат: вероятности от 0 до 1, сумма = 1
  - Применение: вероятностное распределение по операциям

- **`torch.multinomial(probs, 1)`**: Сэмплирование операции
  - `probs`: Вероятности операций
  - `1`: Количество образцов
  - Результат: индекс выбранной операции
  - Применение: стохастический выбор операции

- **`action.item()`**: Преобразование в Python int
  - Преобразует: tensor в Python int
  - Применение: использование в качестве индекса
  - Результат: целое число от 0 до num_ops-1

- **`self.ops[op_idx](x)`**: Применение выбранной операции
  - `op_idx`: Индекс выбранной операции
  - `x`: Входные данные
  - Применение: выполнение операции на данных
  - Результат: преобразованные данные

**Операции ENAS:**

- **`nn.Conv2d(3, 64, 3, padding=1)`**: 3x3 свертка
  - `3`: Входные каналы
  - `64`: Выходные каналы
  - `3`: Размер ядра
  - `padding=1`: Заполнение для сохранения размера

- **`nn.Conv2d(3, 64, 5, padding=2)`**: 5x5 свертка
  - `5`: Размер ядра (больше рецептивное поле)
  - `padding=2`: Заполнение для сохранения размера

- **`nn.MaxPool2d(3, stride=1, padding=1)`**: Max pooling
  - `3`: Размер окна
  - `stride=1`: Шаг 1 для сохранения размера
  - `padding=1`: Заполнение для сохранения размера

- **`nn.AvgPool2d(3, stride=1, padding=1)`**: Average pooling
  - `3`: Размер окна
  - `stride=1`: Шаг 1 для сохранения размера
  - `padding=1`: Заполнение для сохранения размера

- **`nn.Conv2d(3, 64, 1)`**: 1x1 свертка
  - `1`: Размер ядра (точечная свертка)
  - Применение: изменение каналов без изменения размера

- **`dilation=2`**: Дилатированная свертка
  - `2`: Коэффициент дилатации
  - Применение: увеличение рецептивного поля

- **`dilation=3`**: Дилатированная свертка
  - `3`: Коэффициент дилатации
  - Применение: еще большее рецептивное поле

- **`nn.Identity()`**: Тождественная операция
  - Применение: пропуск данных без изменений
  - Использование: для skip connections
```

## Meta-Learning

<img src="images/optimized/meta_learning.png" alt="Meta-Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.3: Meta-Learning (Learning to Learn) - методы обучения тому, как учиться*

**Типы методов мета-обучения:**
- **MAML (Model-Agnostic)**: Универсальный мета-обучение для любых моделей
- **Prototypical Networks**: Обучение через прототипы классов
- **Matching Networks**: Сопоставление примеров для классификации
- **Reptile**: Простой и эффективный мета-обучение
- **Meta-SGD**: Мета-обучение с адаптивными шагами обучения
- **Gradient Meta-Learning**: Мета-обучение через градиенты

### 1. Model-Agnostic Meta-Learning (MAML)

```python
class MAML(nn.Module):
    """Model-Agnostic Meta-Learning"""
    
    def __init__(self, model, lr=0.01):
        super(MAML, self).__init__()
        self.model = model
        self.lr = lr
        
    def forward(self, x):
        return self.model(x)
    
    def meta_update(self, support_set, query_set, num_inner_steps=5):
        """Мета-обновление модели"""
        
        # Копирование параметров
        fast_weights = {name: param.clone() for name, param in self.model.named_parameters()}
        
        # Внутренние обновления
        for step in range(num_inner_steps):
            # Forward pass на support set
            support_pred = self.forward_with_weights(support_set[0], fast_weights)
            support_loss = F.cross_entropy(support_pred, support_set[1])
            
            # Градиенты
            grads = torch.autograd.grad(support_loss, fast_weights.values(), create_graph=True)
            
            # Обновление весов
            fast_weights = {name: weight - self.lr * grad 
                          for (name, weight), grad in zip(fast_weights.items(), grads)}
        
        # Оценка на query set
        query_pred = self.forward_with_weights(query_set[0], fast_weights)
        query_loss = F.cross_entropy(query_pred, query_set[1])
        
        return query_loss
    
    def forward_with_weights(self, x, weights):
        """Forward pass с заданными весами"""
        # Реализация forward pass с custom весами
        pass
```

**Детальные описания параметров MAML:**

- **`model`**: Базовая модель для мета-обучения
  - Тип: nn.Module
  - Требования: должна поддерживать named_parameters()
  - Применение: любая модель (CNN, RNN, Transformer)
  - Примеры: ResNet, LSTM, BERT

- **`lr=0.01`**: Learning rate для внутренних обновлений
  - `0.01`: Стандартное значение (рекомендуется)
  - `0.001`: Меньший learning rate (стабильнее)
  - `0.1`: Больший learning rate (быстрее)
  - `0.5`: Очень большой learning rate (может быть нестабильным)
  - Применение: скорость адаптации к новым задачам

- **`support_set`**: Поддерживающий набор данных
  - Формат: (data, labels) tuple
  - Размер: обычно 5-20 образцов (few-shot learning)
  - Применение: быстрая адаптация к новой задаче
  - Рекомендация: сбалансированные классы

- **`query_set`**: Запросный набор данных
  - Формат: (data, labels) tuple
  - Размер: обычно 15-100 образцов
  - Применение: оценка качества адаптации
  - Рекомендация: независимый от support_set

- **`num_inner_steps=5`**: Количество внутренних шагов
  - `5`: Стандартное количество (рекомендуется)
  - `1`: Быстрая адаптация (менее точно)
  - `10`: Медленная адаптация (более точно)
  - `20`: Очень медленная адаптация (очень точно)
  - Применение: контроль скорости адаптации

- **`fast_weights`**: Быстрые веса для адаптации
  - Тип: dict с параметрами модели
  - Инициализация: копия исходных весов
  - Применение: временные веса для новой задачи
  - Обновление: через градиентный спуск

- **`support_pred = self.forward_with_weights(support_set[0], fast_weights)`**: Предсказание на support set
  - `support_set[0]`: Данные support set
  - `fast_weights`: Текущие быстрые веса
  - Результат: предсказания модели
  - Применение: вычисление потерь для адаптации

- **`F.cross_entropy(support_pred, support_set[1])`**: Функция потерь
  - `support_pred`: Предсказания модели
  - `support_set[1]`: Истинные метки
  - Применение: классификация
  - Альтернативы: F.mse_loss для регрессии

- **`torch.autograd.grad(support_loss, fast_weights.values(), create_graph=True)`**: Вычисление градиентов
  - `support_loss`: Потери на support set
  - `fast_weights.values()`: Параметры для дифференцирования
  - `create_graph=True`: Сохранение графа для второго порядка
  - Результат: градиенты по параметрам
  - Применение: обновление быстрых весов

- **`weight - self.lr * grad`**: Обновление весов
  - `weight`: Текущий вес
  - `self.lr`: Learning rate
  - `grad`: Градиент веса
  - Результат: новый вес
  - Применение: градиентный спуск

- **`query_pred = self.forward_with_weights(query_set[0], fast_weights)`**: Предсказание на query set
  - `query_set[0]`: Данные query set
  - `fast_weights`: Адаптированные веса
  - Результат: предсказания на query set
  - Применение: оценка качества адаптации

- **`query_loss = F.cross_entropy(query_pred, query_set[1])`**: Потери на query set
  - `query_pred`: Предсказания на query set
  - `query_set[1]`: Истинные метки query set
  - Результат: финальные потери
  - Применение: мета-обучение

**Ключевые особенности MAML:**

- **Model-Agnostic**: Работает с любыми моделями
- **Few-Shot Learning**: Быстрая адаптация к новым задачам
- **Meta-Learning**: Обучение тому, как учиться
- **Gradient-Based**: Использует градиенты для адаптации
- **Second-Order**: Учитывает градиенты второго порядка

**Применение MAML:**

- **Few-Shot Classification**: Классификация с малым количеством примеров
- **Few-Shot Regression**: Регрессия с малым количеством примеров
- **Domain Adaptation**: Адаптация к новым доменам
- **Task Adaptation**: Адаптация к новым задачам
- **Continual Learning**: Непрерывное обучение
```

### 2. Prototypical Networks

```python
class PrototypicalNetworks(nn.Module):
    """Prototypical Networks для few-shot learning"""
    
    def __init__(self, input_dim, hidden_dim=64):
        super(PrototypicalNetworks, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
    
    def forward(self, support_set, query_set, num_classes):
        """Forward pass для few-shot learning"""
        
        # Кодирование support set
        support_embeddings = self.encoder(support_set)
        
        # Вычисление прототипов классов
        prototypes = []
        for i in range(num_classes):
            class_mask = (support_set[:, -1] == i)  # Предполагаем, что последний столбец - это класс
            class_embeddings = support_embeddings[class_mask]
            prototype = class_embeddings.mean(dim=0)
            prototypes.append(prototype)
        
        prototypes = torch.stack(prototypes)
        
        # Кодирование query set
        query_embeddings = self.encoder(query_set)
        
        # Вычисление расстояний до прототипов
        distances = torch.cdist(query_embeddings, prototypes)
        
        # Предсказания (ближайший прототип)
        predictions = torch.argmin(distances, dim=1)
        
        return predictions, distances
```

## Multi-Modal Learning

<img src="images/optimized/multimodal_learning.png" alt="Multi-Modal Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.4: Multi-Modal Learning - работа с различными типами данных одновременно*

**Типы модальностей:**
- **Vision (Images)**: Обработка изображений и визуальных данных
- **Language (Text)**: Обработка текста и естественного языка
- **Audio (Sound)**: Обработка звуковых и аудио данных
- **Video (Motion)**: Обработка видео и временных последовательностей
- **Sensor Data**: Обработка данных с датчиков
- **Structured Data**: Обработка структурированных данных

**Методы фьюжна:**
- **Early Fusion**: Раннее объединение модальностей
- **Late Fusion**: Позднее объединение модальностей
- **Cross-Modal Attention**: Взаимное внимание между модальностями

### 1. Vision-Language Models

```python
class VisionLanguageModel(nn.Module):
    """Мультимодальная модель для изображений и текста"""
    
    def __init__(self, image_dim=2048, text_dim=768, hidden_dim=512):
        super(VisionLanguageModel, self).__init__()
        
        # Визуальный энкодер
        self.vision_encoder = nn.Sequential(
            nn.Linear(image_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Текстовый энкодер
        self.text_encoder = nn.Sequential(
            nn.Linear(text_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Фьюжн модуль
        self.fusion = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, images, texts):
        # Кодирование изображений
        image_features = self.vision_encoder(images)
        
        # Кодирование текста
        text_features = self.text_encoder(texts)
        
        # Объединение признаков
        combined = torch.cat([image_features, text_features], dim=1)
        
        # Предсказание
        output = self.fusion(combined)
        
        return output
```

### 2. Cross-Modal Attention

```python
class CrossModalAttention(nn.Module):
    """Cross-modal attention для мультимодального обучения"""
    
    def __init__(self, dim):
        super(CrossModalAttention, self).__init__()
        self.dim = dim
        
        # Attention механизмы
        self.attention = nn.MultiheadAttention(dim, num_heads=8)
        
        # Нормализация
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        
        # Feed-forward
        self.ff = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.ReLU(),
            nn.Linear(dim * 4, dim)
        )
    
    def forward(self, modality1, modality2):
        # Cross-attention между модальностями
        attended1, _ = self.attention(modality1, modality2, modality2)
        attended1 = self.norm1(attended1 + modality1)
        
        attended2, _ = self.attention(modality2, modality1, modality1)
        attended2 = self.norm1(attended2 + modality2)
        
        # Feed-forward
        output1 = self.norm2(attended1 + self.ff(attended1))
        output2 = self.norm2(attended2 + self.ff(attended2))
        
        return output1, output2
```

## Federated Learning

<img src="images/optimized/federated_learning.png" alt="Federated Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.5: Federated Learning Architecture - распределенное обучение с сохранением приватности*

**Архитектура федеративного обучения:**
- **Global Server**: Центральный сервер для агрегации моделей
- **Clients**: Распределенные клиенты с локальными данными
- **Local Training**: Локальное обучение на каждом клиенте
- **Model Aggregation**: Агрегация обновлений модели
- **Privacy Preservation**: Сохранение приватности данных

**Преимущества федеративного обучения:**
- **Сохранение приватности**: Данные не покидают клиентов
- **Распределенные данные**: Обучение на распределенных данных
- **Масштабируемость**: Масштабирование на множество клиентов
- **Снижение коммуникации**: Минимизация передачи данных
- **Локальная обработка**: Обработка данных на устройстве

### 1. Federated Averaging (FedAvg)

```python
class FederatedAveraging:
    """Federated Averaging для распределенного обучения"""
    
    def __init__(self, global_model, clients):
        self.global_model = global_model
        self.clients = clients
    
    def federated_round(self, num_epochs=5):
        """Один раунд федеративного обучения"""
        
        # Обучение на клиентах
        client_models = []
        client_weights = []
        
        for client in self.clients:
            # Локальное обучение
            local_model = self.train_client(client, num_epochs)
            client_models.append(local_model)
            client_weights.append(len(client.data))  # Вес пропорционален размеру данных
        
        # Агрегация моделей
        self.aggregate_models(client_models, client_weights)
    
    def train_client(self, client, num_epochs):
        """Обучение модели на клиенте"""
        
        # Копирование глобальной модели
        local_model = copy.deepcopy(self.global_model)
        
        # Локальное обучение
        optimizer = torch.optim.SGD(local_model.parameters(), lr=0.01)
        
        for epoch in range(num_epochs):
            for batch in client.data_loader:
                optimizer.zero_grad()
                output = local_model(batch[0])
                loss = F.cross_entropy(output, batch[1])
                loss.backward()
                optimizer.step()
        
        return local_model
    
    def aggregate_models(self, client_models, weights):
        """Агрегация моделей с учетом весов"""
        
        total_weight = sum(weights)
        
        # Инициализация глобальной модели
        for param in self.global_model.parameters():
            param.data.zero_()
        
        # Взвешенное усреднение
        for model, weight in zip(client_models, weights):
            for global_param, local_param in zip(self.global_model.parameters(), model.parameters()):
                global_param.data += local_param.data * (weight / total_weight)
```

**Детальные описания параметров Federated Learning:**

- **`global_model`**: Глобальная модель на сервере
  - Тип: nn.Module
  - Применение: центральная модель для агрегации
  - Инициализация: случайные веса или предобученная модель
  - Обновление: через агрегацию локальных моделей

- **`clients`**: Список клиентов
  - Тип: List[Client]
  - Содержит: локальные данные и модели
  - Применение: распределенное обучение
  - Рекомендация: 10-1000 клиентов

- **`num_epochs=5`**: Количество эпох локального обучения
  - `5`: Стандартное количество (рекомендуется)
  - `1`: Быстрое обучение (менее точно)
  - `10`: Медленное обучение (более точно)
  - `20`: Очень медленное обучение (очень точно)
  - Применение: контроль локального обучения

- **`client.data`**: Локальные данные клиента
  - Тип: Dataset
  - Содержит: приватные данные клиента
  - Применение: локальное обучение
  - Приватность: данные не покидают клиента

- **`len(client.data)`**: Размер данных клиента
  - Применение: вес для агрегации
  - Логика: больше данных = больше вес
  - Результат: пропорциональное влияние на глобальную модель

- **`copy.deepcopy(self.global_model)`**: Копирование глобальной модели
  - Применение: инициализация локальной модели
  - Результат: независимая копия модели
  - Преимущества: изоляция обучения

- **`torch.optim.SGD(local_model.parameters(), lr=0.01)`**: SGD оптимизатор
  - `local_model.parameters()`: Параметры локальной модели
  - `lr=0.01`: Learning rate (рекомендуется для FedAvg)
  - `0.001`: Меньший learning rate (стабильнее)
  - `0.1`: Больший learning rate (быстрее)
  - Применение: локальная оптимизация

- **`client.data_loader`**: Загрузчик данных клиента
  - Тип: DataLoader
  - Содержит: батчи локальных данных
  - Применение: итерация по данным
  - Рекомендация: сбалансированные батчи

- **`total_weight = sum(weights)`**: Общий вес всех клиентов
  - Вычисление: сумма весов всех клиентов
  - Применение: нормализация весов
  - Результат: сумма всех весов

- **`param.data.zero_()`**: Обнуление параметров глобальной модели
  - Применение: подготовка к агрегации
  - Результат: нулевые параметры
  - Необходимо: перед взвешенным усреднением

- **`global_param.data += local_param.data * (weight / total_weight)`**: Взвешенное усреднение
  - `global_param`: Параметр глобальной модели
  - `local_param`: Параметр локальной модели
  - `weight / total_weight`: Нормализованный вес
  - Результат: взвешенная сумма параметров

**Ключевые особенности Federated Learning:**

- **Privacy-Preserving**: Сохранение приватности данных
- **Distributed Training**: Распределенное обучение
- **Communication Efficient**: Эффективная коммуникация
- **Fault Tolerant**: Устойчивость к сбоям
- **Scalable**: Масштабируемость

**Преимущества Federated Learning:**

- **Data Privacy**: Данные не покидают клиентов
- **Reduced Communication**: Минимизация передачи данных
- **Local Processing**: Обработка на устройстве
- **Federated Aggregation**: Агрегация обновлений
- **Global Model**: Единая глобальная модель

**Применение Federated Learning:**

- **Mobile Devices**: Обучение на мобильных устройствах
- **IoT Sensors**: Обучение на датчиках
- **Healthcare**: Медицинские данные
- **Finance**: Финансовые данные
- **Edge Computing**: Обучение на границе сети
```

### 2. Differential Privacy

```python
class DifferentialPrivacy:
    """Differential Privacy для защиты приватности"""
    
    def __init__(self, epsilon=1.0, delta=1e-5):
        self.epsilon = epsilon
        self.delta = delta
    
    def add_noise(self, gradients, sensitivity=1.0):
        """Добавление шума для обеспечения дифференциальной приватности"""
        
        # Вычисление стандартного отклонения шума
        sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * sensitivity / self.epsilon
        
        # Добавление гауссовского шума
        noise = torch.normal(0, sigma, size=gradients.shape)
        noisy_gradients = gradients + noise
        
        return noisy_gradients
    
    def clip_gradients(self, gradients, max_norm=1.0):
        """Обрезка градиентов для ограничения чувствительности"""
        
        # L2 нормализация
        grad_norm = torch.norm(gradients)
        if grad_norm > max_norm:
            gradients = gradients * (max_norm / grad_norm)
        
        return gradients
```

## Continual Learning

<img src="images/optimized/continual_learning.png" alt="Continual Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.6: Continual Learning (Lifelong Learning) - непрерывное обучение без забывания*

**Типы методов непрерывного обучения:**
- **EWC (Elastic Weight)**: Эластичное закрепление весов для сохранения знаний
- **Progressive Networks**: Прогрессивные сети с боковыми соединениями
- **Memory Replay**: Воспроизведение предыдущих примеров
- **Regularization Methods**: Регуляризация для предотвращения забывания
- **Architectural Methods**: Архитектурные изменения для новых задач
- **Meta-Learning Approaches**: Мета-обучение для непрерывной адаптации

**Проблема катастрофического забывания:**
- **Забывание предыдущих задач**: Потеря знаний о старых задачах
- **Интерференция между задачами**: Конфликт между новыми и старыми знаниями
- **Необходимость сохранения знаний**: Важность сохранения предыдущего опыта
- **Баланс между старым и новым**: Равновесие между старыми и новыми знаниями

### 1. Elastic Weight Consolidation (EWC)

```python
class ElasticWeightConsolidation:
    """Elastic Weight Consolidation для непрерывного обучения"""
    
    def __init__(self, model, lambda_ewc=1000):
        self.model = model
        self.lambda_ewc = lambda_ewc
        self.fisher_information = {}
        self.optimal_params = {}
    
    def compute_fisher_information(self, dataloader):
        """Вычисление информации Фишера"""
        
        self.model.eval()
        fisher_info = {}
        
        for name, param in self.model.named_parameters():
            fisher_info[name] = torch.zeros_like(param)
        
        for batch in dataloader:
            self.model.zero_grad()
            output = self.model(batch[0])
            loss = F.cross_entropy(output, batch[1])
            loss.backward()
            
            for name, param in self.model.named_parameters():
                if param.grad is not None:
                    fisher_info[name] += param.grad ** 2
        
        # Нормализация
        for name in fisher_info:
            fisher_info[name] /= len(dataloader)
        
        self.fisher_information = fisher_info
    
    def ewc_loss(self, current_loss):
        """Добавление EWC регуляризации к loss"""
        
        ewc_loss = current_loss
        
        for name, param in self.model.named_parameters():
            if name in self.fisher_information:
                ewc_loss += (self.lambda_ewc / 2) * torch.sum(
                    self.fisher_information[name] * (param - self.optimal_params[name]) ** 2
                )
        
        return ewc_loss
```

### 2. Progressive Neural Networks

```python
class ProgressiveNeuralNetwork(nn.Module):
    """Progressive Neural Networks для непрерывного обучения"""
    
    def __init__(self, input_dim, hidden_dim=64):
        super(ProgressiveNeuralNetwork, self).__init__()
        self.columns = nn.ModuleList()
        self.lateral_connections = nn.ModuleList()
        
        # Первая колонка
        first_column = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        self.columns.append(first_column)
    
    def add_column(self, input_dim, hidden_dim=64):
        """Добавление новой колонки для новой задачи"""
        
        # Новая колонка
        new_column = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        self.columns.append(new_column)
        
        # Боковые соединения с предыдущими колонками
        lateral_conn = nn.ModuleList()
        for i in range(len(self.columns) - 1):
            lateral_conn.append(nn.Linear(hidden_dim, hidden_dim))
        self.lateral_connections.append(lateral_conn)
    
    def forward(self, x, column_idx):
        """Forward pass для конкретной колонки"""
        
        # Основной путь через текущую колонку
        output = self.columns[column_idx](x)
        
        # Боковые соединения с предыдущими колонками
        for i in range(column_idx):
            lateral_output = self.lateral_connections[column_idx][i](
                self.columns[i](x)
            )
            output = output + lateral_output
        
        return output
```

## Quantum Machine Learning

<img src="images/optimized/quantum_ml.png" alt="Quantum Machine Learning" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.7: Quantum Machine Learning - использование квантовых вычислений для ML*

**Компоненты квантового ML:**
- **Quantum Neural Networks**: Квантовые нейронные сети
- **Quantum Circuits**: Квантовые схемы и алгоритмы
- **Quantum Algorithms**: Квантовые алгоритмы для ML
- **Quantum Gates**: Квантовые вентили для вычислений
- **Quantum Entanglement**: Квантовая запутанность для параллелизма
- **Quantum Superposition**: Квантовая суперпозиция для экспоненциального ускорения

**Квантовые преимущества:**
- **Экспоненциальное ускорение**: Экспоненциальное ускорение вычислений
- **Параллельные вычисления**: Параллельная обработка информации
- **Квантовая суперпозиция**: Одновременное нахождение в нескольких состояниях
- **Квантовая запутанность**: Коррелированные состояния для вычислений
- **Квантовые интерференции**: Интерференция для оптимизации

### 1. Quantum Neural Networks

```python
# Пример с использованием PennyLane
import pennylane as qml
import numpy as np

def quantum_neural_network(params, x):
    """Квантовая нейронная сеть"""
    
    # Кодирование данных
    for i in range(len(x)):
        qml.RY(x[i], wires=i)
    
    # Параметризованные слои
    for layer in range(len(params)):
        for i in range(len(x)):
            qml.RY(params[layer][i], wires=i)
        
        # Энтangling gates
        for i in range(len(x) - 1):
            qml.CNOT(wires=[i, i+1])
    
    # Измерение
    return [qml.expval(qml.PauliZ(i)) for i in range(len(x))]

# Создание квантового устройства
dev = qml.device('default.qubit', wires=4)

# Создание QNode
qnode = qml.QNode(quantum_neural_network, dev)

# Обучение квантовой модели
def train_quantum_model(X, y, num_layers=3):
    """Обучение квантовой нейронной сети"""
    
    # Инициализация параметров
    params = np.random.uniform(0, 2*np.pi, (num_layers, len(X[0])))
    
    # Оптимизатор
    opt = qml.GradientDescentOptimizer(stepsize=0.1)
    
    for iteration in range(100):
        # Вычисление градиентов
        grads = qml.grad(qnode)(params, X[0])
        
        # Обновление параметров
        params = opt.step(qnode, params, X[0])
        
        if iteration % 10 == 0:
            print(f"Iteration {iteration}, Cost: {qnode(params, X[0])}")
    
    return params
```

## Заключение

<img src="images/optimized/advanced_methods_comparison.png" alt="Сравнение продвинутых методов" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 18.8: Сравнение продвинутых методов AutoML - производительность, сложность, время обучения, требования к данным*

**Сравнение продвинутых методов:**
- **Performance vs Complexity**: Баланс между производительностью и сложностью
- **Training Time**: Время обучения различных методов
- **Data Requirements**: Требования к объему данных
- **Real-world Applicability**: Применимость в реальных задачах

Продвинутые темы AutoML представляют собой быстро развивающуюся область, включающую:

1. **Neural Architecture Search** - автоматический поиск оптимальных архитектур
2. **Meta-Learning** - обучение тому, как учиться
3. **Multi-Modal Learning** - работа с различными типами данных
4. **Federated Learning** - распределенное обучение с сохранением приватности
5. **Continual Learning** - непрерывное обучение без забывания
6. **Quantum Machine Learning** - использование квантовых вычислений

Эти технологии открывают новые возможности для создания более эффективных, адаптивных и мощных ML-систем, но требуют глубокого понимания как теоретических основ, так и практических аспектов их применения.
