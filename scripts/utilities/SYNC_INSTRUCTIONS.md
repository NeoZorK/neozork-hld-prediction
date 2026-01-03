# instructions on синхронизации Git после перевода коммитов

## Проблема
После использования `git filter-branch` for перевода коммитов, GitHub not может обработать такой большой push (153MB, 18714 объектов) за один раз из-за таймаута HTTP 408.

## Текущее состояние
- ✅ Локально переведено: **2271 из 2289 коммитов (99.2%)**
- ✅ Создан скрипт: `scripts/utilities/translate_commits.py`
- ✅ Создан bundle: `/tmp/repo-bundle.bundle` (151MB)
- ❌ Push not проходит из-за ограничений GitHub

## Решения

### Вариант 1: Попробовать позже (рекомендуется)
GitHub может иметь временные ограничения. Попробуйте через несколько часов:

```bash
./scripts/utilities/push_with_retry.sh v0.5.8 origin
```

### Вариант 2: Использовать GitHub CLI for создания нового репозитория
```bash
# Создать новый репозиторий with переведенными коммитами
gh repo create neozork-hld-Prediction-translated --public --source=. --remote=origin-new
git push origin-new v0.5.8
```

### Вариант 3: Использовать git bundle через веб-интерфейс
1. Bundle уже создан: `/tmp/repo-bundle.bundle`
2. Загрузите его через GitHub веб-интерфейс (требует специальных инструментов)

### Вариант 4: Связаться with поддержкой GitHub
Обратитесь in GitHub Support for временного увеличения лимитов for вашего аккаунта.

### Вариант 5: Использовать частичный push (экспериментально)
```bash
./scripts/utilities/smart_sync.sh v0.5.8 origin 200
```

## Альтернативный подход: Создать новую ветку with последними изменениями

Если нужно срочно синхронизировать только последние изменения:

```bash
# Создать ветку только with последними 100 коммитами
git checkout -b v0.5.8-recent-translated
git reset --soft HEAD~100
git commit -m "chore: batch update - translated commit messages (last 100 commits)"
git push origin v0.5.8-recent-translated
```

## check статуса

```bash
# Проверить количество непереведенных коммитов
git log --format="%s" | grep -E "[А-Яа-яЁё]" | wc -l

# Проверить статус синхронизации
git status

# Посмотреть различия
git log --oneline v0.5.8 ^origin/v0.5.8 | wc -l
```

## Рекомендация
**Лучший вариант**: Попробовать позже (через несколько часов) with помощью `push_with_retry.sh`. GitHub может иметь временные ограничения, которые снимаются через некоторое время.

Если это not сработает, используйте **Вариант 2** (create нового репозитория через GitHub CLI) or **Вариант 4** (обращение in поддержку).

