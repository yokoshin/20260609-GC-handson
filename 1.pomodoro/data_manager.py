"""
データ永続化レイヤー
JSONファイルを使用してユーザーデータを保存・読込
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from gamification import GamificationEngine


class DataManager:
    """データ永続化を管理"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = str(Path.home() / ".pomodoro_timer")
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "user_data.json"

    def save_gamification_data(self, engine: GamificationEngine) -> bool:
        """ゲーミフィケーションデータを保存"""
        try:
            data = engine.to_dict()
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_gamification_data(self) -> GamificationEngine:
        """ゲーミフィケーションデータを読込"""
        if not self.data_file.exists():
            # 新規作成
            return GamificationEngine()

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return GamificationEngine.from_dict(data)
        except Exception as e:
            print(f"Error loading data: {e}")
            return GamificationEngine()

    def delete_all_data(self) -> bool:
        """全データを削除"""
        try:
            if self.data_file.exists():
                os.remove(self.data_file)
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False

    def export_data(self, export_path: str) -> bool:
        """データをエクスポート"""
        try:
            engine = self.load_gamification_data()
            data = engine.to_dict()
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False

    def import_data(self, import_path: str) -> bool:
        """データをインポート"""
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            engine = GamificationEngine.from_dict(data)
            return self.save_gamification_data(engine)
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
