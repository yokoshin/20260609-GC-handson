architecture.md と features.md を確認しながら、UIモックも踏まえた実装計画を整理します。  

Read [](file:///workspaces/20260609-GC-handson/architecture.md#1-1), lines 1 to 50

Read [](file:///workspaces/20260609-GC-handson/features.md#1-1), lines 1 to 80

内容を確認できました。以下に段階的な実装計画を提案します。

---

## 段階的な実装計画

### Step 1: プロジェクト基盤の準備

**目的**: Flask が起動して画面が返せる最小構成を作る

実装内容:
- `requirements.txt` に Flask を記述
- app.py に Flask 起動コードと `GET /` ルートを実装
- `templates/index.html` にプレースホルダーを作成
- `static/css/style.css` を空で用意

確認できること:
- `python app.py` でサーバーが起動すること
- ブラウザでページが表示されること

---

### Step 2: タイマーのドメインモデルと状態管理

**目的**: タイマーの状態を扱うコアロジックをFlask無しで書き、単体テストで動作確認する

実装内容:
- `models/timer_state.py` に `TimerState` クラスを実装
  - フィールド: `phase`, `status`, `duration`, `elapsed`, `sessions_completed`
- `services/timer_service.py` に `TimerService` クラスを実装
  - メソッド: `start()`, `pause()`, `resume()`, `reset()`, `tick(seconds)`, `complete_session()`
- `repositories/session_repository.py` にメモリ実装を用意
- `tests/test_timer_service.py` で単体テストを作成

確認できること:
- `start()` で status が `running` になる
- `tick()` で elapsed が増え、duration に達したら完了検知される
- `reset()` で初期状態に戻る

---

### Step 3: バックエンド API の実装

**目的**: タイマー操作を HTTP 経由で扱えるようにする

実装内容:
- app.py に API エンドポイントを実装
  - `POST /api/timer/start`
  - `POST /api/timer/pause`
  - `POST /api/timer/resume`
  - `POST /api/timer/reset`
  - `GET /api/timer/status`
- `tests/test_api.py` に Flask `test_client` を使ったテストを実装

確認できること:
- `curl` や `test_client` でAPIを叩いて状態が変わること
- status レスポンスに正しい JSON が返ること

---

### Step 4: 基本UIの実装（タイマー表示とボタン）

**目的**: モックの中央部分（時間表示・開始・リセット）を動かす

実装内容:
- `index.html` にタイマー表示エリアとボタンを配置
- `timer.js` に以下を実装:
  - `GET /api/timer/status` を定期ポーリング（1秒間隔）
  - `mm:ss` 形式の時間フォーマット関数
  - ボタンクリックで API を呼び出す処理
  - フェーズラベル（「作業中」「休憩中」）の切替表示
- `style.css` に基本レイアウトを追加

確認できること:
- 開始ボタンを押したら画面のカウントダウンが動き始める
- リセットで 25:00 に戻る
- ラベルが「作業中」「休憩中」で切り替わる

---

### Step 5: 円形プログレスリングの実装

**目的**: UIモックの中心にある円弧アニメーションを再現する

実装内容:
- SVG を使った円形プログレスリングを `index.html` に実装
- `timer.js` に残り時間の割合から円弧の描画量を計算する関数を追加
- `style.css` でリングの配色とアニメーションを調整（モックのブルー/グレー）

確認できること:
- タイマーが進むにつれて円弧が徐々に減っていく
- 作業フェーズと休憩フェーズで色が変わる

---

### Step 6: 進捗パネルの実装

**目的**: 今日の進捗（完了セッション数・集中時間）を表示する

実装内容:
- `GET /api/stats` エンドポイントを app.py に追加
- `TimerService` に集中時間集計ロジックを追加
- 日付が変わったら進捗をリセットする処理を追加
- `index.html` に進捗パネルを追加
- `timer.js` から定期的に `/api/stats` を取得して表示を更新

確認できること:
- セッション完了のたびに「完了」数が増える
- 集中時間が正しく累積される
- 翌日になるとリセットされる

---

### Step 7: 通知機能の実装

**目的**: セッション完了時にブラウザ通知と音声で知らせる

実装内容:
- `timer.js` に Web Notification API の呼び出しを追加
- セッション完了時に通知音を再生する処理を追加（Audio API）
- 通知権限のリクエスト処理を追加

確認できること:
- タイマー終了時にブラウザ通知が表示される
- 通知音が鳴る

---

### Step 8: スタイル仕上げ

**目的**: UIモックに近いデザインに仕上げる

実装内容:
- モックのカラースキーム（薄紫の背景・ブルーのアクセント）に合わせる
- ボタンのスタイルを調整（「開始」は塗り、「リセット」はアウトライン）
- カードレイアウト・角丸・影の調整
- レスポンシブ対応

---

### まとめ

```
Step 1: Flask 起動 + 空ページ表示
Step 2: タイマーロジック実装 + 単体テスト
Step 3: バックエンド API 実装 + APIテスト
Step 4: 基本 UI（時間表示・ボタン動作）
Step 5: 円形プログレスリング
Step 6: 今日の進捗パネル
Step 7: 通知機能
Step 8: スタイル仕上げ
```

各Stepは独立して動作確認できる粒度にしているため、1Stepごとにコミットしながら進めやすい構成です。