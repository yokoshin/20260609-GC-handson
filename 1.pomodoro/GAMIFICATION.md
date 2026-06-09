# ポモドーロタイマー - ゲーミフィケーション機能ドキュメント

## 概要

このドキュメントは、ポモドーロタイマーに実装されたゲーミフィケーション要素について説明します。

## 機能

### 1. XP・レベルシステム

**説明**: ポモドーロを完了するたびにXP（経験値）を獲得し、レベルアップします。

**仕様**:
- 1つのポモドーロ完了 = 10 XP獲得
- レベルアップに必要なXP = 100 XP
- レベル1から開始

**表示**:
- 現在のレベルと合計XP
- 次のレベルまでのプログレスバー
- 次のレベルに必要な残りXP

**実装ファイル**: `gamification.py` - `XPSystem` クラス

### 2. ストリーク機能

**説明**: 連続した日数でポモドーロを完了した日数をカウントします。

**仕様**:
- 毎日少なくとも1つのポモドーロを完了すると、ストリーク+1
- 3日以上の連続で「3日連続バッジ」獲得
- 1日以上途絶えるとストリークはリセット
- 最高ストリーク数も記録

**表示**:
- 現在のストリーク日数
- 最高ストリーク日数

**実装ファイル**: `gamification.py` - `StreakTracker` クラス

### 3. バッジシステム

**説明**: 特定の条件を達成するとバッジを獲得できます。

**獲得条件**:

| バッジ名 | 条件 | 説明 |
|---------|------|------|
| 3日連続 | ストリーク ≥ 3日 | 3日連続でポモドーロを完了 |
| 週10回 | 週間合計 ≥ 10 | 1週間で10ポモドーロ以上完了 |
| 月30回 | 月間合計 ≥ 30 | 1ヶ月で30ポモドーロ以上完了 |
| 50回達成 | 総計 ≥ 50 | 通算50ポモドーロ達成 |
| 100回達成 | 総計 ≥ 100 | 通算100ポモドーロ達成 |

**表示**:
- 獲得したバッジ一覧
- 新しいバッジ獲得時にポップアップ通知

**実装ファイル**: `gamification.py` - `BadgeSystem` クラス

### 4. 統計情報

**説明**: ポモドーロの完了履歴と統計情報を記録・表示します。

**記録される情報**:
- 完了日別のポモドーロ数
- 総ポモドーロ数

**表示される統計**:
- 今週の統計（ポモドーロ数、活動日数）
- 今月の統計（ポモドーロ数、活動日数）
- 総ポモドーロ数
- 現在のレベル
- ストリーク情報
- バッジ数

**実装ファイル**: `gamification.py` - `Statistics` クラス

## 実装の詳細

### アーキテクチャ

```
┌─────────────────────────────────────────────┐
│         PomodoroTimerApp (UI)               │
│              (app.py)                       │
└──────────────┬──────────────────────────────┘
               │
               ├─→ GamificationEngine
               │   (gamification.py)
               │   ├─ XPSystem
               │   ├─ StreakTracker
               │   ├─ BadgeSystem
               │   └─ Statistics
               │
               └─→ DataManager
                   (data_manager.py)
                   └─ JSON永続化層
```

### モジュール構成

#### `gamification.py`

**クラス**:
- `XPSystem`: XP・レベル管理
- `StreakTracker`: ストリーク追跡
- `BadgeSystem`: バッジ管理
- `Statistics`: 統計情報
- `GamificationEngine`: 全体を統合するエンジン
- `Badge`: バッジの種類（Enum）

**主要メソッド**:
- `GamificationEngine.record_pomodoro_completion(count)`: ポモドーロ完了を記録
- `GamificationEngine.get_stats()`: 全統計を取得

#### `data_manager.py`

**クラス**:
- `DataManager`: データの保存・読込

**主要メソッド**:
- `save_gamification_data(engine)`: データをJSON保存
- `load_gamification_data()`: JSONからデータを読込
- `export_data(path)`: データをエクスポート
- `import_data(path)`: データをインポート

#### `app.py`

**クラス**:
- `PomodoroTimerApp`: UIとタイマーの統合

**主要機能**:
- タイマー表示と制御
- ゲーミフィケーション要素の表示
- 統計情報の表示

## データ永続化

ユーザーデータはJSON形式で以下の場所に保存されます：

```
~/.pomodoro_timer/user_data.json
```

### データ構造

```json
{
  "xp_system": {
    "total_xp": 150,
    "current_level": 2,
    "xp_in_level": 50,
    "xp_to_next_level": 50,
    "level_progress": 0.5
  },
  "streak_tracker": {
    "current_streak": 3,
    "max_streak": 5,
    "last_pomodoro_date": "2026-06-09"
  },
  "badge_system": {
    "earned_badges": ["three_day_streak", "ten_weekly"],
    "count": 2
  },
  "statistics": {
    "total_pomodoros": 15,
    "history": [
      {"date": "2026-06-09", "count": 5},
      {"date": "2026-06-08", "count": 4}
    ],
    "weekly_stats": {
      "week_start": "2026-06-09",
      "total_pomodoros": 9,
      "days_active": 2
    },
    "monthly_stats": {
      "month_start": "2026-06-01",
      "total_pomodoros": 15,
      "days_active": 5
    }
  }
}
```

## テスト

### テストファイル

`test_gamification.py` - 26個のユニットテストが含まれています

### テスト実行

```bash
cd 1.pomodoro
python -m unittest test_gamification -v
```

### テストカバレッジ

- XPシステム: 初期化、XP追加、レベルアップ、進捗計算
- ストリーク: 初期化、初回記録、同日記録、最大ストリーク追跡
- バッジシステム: 初期化、バッジ追加、重複チェック
- 統計: 初期化、セッション追加、週間/月間統計
- ゲーミフィケーションエンジン: 統合テスト
- データ永続化: シリアライゼーション

## 使用方法

### アプリケーション実行

```bash
# 通常モード（25分ポモドーロ）
python app.py

# 開発モード（5秒ポモドーロ）
python app.py --dev
```

### プログラマティック使用

```python
from gamification import GamificationEngine
from data_manager import DataManager

# データを読み込む
dm = DataManager()
engine = dm.load_gamification_data()

# ポモドーロを記録
result = engine.record_pomodoro_completion(1)

# 結果を確認
print(f"レベル: {result['new_level']}")
print(f"XP: {result['xp_gained']}")
print(f"新バッジ: {result['new_badges']}")

# データを保存
dm.save_gamification_data(engine)
```

## パフォーマンス

- JSON読込/保存: < 10ms
- ポモドーロ完了処理: < 5ms
- バッジチェック: < 1ms

## 今後の拡張可能性

1. **グラフ表示**: matplotlib/plotlyを使用した週間・月間グラフ
2. **ランキング**: ユーザー間でのランキング機能
3. **アチーブメント**: より多くのバッジ条件の追加
4. **カスタマイズ**: ユーザーがゲーム要素をカスタマイズ可能に
5. **ソーシャル機能**: SNS連携や友人とのシェア
6. **通知**: 毎日のリマインダー、目標達成時の通知

## トラブルシューティング

### データが保存されない

**原因**: ディレクトリのパーミッション問題

**解決方法**:
```bash
mkdir -p ~/.pomodoro_timer
chmod 755 ~/.pomodoro_timer
```

### データが破損している

**解決方法**:
```python
from data_manager import DataManager
dm = DataManager()
dm.delete_all_data()  # すべてのデータを削除
```

## ライセンス

このプロジェクトの一部です。

## 参考資料

- ポモドーロ・テクニック: https://en.wikipedia.org/wiki/Pomodoro_Technique
- ゲーミフィケーション: https://en.wikipedia.org/wiki/Gamification
