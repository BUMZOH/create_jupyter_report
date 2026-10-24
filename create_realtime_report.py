import subprocess
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import papermill as pm


# ================================================
#   Settings
# ================================================
NOTEBOOK_PATH = "jupyter_report_body_inspection.ipynb"
OUTPUT_NOTEBOOK_PATH = "output_report.ipynb"

UPDATE_INTERVAL_SECONDS = 1 * 60
BROWSER_REFRESH_SECONDS = 60

DESKTOP_PATH = Path.home() / "Desktop"
OUTPUT_HTML_PATH = DESKTOP_PATH / "body_inspection_realtime.html"


# ================================================
#   Functions
# ================================================
def normalize_date(value):
    parts = value.split("-")

    if len(parts) == 2:
        year = datetime.now().year
        month, day = map(int, parts)
    elif len(parts) == 3:
        year, month, day = map(int, parts)

        if year < 100:
            year += 2000
    else:
        raise ValueError("日付は YYYY-M-D / YY-M-D / M-D で入力してください。")

    date = datetime(year, month, day)

    return date.strftime("%Y-%m-%d")


def create_html_report(start_date, end_date):
    print()
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] レポート更新開始")
    print(f"対象期間: {start_date} ～ {end_date}")

    try:
        print("Notebookを実行しています...")

        pm.execute_notebook(
            NOTEBOOK_PATH,
            OUTPUT_NOTEBOOK_PATH,
            parameters={
                "START_DATE": start_date,
                "END_DATE": end_date,
            },
        )

        print("HTMLを作成しています...")

        subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "html",
                "--no-input",
                "--no-prompt",
                "--output",
                str(OUTPUT_HTML_PATH),
                OUTPUT_NOTEBOOK_PATH,
            ],
            check=True,
        )

        add_auto_refresh(OUTPUT_HTML_PATH)

        print(f"HTMLを更新しました: {OUTPUT_HTML_PATH}")

    finally:
        temp_path = Path(OUTPUT_NOTEBOOK_PATH)

        if temp_path.exists():
            temp_path.unlink()
            print("一時Notebookを削除しました。")


def add_auto_refresh(html_path):
    html = html_path.read_text(encoding="utf-8")

    refresh_tag = (
        f'<meta http-equiv="refresh" '
        f'content="{BROWSER_REFRESH_SECONDS}">'
    )

    if "<head>" in html:
        html = html.replace("<head>", f"<head>\n{refresh_tag}", 1)
    else:
        raise RuntimeError("HTMLの<head>タグが見つかりません。")

    html_path.write_text(html, encoding="utf-8")


# ================================================
#   Main
# ================================================
def main():
    start_date = normalize_date(input("開始日: "))
    end_date = normalize_date(input("終了日: "))

    print()
    print("リアルタイムHTMLレポートを開始します。")
    print(f"更新間隔: {UPDATE_INTERVAL_SECONDS // 60}分")
    print(f"ブラウザ再読み込み間隔: {BROWSER_REFRESH_SECONDS}秒")
    print("終了する場合は Ctrl+C を押してください。")

    browser_opened = False

    try:
        while True:
            try:
                create_html_report(start_date, end_date)

                if not browser_opened:
                    webbrowser.open(OUTPUT_HTML_PATH.resolve().as_uri())
                    browser_opened = True

            except Exception as error:
                print()
                print(f"レポート更新に失敗しました: {error}")
                print("次回の更新時に再試行します。")

            print()
            print(
                f"次回更新まで "
                f"{UPDATE_INTERVAL_SECONDS // 60}分待機します..."
            )
            time.sleep(UPDATE_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print()
        print("リアルタイムHTMLレポートを終了しました。")


if __name__ == "__main__":
    main()
