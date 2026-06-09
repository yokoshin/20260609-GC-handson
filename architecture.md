# Pomodoro Timer Web App アーキテクチャ案

## 1. 目的
Flask + HTML/CSS/JavaScript を使って、ポモドーロタイマーのWebアプリを構築する。

目的は以下のとおり。
- シンプルに使えるタイマー機能を提供する
- 作業中/休憩中の状態を明確に表示する
- テストしやすい構成にして、今後の機能拡張にも耐えられる設計にする

---

## 2. 全体構成

```text
1.pomodoro/
├── app.py
├── services/
│   └── timer_service.py
├── models/
│   └── timer_state.py
├── repositories/
│   └── session_repository.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── timer.js
└── tests/
    ├── test_timer_service.py
    └── test_api.py
```

---

## 3. レイヤー構成

### 3.1 Presentation Layer
場所: `templates/`, `static/js/`, `static/css/`

責務:
- ユーザー操作を受け付ける
- タイマー画面の表示
- ボタンクリックや状態更新のイベント処理
- ブラウザ通知や音声通知の発火

実装方針:
- HTMLはテンプレートとして分離
- JavaScriptはモジュール化して責務ごとに関数化する
- UIロジックをAPI呼び出しに寄せ、DOM更新処理を最小限にする

---

### 3.2 Application Layer
場所: `services/timer_service.py`

責務:
- タイマー開始・一時停止・再開・リセット
- 作業/休憩フェーズの切替
- 経過時間と残り時間の計算
- セッション完了判定

特徴:
- Flask依存を持たないように設計する
- テストで直接呼び出しやすい構造にする

---

### 3.3 Domain Layer
場所: `models/timer_state.py`

責務:
- タイマー状態を表現するデータモデル
- 例: phase, status, duration, elapsed, sessionsCompleted

特徴:
- 状態を値オブジェクト的に管理する
- 画面表示やAPIレスポンスの基礎データになる

---

### 3.4 Infrastructure Layer
場所: `repositories/session_repository.py`

責務:
- タイマー状態の保存・取得
- 今後はメモリ実装、JSON実装、SQLite実装へ拡張可能にする

特徴:
- 状態保存方法を抽象化する
- テストでは fake repository を差し替えられるようにする

---

## 4. Flask の役割
Flask は主に以下を担当する。
- HTTP API の提供
- 画面の描画
- リクエストとレスポンスの橋渡し

Flask ルートは以下を意識して設計する。
- ビジネスロジックを持たない
- 入出力の変換だけに集中する
- テストでは `test_client` で呼び出しやすいようにする

---

## 5. API 設計案

### 5.1 タイマー制御
- `POST /api/timer/start`
  - タイマー開始
- `POST /api/timer/pause`
  - 一時停止
- `POST /api/timer/resume`
  - 再開
- `POST /api/timer/reset`
  - リセット

### 5.2 状態取得
- `GET /api/timer/status`
  - 現在の状態をJSONで返す

### 5.3 統計情報
- `GET /api/stats`
  - 完了セッション数や進行状況などを返す

---

## 6. 状態モデル案

```json
{
  "phase": "work",
  "status": "running",
  "duration": 1500,
  "elapsed": 450,
  "sessionsCompleted": 3,
  "lastUpdated": 1718000000
}
```

- `phase`: work / break
- `status`: idle / running / paused
- `duration`: 現在のセッション長（秒）
- `elapsed`: 経過時間（秒）
- `sessionsCompleted`: 完了したポモドーロ数

---

## 7. テスト容易性を高めるための設計ポイント

### 7.1 ロジックとHTTPを分離する
- タイマーの計算・状態遷移は `services/` に配置する
- Flask ルートは API 呼び出しの受付に限定する

### 7.2 時刻を注入可能にする
- 実時間取得は `SystemClock` に切り出す
- テストでは `FakeClock` を差し替える

### 7.3 状態保存を抽象化する
- 直接グローバル変数や辞書を使わず、repository を使う
- テスト用の fake repository を用意できるようにする

### 7.4 UIロジックも分離する
- `timer.js` は、API通信とDOM更新を明確に分ける
- できれば関数単位でテストできるように設計する

---

## 8. テスト戦略

### 単体テスト
- タイマーの進行
- フェーズ切替
- セッション完了判定
- 休憩時間の計算

### APIテスト
- Flask の `test_client` で `/api/...` を確認
- 状態の更新成功・失敗を検証

### UIテスト（将来）
- ボタン押下で表示が変わるか
- 通知が発火するか
- タイマー表示が更新されるか

---

## 9. 実装の進め方
1. まずは `app.py` に最小の Flask ルートを作る
2. `timer_service.py` でタイマー処理を切り出す
3. `templates/index.html` と `static/js/timer.js` でUIを組み立てる
4. `tests/` でロジックとAPIを確認する
5. 必要に応じて通知・統計機能を追加する

---

## 10. この設計のメリット
- コード責務が明確で保守しやすい
- Flask と JavaScript の役割が整理されている
- テストがしやすく、将来の機能追加に対応しやすい
- 既存のシンプル構成を維持しつつ拡張しやすい
