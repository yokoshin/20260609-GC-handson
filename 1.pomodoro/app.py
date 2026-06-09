"""
ポモドーロタイマー with ゲーミフィケーション要素
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from gamification import GamificationEngine, Badge
from data_manager import DataManager


class PomodoroTimerApp:
    """ポモドーロタイマーアプリケーション"""

    # 定数
    WORK_TIME = 25 * 60  # 25分
    BREAK_TIME = 5 * 60  # 5分
    WORK_TIME_DEV = 5  # 開発用: 5秒
    BREAK_TIME_DEV = 2  # 開発用: 2秒

    def __init__(self, root, dev_mode=False):
        self.root = root
        self.root.title("ポモドーロタイマー")
        self.root.geometry("800x900")
        self.root.resizable(False, False)

        # 開発モード
        self.dev_mode = dev_mode
        self.work_time = self.WORK_TIME_DEV if dev_mode else self.WORK_TIME
        self.break_time = self.BREAK_TIME_DEV if dev_mode else self.BREAK_TIME

        # ゲーミフィケーションエンジンとデータマネージャー
        self.data_manager = DataManager()
        self.engine = self.data_manager.load_gamification_data()

        # タイマー状態
        self.is_running = False
        self.is_work_time = True
        self.time_remaining = self.work_time
        self.timer_job = None
        self.sessions_completed = 0

        # UI構築
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """UIウィジェットを作成"""

        # メインフレーム
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ===== ヘッダー（レベルとストリーク）=====
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)

        # レベル表示
        level = self.engine.xp_system.current_level
        xp_data = self.engine.xp_system.to_dict()
        level_label = ttk.Label(
            header_frame,
            text=f"🏆 レベル {level} | XP: {xp_data['total_xp']}",
            font=("Arial", 14, "bold"),
        )
        level_label.pack(side=tk.LEFT, padx=5)

        # ストリーク表示
        streak = self.engine.streak_tracker.current_streak
        streak_label = ttk.Label(
            header_frame,
            text=f"🔥 ストリーク: {streak}日",
            font=("Arial", 14, "bold"),
            foreground="orange",
        )
        streak_label.pack(side=tk.LEFT, padx=20)
        self.streak_label = streak_label

        # ===== タイマー表示 =====
        timer_frame = ttk.LabelFrame(main_frame, text="タイマー")
        timer_frame.pack(fill=tk.X, pady=20)

        # 時間表示（大きく）
        self.time_label = ttk.Label(
            timer_frame, text="25:00", font=("Arial", 72, "bold")
        )
        self.time_label.pack(pady=20)

        # 仕事/休憩の状態表示
        self.state_label = ttk.Label(
            timer_frame, text="仕事時間", font=("Arial", 18)
        )
        self.state_label.pack(pady=10)

        # プログレスバー
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            timer_frame, variable=self.progress_var, maximum=100, length=400
        )
        self.progress_bar.pack(pady=10, fill=tk.X, padx=20)

        # ===== コントロールボタン =====
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=20)

        self.start_button = ttk.Button(
            control_frame, text="スタート", command=self.start_timer
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(
            control_frame, text="一時停止", command=self.pause_timer, state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(
            control_frame, text="リセット", command=self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.skip_button = ttk.Button(
            control_frame, text="スキップ", command=self.skip_timer
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)

        # ===== XP・レベル情報 =====
        xp_frame = ttk.LabelFrame(main_frame, text="経験値・レベル")
        xp_frame.pack(fill=tk.X, pady=10)

        xp_progress_frame = ttk.Frame(xp_frame)
        xp_progress_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(xp_progress_frame, text="次のレベルまで:").pack(side=tk.LEFT)
        self.xp_progress_var = tk.DoubleVar()
        xp_progress_bar = ttk.Progressbar(
            xp_progress_frame,
            variable=self.xp_progress_var,
            maximum=100,
            length=300,
        )
        xp_progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.xp_text_label = ttk.Label(
            xp_progress_frame, text="", font=("Arial", 10)
        )
        self.xp_text_label.pack(side=tk.LEFT, padx=5)

        # ===== バッジ表示 =====
        badge_frame = ttk.LabelFrame(main_frame, text="獲得バッジ")
        badge_frame.pack(fill=tk.X, pady=10)

        self.badge_label = ttk.Label(
            badge_frame, text="バッジを獲得して、この欄に表示されます", wraplength=400
        )
        self.badge_label.pack(padx=10, pady=10)
        self.update_badges_display()

        # ===== 統計 =====
        stats_frame = ttk.LabelFrame(main_frame, text="統計")
        stats_frame.pack(fill=tk.X, pady=10)

        stats_text_frame = ttk.Frame(stats_frame)
        stats_text_frame.pack(fill=tk.X, padx=10, pady=10)

        self.stats_text = tk.Text(stats_text_frame, height=6, width=80)
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(stats_text_frame, command=self.stats_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_text.config(yscrollcommand=scrollbar.set)
        self.stats_text.config(state=tk.DISABLED)

        self.update_stats_display()

        # ===== セッション完了カウンター =====
        session_frame = ttk.Frame(main_frame)
        session_frame.pack(fill=tk.X, pady=10)

        ttk.Label(session_frame, text="セッション完了数:", font=("Arial", 12)).pack(
            side=tk.LEFT
        )
        self.session_label = ttk.Label(
            session_frame, text="0", font=("Arial", 12, "bold")
        )
        self.session_label.pack(side=tk.LEFT, padx=10)

    def start_timer(self):
        """タイマーを開始"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.timer_loop()

    def pause_timer(self):
        """タイマーを一時停止"""
        self.is_running = False
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def reset_timer(self):
        """タイマーをリセット"""
        self.is_running = False
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.is_work_time = True
        self.time_remaining = self.work_time
        self.sessions_completed = 0
        self.update_display()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def skip_timer(self):
        """タイマーをスキップ"""
        # スキップ時はポイントを付与しない（実作業ではないため）
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.is_work_time = not self.is_work_time
        self.time_remaining = (
            self.break_time if not self.is_work_time else self.work_time
        )
        self.is_running = False
        self.update_display()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def timer_loop(self):
        """タイマーループ"""
        if not self.is_running:
            return

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
        else:
            # タイマー完了
            if self.is_work_time:
                self.on_work_complete()
            else:
                self.on_break_complete()

            # 次のセッションに切り替え
            self.is_work_time = not self.is_work_time
            self.time_remaining = (
                self.break_time if not self.is_work_time else self.work_time
            )
            self.update_display()

            # ビープ音を出す（簡易版）
            self.root.bell()

        self.timer_job = self.root.after(1000, self.timer_loop)

    def on_work_complete(self):
        """仕事時間完了時の処理"""
        self.sessions_completed += 1

        # ゲーミフィケーション更新
        result = self.engine.record_pomodoro_completion(1)

        # データを保存
        self.data_manager.save_gamification_data(self.engine)

        # 新しいバッジを表示
        if result["new_badges"]:
            badge_names = ", ".join([b.value for b in result["new_badges"]])
            messagebox.showinfo("新しいバッジを獲得！", f"バッジ: {badge_names}")

        # レベルアップを表示
        if result["level_up"]:
            messagebox.showinfo("レベルアップ！", f"レベル {result['new_level']} に到達しました！")

        self.update_badges_display()
        self.update_stats_display()
        self.session_label.config(text=str(self.sessions_completed))

    def on_break_complete(self):
        """休憩時間完了時の処理"""
        pass

    def update_display(self):
        """タイマー表示を更新"""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_str)

        # プログレスバー更新
        if self.is_work_time:
            max_time = self.work_time
            self.state_label.config(text="仕事時間")
        else:
            max_time = self.break_time
            self.state_label.config(text="休憩時間")

        progress = (1 - self.time_remaining / max_time) * 100
        self.progress_var.set(progress)

        # XP進捗更新
        xp_progress = self.engine.xp_system.level_progress * 100
        self.xp_progress_var.set(xp_progress)

        xp_to_next = self.engine.xp_system.xp_to_next_level
        self.xp_text_label.config(text=f"{xp_to_next} XP")

        # ストリーク更新
        streak = self.engine.streak_tracker.current_streak
        self.streak_label.config(text=f"🔥 ストリーク: {streak}日")

    def update_badges_display(self):
        """バッジ表示を更新"""
        badges = self.engine.badge_system.earned_badges
        if badges:
            badge_text = "獲得バッジ: " + ", ".join(badges)
        else:
            badge_text = "バッジを獲得して、この欄に表示されます"
        self.badge_label.config(text=badge_text)

    def update_stats_display(self):
        """統計表示を更新"""
        stats = self.engine.get_stats()

        stats_info = f"""総ポモドーロ数: {stats['statistics']['total_pomodoros']}
今週: {stats['statistics']['weekly_stats']['total_pomodoros']} ポモドーロ ({stats['statistics']['weekly_stats']['days_active']} 日間)
今月: {stats['statistics']['monthly_stats']['total_pomodoros']} ポモドーロ ({stats['statistics']['monthly_stats']['days_active']} 日間)
現在のレベル: {stats['xp']['current_level']}
現在のXP: {stats['xp']['total_xp']}
ストリーク: {stats['streak']['current_streak']} 日 (最高: {stats['streak']['max_streak']} 日)
バッジ: {stats['badges']['count']} 個"""

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats_info)
        self.stats_text.config(state=tk.DISABLED)


def main():
    """メイン関数"""
    root = tk.Tk()

    # 開発モード: コマンドライン引数を確認
    import sys

    dev_mode = "--dev" in sys.argv
    app = PomodoroTimerApp(root, dev_mode=dev_mode)

    root.mainloop()


if __name__ == "__main__":
    main()
