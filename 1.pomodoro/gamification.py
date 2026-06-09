"""
ゲーミフィケーション要素の実装
- XP・レベルシステム
- バッジシステム
- ストリーク機能
- 統計機能
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from enum import Enum


class Badge(Enum):
    """バッジの種類"""
    THREE_DAY_STREAK = "three_day_streak"  # 3日連続
    TEN_WEEKLY = "ten_weekly"  # 週10回
    THIRTY_MONTHLY = "thirty_monthly"  # 月30回
    FIFTY_POMODOROS = "fifty_pomodoros"  # 50回達成
    HUNDRED_POMODOROS = "hundred_pomodoros"  # 100回達成


class XPSystem:
    """XP・レベルシステム"""

    # 定数
    XP_PER_POMODORO = 10  # 1ポモドーロあたりのXP
    XP_PER_LEVEL = 100  # レベルアップに必要なXP

    def __init__(self, total_xp: int = 0):
        self.total_xp = total_xp

    @property
    def current_level(self) -> int:
        """現在のレベルを計算"""
        return self.total_xp // self.XP_PER_LEVEL + 1

    @property
    def xp_in_level(self) -> int:
        """現在のレベル内での経験値"""
        return self.total_xp % self.XP_PER_LEVEL

    @property
    def xp_to_next_level(self) -> int:
        """次のレベルまでの必要XP"""
        return self.XP_PER_LEVEL - self.xp_in_level

    @property
    def level_progress(self) -> float:
        """レベルの進捗率 (0.0～1.0)"""
        return self.xp_in_level / self.XP_PER_LEVEL

    def add_xp(self, pomodoro_count: int = 1) -> Tuple[int, bool]:
        """
        XPを追加

        Args:
            pomodoro_count: ポモドーロの数

        Returns:
            (新しいXP, レベルアップしたか)
        """
        old_level = self.current_level
        self.total_xp += pomodoro_count * self.XP_PER_POMODORO
        new_level = self.current_level
        return self.total_xp, new_level > old_level

    def to_dict(self) -> Dict:
        """辞書形式で返す"""
        return {
            "total_xp": self.total_xp,
            "current_level": self.current_level,
            "xp_in_level": self.xp_in_level,
            "xp_to_next_level": self.xp_to_next_level,
            "level_progress": self.level_progress,
        }


class StreakTracker:
    """ストリーク追跡（連続日数）"""

    def __init__(self, current_streak: int = 0, last_pomodoro_date: str = ""):
        self.current_streak = current_streak
        self.last_pomodoro_date = last_pomodoro_date  # YYYY-MM-DD format
        self.max_streak = current_streak

    def record_pomodoro(self) -> bool:
        """
        ポモドーロを記録

        Returns:
            ストリークが更新されたか
        """
        today = datetime.now().strftime("%Y-%m-%d")

        if not self.last_pomodoro_date:
            # 最初のポモドーロ
            self.current_streak = 1
            self.last_pomodoro_date = today
            self.max_streak = max(self.max_streak, self.current_streak)
            return False

        last_date = datetime.strptime(self.last_pomodoro_date, "%Y-%m-%d")
        today_date = datetime.strptime(today, "%Y-%m-%d")
        days_diff = (today_date - last_date).days

        if days_diff == 0:
            # 同じ日 - ストリーク変更なし
            return False
        elif days_diff == 1:
            # 前日からの継続
            self.current_streak += 1
            self.max_streak = max(self.max_streak, self.current_streak)
            self.last_pomodoro_date = today
            return True
        else:
            # 連続中断 - ストリークリセット
            self.current_streak = 1
            self.last_pomodoro_date = today
            return False

    def to_dict(self) -> Dict:
        """辞書形式で返す"""
        return {
            "current_streak": self.current_streak,
            "max_streak": self.max_streak,
            "last_pomodoro_date": self.last_pomodoro_date,
        }


class BadgeSystem:
    """バッジシステム"""

    def __init__(self, earned_badges: List[str] = None):
        self.earned_badges = earned_badges or []

    def add_badge(self, badge: Badge) -> bool:
        """
        バッジを追加

        Returns:
            新しく獲得したか
        """
        badge_value = badge.value
        if badge_value not in self.earned_badges:
            self.earned_badges.append(badge_value)
            return True
        return False

    def has_badge(self, badge: Badge) -> bool:
        """バッジを持っているか確認"""
        return badge.value in self.earned_badges

    def to_dict(self) -> Dict:
        """辞書形式で返す"""
        return {
            "earned_badges": self.earned_badges,
            "count": len(self.earned_badges),
        }


class Statistics:
    """統計情報"""

    def __init__(self, pomodoro_history: List[Dict] = None):
        self.pomodoro_history = pomodoro_history or []  # [{date, count}, ...]

    def add_pomodoro_session(self, count: int = 1, date: str = ""):
        """ポモドーロセッションを追加"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # 同じ日付があるかチェック
        for entry in self.pomodoro_history:
            if entry["date"] == date:
                entry["count"] += count
                return

        # 新しい日付
        self.pomodoro_history.append({"date": date, "count": count})

    def get_weekly_stats(self) -> Dict:
        """今週の統計を取得"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_start_str = week_start.strftime("%Y-%m-%d")

        total_count = 0
        for entry in self.pomodoro_history:
            if entry["date"] >= week_start_str:
                total_count += entry["count"]

        return {
            "week_start": week_start_str,
            "total_pomodoros": total_count,
            "days_active": len(
                [e for e in self.pomodoro_history if e["date"] >= week_start_str]
            ),
        }

    def get_monthly_stats(self) -> Dict:
        """今月の統計を取得"""
        today = datetime.now()
        month_start = today.replace(day=1)
        month_start_str = month_start.strftime("%Y-%m-%d")

        total_count = 0
        for entry in self.pomodoro_history:
            if entry["date"] >= month_start_str:
                total_count += entry["count"]

        return {
            "month_start": month_start_str,
            "total_pomodoros": total_count,
            "days_active": len(
                [e for e in self.pomodoro_history if e["date"] >= month_start_str]
            ),
        }

    def get_total_pomodoros(self) -> int:
        """総ポモドーロ数"""
        return sum(entry["count"] for entry in self.pomodoro_history)

    def to_dict(self) -> Dict:
        """辞書形式で返す"""
        return {
            "total_pomodoros": self.get_total_pomodoros(),
            "history": self.pomodoro_history,
            "weekly_stats": self.get_weekly_stats(),
            "monthly_stats": self.get_monthly_stats(),
        }


class GamificationEngine:
    """ゲーミフィケーションエンジン"""

    def __init__(
        self,
        xp_system: XPSystem = None,
        streak_tracker: StreakTracker = None,
        badge_system: BadgeSystem = None,
        statistics: Statistics = None,
    ):
        self.xp_system = xp_system or XPSystem()
        self.streak_tracker = streak_tracker or StreakTracker()
        self.badge_system = badge_system or BadgeSystem()
        self.statistics = statistics or Statistics()

    def record_pomodoro_completion(self, count: int = 1) -> Dict:
        """
        ポモドーロ完了を記録

        Returns:
            {
                'xp_gained': int,
                'level_up': bool,
                'new_level': int,
                'streak_updated': bool,
                'current_streak': int,
                'new_badges': list[Badge],
                'stats': dict
            }
        """
        # XPを追加
        old_level = self.xp_system.current_level
        new_xp, level_up = self.xp_system.add_xp(count)

        # ストリークを記録
        streak_updated = self.streak_tracker.record_pomodoro()

        # 統計を追加
        self.statistics.add_pomodoro_session(count)

        # バッジをチェック
        new_badges = self._check_badges()

        result = {
            "xp_gained": count * XPSystem.XP_PER_POMODORO,
            "level_up": level_up,
            "new_level": self.xp_system.current_level,
            "streak_updated": streak_updated,
            "current_streak": self.streak_tracker.current_streak,
            "new_badges": new_badges,
            "stats": self.get_stats(),
        }

        return result

    def _check_badges(self) -> List[Badge]:
        """
        新しく獲得したバッジをチェック

        Returns:
            新しく獲得したバッジのリスト
        """
        new_badges = []

        # 3日連続チェック
        if (
            self.streak_tracker.current_streak >= 3
            and not self.badge_system.has_badge(Badge.THREE_DAY_STREAK)
        ):
            if self.badge_system.add_badge(Badge.THREE_DAY_STREAK):
                new_badges.append(Badge.THREE_DAY_STREAK)

        # 週10回チェック
        weekly_stats = self.statistics.get_weekly_stats()
        if (
            weekly_stats["total_pomodoros"] >= 10
            and not self.badge_system.has_badge(Badge.TEN_WEEKLY)
        ):
            if self.badge_system.add_badge(Badge.TEN_WEEKLY):
                new_badges.append(Badge.TEN_WEEKLY)

        # 月30回チェック
        monthly_stats = self.statistics.get_monthly_stats()
        if (
            monthly_stats["total_pomodoros"] >= 30
            and not self.badge_system.has_badge(Badge.THIRTY_MONTHLY)
        ):
            if self.badge_system.add_badge(Badge.THIRTY_MONTHLY):
                new_badges.append(Badge.THIRTY_MONTHLY)

        # 50回達成チェック
        total_pomodoros = self.statistics.get_total_pomodoros()
        if (
            total_pomodoros >= 50
            and not self.badge_system.has_badge(Badge.FIFTY_POMODOROS)
        ):
            if self.badge_system.add_badge(Badge.FIFTY_POMODOROS):
                new_badges.append(Badge.FIFTY_POMODOROS)

        # 100回達成チェック
        if (
            total_pomodoros >= 100
            and not self.badge_system.has_badge(Badge.HUNDRED_POMODOROS)
        ):
            if self.badge_system.add_badge(Badge.HUNDRED_POMODOROS):
                new_badges.append(Badge.HUNDRED_POMODOROS)

        return new_badges

    def get_stats(self) -> Dict:
        """全統計を取得"""
        return {
            "xp": self.xp_system.to_dict(),
            "streak": self.streak_tracker.to_dict(),
            "badges": self.badge_system.to_dict(),
            "statistics": self.statistics.to_dict(),
        }

    def to_dict(self) -> Dict:
        """全データを辞書形式で返す"""
        return {
            "xp_system": self.xp_system.to_dict(),
            "streak_tracker": self.streak_tracker.to_dict(),
            "badge_system": self.badge_system.to_dict(),
            "statistics": self.statistics.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "GamificationEngine":
        """辞書からインスタンスを作成"""
        xp_data = data.get("xp_system", {})
        xp_system = XPSystem(total_xp=xp_data.get("total_xp", 0))

        streak_data = data.get("streak_tracker", {})
        streak_tracker = StreakTracker(
            current_streak=streak_data.get("current_streak", 0),
            last_pomodoro_date=streak_data.get("last_pomodoro_date", ""),
        )

        badge_data = data.get("badge_system", {})
        badge_system = BadgeSystem(earned_badges=badge_data.get("earned_badges", []))

        stats_data = data.get("statistics", {})
        statistics = Statistics(
            pomodoro_history=stats_data.get("history", [])
        )

        return cls(xp_system, streak_tracker, badge_system, statistics)
