"""
ゲーミフィケーション機能の統合テスト
全体の動作確認
"""

import tempfile
import json
from gamification import GamificationEngine, Badge
from data_manager import DataManager


def test_gamification_scenario():
    """実際の利用シナリオをテスト"""
    print("=" * 60)
    print("統合テスト: ゲーミフィケーション機能")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        dm = DataManager(tmpdir)
        engine = GamificationEngine()

        print("\n【初期状態】")
        stats = engine.get_stats()
        print(f"  レベル: {stats['xp']['current_level']}")
        print(f"  XP: {stats['xp']['total_xp']}")
        print(f"  ストリーク: {stats['streak']['current_streak']}")
        print(f"  バッジ数: {stats['badges']['count']}")
        print(f"  総ポモドーロ: {stats['statistics']['total_pomodoros']}")

        print("\n【シナリオ1: 5ポモドーロ完了】")
        for i in range(5):
            result = engine.record_pomodoro_completion(1)
            print(f"  {i+1}番目: XP {result['xp_gained']} 獲得")

        stats = engine.get_stats()
        print(f"  → レベル: {stats['xp']['current_level']}")
        print(f"  → XP: {stats['xp']['total_xp']}")
        print(f"  → ストリーク: {stats['streak']['current_streak']}")

        print("\n【シナリオ2: 10ポモドーロ追加完了（合計15）】")
        result = engine.record_pomodoro_completion(10)
        print(f"  XP {result['xp_gained']} 獲得")
        print(f"  レベルアップ: {result['level_up']}")
        print(f"  新しいレベル: {result['new_level']}")
        if result["new_badges"]:
            print(f"  新バッジ: {[b.value for b in result['new_badges']]}")

        stats = engine.get_stats()
        print(f"  → レベル: {stats['xp']['current_level']}")
        print(f"  → XP: {stats['xp']['total_xp']}")
        print(f"  → 次のレベルまで: {stats['xp']['xp_to_next_level']} XP")

        print("\n【統計情報】")
        weekly = stats['statistics']['weekly_stats']
        monthly = stats['statistics']['monthly_stats']
        print(f"  総ポモドーロ: {stats['statistics']['total_pomodoros']}")
        print(f"  今週: {weekly['total_pomodoros']} ポモドーロ ({weekly['days_active']} 日間)")
        print(f"  今月: {monthly['total_pomodoros']} ポモドーロ ({monthly['days_active']} 日間)")

        print("\n【バッジ情報】")
        if stats['badges']['earned_badges']:
            print(f"  獲得バッジ: {stats['badges']['earned_badges']}")
        else:
            print("  獲得バッジ: なし")

        print("\n【データ永続化テスト】")
        dm.save_gamification_data(engine)
        print("  ✓ データを保存しました")

        loaded_engine = dm.load_gamification_data()
        loaded_stats = loaded_engine.get_stats()
        print("  ✓ データを読み込みました")

        assert loaded_stats['xp']['total_xp'] == stats['xp']['total_xp']
        assert (
            loaded_stats['statistics']['total_pomodoros']
            == stats['statistics']['total_pomodoros']
        )
        print("  ✓ データが一致しました")

        print("\n【XPから次のレベルまでの詳細】")
        xp_info = loaded_engine.xp_system.to_dict()
        print(f"  現在レベル: {xp_info['current_level']}")
        print(f"  総XP: {xp_info['total_xp']}")
        print(f"  今のレベル内XP: {xp_info['xp_in_level']} / 100")
        print(f"  進捗: {xp_info['level_progress']*100:.1f}%")
        print(f"  次のレベルまで: {xp_info['xp_to_next_level']} XP")

        print("\n" + "=" * 60)
        print("✓ すべてのテストが完了しました")
        print("=" * 60)


def test_badge_acquisition():
    """バッジ獲得テスト"""
    print("\n" + "=" * 60)
    print("テスト: バッジ獲得シナリオ")
    print("=" * 60)

    engine = GamificationEngine()

    print("\n【週10回達成テスト】")
    result = engine.record_pomodoro_completion(10)
    print(f"  10ポモドーロ完了")
    print(f"  新バッジ: {[b.value for b in result['new_badges']] if result['new_badges'] else 'なし'}")

    stats = engine.get_stats()
    weekly_stats = stats['statistics']['weekly_stats']
    print(f"  今週の統計: {weekly_stats['total_pomodoros']} ポモドーロ")

    print("\n" + "=" * 60)


def test_level_progression():
    """レベル進行テスト"""
    print("\n" + "=" * 60)
    print("テスト: レベル進行")
    print("=" * 60)

    engine = GamificationEngine()

    print("\n【100ポモドーロまでのレベル進行】")
    for level_target in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        xp_needed = (level_target - 1) * 100
        pomodoros_needed = max(0, (xp_needed - engine.xp_system.total_xp) // 10)

        if pomodoros_needed > 0:
            engine.record_pomodoro_completion(pomodoros_needed)

        current_level = engine.xp_system.current_level
        print(f"  レベル {current_level}: XP {engine.xp_system.total_xp}")

        if current_level >= 11:
            break

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_gamification_scenario()
    test_badge_acquisition()
    test_level_progression()
    print("\n✅ すべての統合テストが完了しました！\n")
