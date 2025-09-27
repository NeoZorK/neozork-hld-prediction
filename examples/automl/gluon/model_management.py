#!/usr/bin/env python3
"""
AutoGluon Model Management Script
Управление моделями AutoGluon
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoGluonModelManager:
    """Менеджер для управления моделями AutoGluon"""
    
    def __init__(self, models_dir="models/autogluon"):
        self.models_dir = Path(models_dir)
        self.archive_dir = self.models_dir / "archived_models"
        self.archive_dir.mkdir(exist_ok=True)
    
    def get_model_info(self):
        """Получить информацию о модели"""
        metadata_file = self.models_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            return metadata
        return None
    
    def archive_old_models(self, keep_best=True):
        """Архивировать старые модели, оставив только лучшую"""
        models_path = self.models_dir / "models"
        if not models_path.exists():
            logger.warning("Папка models не найдена")
            return
        
        # Создаем архивную папку с timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = self.archive_dir / f"models_{timestamp}"
        archive_path.mkdir(exist_ok=True)
        
        # Перемещаем все модели в архив
        for model_dir in models_path.iterdir():
            if model_dir.is_dir():
                shutil.move(str(model_dir), str(archive_path / model_dir.name))
        
        logger.info(f"Модели архивированы в: {archive_path}")
        
        if keep_best:
            # Оставляем только лучшую модель
            self._keep_best_model_only()
    
    def _keep_best_model_only(self):
        """Оставить только лучшую модель"""
        # Создаем папку models заново
        models_path = self.models_dir / "models"
        models_path.mkdir(exist_ok=True)
        
        # Копируем только WeightedEnsemble_L2_FULL (лучшая модель)
        best_model = "WeightedEnsemble_L2_FULL"
        archive_dirs = list(self.archive_dir.glob("models_*"))
        if archive_dirs:
            latest_archive = max(archive_dirs, key=os.path.getctime)
            best_model_path = latest_archive / best_model
            if best_model_path.exists():
                shutil.copytree(best_model_path, models_path / best_model)
                logger.info(f"Сохранена лучшая модель: {best_model}")
    
    def clean_utils_cache(self):
        """Очистить кэш данных"""
        utils_path = self.models_dir / "utils"
        if utils_path.exists():
            shutil.rmtree(utils_path)
            logger.info("Кэш данных очищен")
    
    def get_model_size(self):
        """Получить размер модели в MB"""
        total_size = 0
        for root, dirs, files in os.walk(self.models_dir):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        return total_size / (1024 * 1024)  # MB
    
    def list_archived_models(self):
        """Список архивированных моделей"""
        archives = list(self.archive_dir.glob("models_*"))
        return [archive.name for archive in archives]
    
    def restore_model(self, archive_name, model_name="WeightedEnsemble_L2_FULL"):
        """Восстановить модель из архива"""
        archive_path = self.archive_dir / archive_name
        if not archive_path.exists():
            logger.error(f"Архив {archive_name} не найден")
            return False
        
        model_path = archive_path / model_name
        if not model_path.exists():
            logger.error(f"Модель {model_name} не найдена в архиве")
            return False
        
        # Восстанавливаем модель
        target_path = self.models_dir / "models" / model_name
        if target_path.exists():
            shutil.rmtree(target_path)
        
        shutil.copytree(model_path, target_path)
        logger.info(f"Модель {model_name} восстановлена из архива {archive_name}")
        return True

def main():
    """Основная функция"""
    manager = AutoGluonModelManager()
    
    print("🔧 AutoGluon Model Manager")
    print("=" * 40)
    
    # Информация о модели
    model_info = manager.get_model_info()
    if model_info:
        print(f"📊 Модель: {model_info.get('name', 'Unknown')}")
        print(f"📅 Дата создания: {model_info.get('date', 'Unknown')}")
    
    # Размер модели
    size_mb = manager.get_model_size()
    print(f"💾 Размер модели: {size_mb:.2f} MB")
    
    # Список архивов
    archives = manager.list_archived_models()
    print(f"📦 Архивированных моделей: {len(archives)}")
    
    # Опции управления
    print("\n🎯 Доступные действия:")
    print("1. Архивировать старые модели")
    print("2. Очистить кэш данных")
    print("3. Показать размер модели")
    print("4. Список архивов")
    
    choice = input("\nВыберите действие (1-4): ").strip()
    
    if choice == "1":
        manager.archive_old_models(keep_best=True)
        print("✅ Модели архивированы, лучшая модель сохранена")
    elif choice == "2":
        manager.clean_utils_cache()
        print("✅ Кэш данных очищен")
    elif choice == "3":
        print(f"💾 Размер модели: {size_mb:.2f} MB")
    elif choice == "4":
        archives = manager.list_archived_models()
        if archives:
            print("📦 Архивированные модели:")
            for archive in archives:
                print(f"  - {archive}")
        else:
            print("📦 Архивов не найдено")

if __name__ == "__main__":
    main()
