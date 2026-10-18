import sys
import subprocess
from datetime import datetime
from pathlib import Path

import papermill as pm


# ================================================
#   Settings
# ================================================
NOTEBOOK_PATH = "jupyter_report_body_inspection.ipynb"
OUTPUT_NOTEBOOK_PATH = "output_report.ipynb"

DESKTOP_PATH = Path.home() / "Desktop"

# ================================================
#   Input date
# ================================================
start_date = input("開始日 [YYYY-MM-DD]: ")
end_date = input("終了日 [YYYY-MM-DD]: ")

datetime.strptime(start_date, "%Y-%m-%d")
datetime.strptime(end_date, "%Y-%m-%d")

start_date_text = start_date.replace("-", "")
end_date_text = end_date.replace("-", "")

output_html_path = (
    DESKTOP_PATH
    / f"body_inspection_{start_date_text}_{end_date_text}.html"
)

# ================================================
#   Execute notebook
# ================================================
print()
print(f"対象期間: {start_date} ～ {end_date}")
print("Notebookを実行しています...")

pm.execute_notebook(
    NOTEBOOK_PATH,
    OUTPUT_NOTEBOOK_PATH,
    parameters={
        "START_DATE": start_date,
        "END_DATE": end_date,
    },
)

print("Notebookの実行が完了しました。")


# ================================================
#   Export HTML
# ================================================
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
        output_html_path,
        OUTPUT_NOTEBOOK_PATH,
    ],
    check=True,
)

print(f"HTMLの作成が完了しました: {output_html_path}")


# ================================================
#   Delete temporary notebook
# ================================================
Path(OUTPUT_NOTEBOOK_PATH).unlink()

print("一時Notebookを削除しました。")