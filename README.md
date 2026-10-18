# create_jupyter_report

Jupyter Notebookを利用して、SQLiteデータベースから設備別の生産実績を集計し、
表とグラフを含むHTMLレポートを作成するサンプルプロジェクトです。

Notebookを直接開いて対話的に分析する使い方と、Python + Papermillで
外部から期間を渡してレポートを自動生成する使い方の両方に対応しています。

## 主な機能

- SQLiteデータベースから設備別の生産数を集計
- pandasによる集計結果の表表示
- Matplotlibによる生産数グラフの表示
- PapermillによるNotebookへの外部パラメータ渡し
- 指定期間でNotebookを自動実行
- nbconvertによるコード非表示のHTMLレポート生成
- HTMLファイルをデスクトップへ保存
- レポート生成後に一時Notebookを自動削除
- 仮想環境から実行するための`run.bat`を付属

## ファイル構成

```text
create_jupyter_report/
├─ create_report.py
├─ jupyter_report_body_inspection.ipynb
├─ body_inspection_machine.db
├─ requirements.txt
├─ run.bat
├─ .gitignore
└─ README.md
```

### `jupyter_report_body_inspection.ipynb`

レポート本体です。

SQLiteデータベースを読み込み、指定期間の設備別生産数を集計して、
表と横棒グラフを表示します。

Notebook単体でも実行できるよう、開始日と終了日にはデフォルト値を設定しています。

### `create_report.py`

レポート自動生成用のPythonプログラムです。

ユーザーから開始日・終了日を受け取り、Papermillを使ってNotebookへ
パラメータを渡して実行します。その後、実行済みNotebookをHTMLへ変換します。

生成されるHTMLファイル名は次の形式です。

```text
body_inspection_YYYYMMDD_YYYYMMDD.html
```

例：

```text
body_inspection_20260901_20260930.html
```

HTMLはユーザーのデスクトップへ保存されます。

### `body_inspection_machine.db`

動作確認用のSQLiteデータベースです。

通常、実運用のデータベースはGit管理から除外する場合がありますが、
このプロジェクトではサンプルをすぐに実行できるよう、意図的にリポジトリへ含めています。

### `run.bat`

Windows用の起動バッチファイルです。

プロジェクト内の`.venv`を有効化してから`create_report.py`を実行します。

## 環境構築

### 1. 仮想環境を作成

プロジェクトフォルダで次を実行します。

```bat
python -m venv .venv
```

### 2. 仮想環境を有効化

```bat
.venv\Scripts\activate
```

### 3. 必要なライブラリをインストール

```bat
python -m pip install -r requirements.txt
```

## Notebookを直接実行する

VS Codeなどで次のNotebookを開きます。

```text
jupyter_report_body_inspection.ipynb
```

Notebookのカーネルには、プロジェクト内の`.venv`を選択してください。

Notebook内のパラメータセルで期間を変更できます。

```python
START_DATE = "2026-09-01"
END_DATE = "2026-09-30"
```

その後、Notebookを実行すると集計表とグラフを確認できます。

## HTMLレポートを作成する

Windowsでは`run.bat`を実行します。

開始日と終了日を入力します。

```text
開始日 [YYYY-MM-DD]: 2026-09-01
終了日 [YYYY-MM-DD]: 2026-09-30
```

Papermillが指定期間をNotebookへ渡して実行し、HTMLレポートを作成します。

生成されたHTMLはデスクトップへ保存されます。

## Papermillによるパラメータ渡し

Notebookのパラメータセルには、VS Codeの
`Mark Cell as Parameters`を設定しています。

`create_report.py`から次の値を渡します。

```python
parameters={
    "START_DATE": start_date,
    "END_DATE": end_date,
}
```

これにより、Notebookを直接編集しなくても対象期間を変更して実行できます。

Notebookを直接実行するときはNotebook内のデフォルト値を使用し、
自動レポート生成時はPapermillから渡された値を使用します。

## `.gitignore`

次のようなローカル環境・一時ファイルはGit管理から除外します。

```text
.venv/
__pycache__/
.ipynb_checkpoints/
output_report.ipynb
.vscode/
```

`body_inspection_machine.db`は動作確認用データとして使用するため、
Git管理対象にしています。

## 使用ライブラリ

主なライブラリは次のとおりです。

- Jupyter
- IPython kernel
- pandas
- Matplotlib
- Papermill
- nbconvert

詳細は`requirements.txt`を参照してください。

## 動作の流れ

```text
run.bat
   ↓
.venvを有効化
   ↓
create_report.py
   ↓
開始日・終了日を入力
   ↓
Papermill
   ↓
Jupyter Notebookを実行
   ↓
output_report.ipynb（一時ファイル）
   ↓
nbconvert
   ↓
HTMLレポートをデスクトップへ保存
   ↓
output_report.ipynbを削除
```

## 補足

このプロジェクトは、Jupyter Notebookを単なる分析用ノートとしてだけでなく、
「対話的な分析」と「定型レポートの自動生成」の両方に利用するための
シンプルなサンプルとして作成しています。
