# create_jupyter_report

Jupyter Notebookを利用して、SQLiteデータベースから設備データを集計し、
表とグラフを含むHTMLレポートを作成するサンプルプロジェクトです。

Notebookを直接開いて対話的に分析する使い方と、Python + Papermillで
外部から期間を渡してレポートを自動生成する使い方の両方に対応しています。

## 主な機能

- SQLiteデータベースから指定期間の設備データを集計
- 設備別の生産数（OK数）を集計
- 設備別の日別生産数をグラフ表示
- データが存在しない日付を0として補完
- 土日の生産数をグレーで表示
- 設備別のOK数・NG数・OK率・NG率を集計
- OK率とNG率を100%積み上げ横棒グラフで表示
- `*_ngcount1`カラムを自動取得し、NG発生要因を設備別に集計
- `*_alarm_count`カラムを自動取得し、全アラーム発生回数を設備別に集計
- 設備別のアラーム発生回数を横棒グラフで表示
- アラーム種類別の発生回数を設備別に集計
- Markdownによるセクション分けと水平線によるレポート整理
- レポート冒頭に集計期間を表示
- PapermillによるNotebookへの外部パラメータ渡し
- nbconvertによるコード非表示のHTMLレポート生成
- HTMLファイルをデスクトップへ保存
- レポート生成後に一時Notebookを自動削除
- `YYYY-M-D`、`YY-M-D`、`M-D`形式の日付入力に対応
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

SQLiteデータベースを読み込み、指定期間について次の内容を集計・表示します。

1. 設備別 生産数
2. 設備別 日別生産数
3. 設備別 NG発生状況
4. 設備別 アラーム発生状況

表による正確な数値の確認と、Matplotlibによるグラフでの視覚的な比較を
組み合わせています。

Notebook単体でも実行できるよう、開始日と終了日にはデフォルト値を設定しています。

### `create_report.py`

レポート自動生成用のPythonプログラムです。

ユーザーから開始日・終了日を受け取り、Papermillを使ってNotebookへ
パラメータを渡して実行します。その後、実行済みNotebookをHTMLへ変換します。

日付は次の形式で入力できます。

```text
2026-9-1
26-9-1
9-1
```

`YY-M-D`形式では西暦2000年代として扱い、
`M-D`形式では実行時の現在年を使用します。

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

Notebookを実行すると、集計期間がレポート冒頭に表示され、
各セクションの集計表とグラフを確認できます。

## レポート内容

### 1. 設備別 生産数

指定期間の`ok_count`を設備ごとに集計し、表と横棒グラフで表示します。

### 2. 設備別 日別生産数

設備ごとの日別生産数を表示します。

指定期間の全日付を作成し、データが存在しない日付は0として補完します。
また、土日の棒はグレーで表示します。

### 3. 設備別 NG発生状況

設備ごとに`ok_count`と`ngcount_total1`を集計し、
OK率・NG率を算出します。

OK率は緑、NG率は赤の100%積み上げ横棒グラフで表示します。

また、データベースのテーブル定義から`*_ngcount1`カラムを自動取得し、
NG発生要因ごとの件数を設備別に集計します。

このため、命名規則に従ってNG項目が追加された場合でも、
集計対象へ自動的に反映できます。

### 4. 設備別 アラーム発生状況

データベースのテーブル定義から`*_alarm_count`カラムを自動取得します。

取得した各アラームカラムをレコードごとに合計し、
設備別・指定期間の全アラーム発生回数を集計します。

全アラーム発生回数は表とピンク色の横棒グラフで表示します。

さらに、各`*_alarm_count`カラムを設備別に集計し、
アラーム種類ごとの内訳も表で表示します。

命名規則に従ってアラーム項目が追加された場合でも、
集計対象へ自動的に反映できます。

## HTMLレポートを作成する

Windowsでは`run.bat`を実行します。

開始日と終了日を入力します。

```text
開始日: 9-1
終了日: 9-30
```

Papermillが指定期間をNotebookへ渡して実行し、
コードを非表示にしたHTMLレポートを作成します。

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
日付形式をYYYY-MM-DDへ正規化
   ↓
Papermill
   ↓
Jupyter Notebookを実行
   ↓
output_report.ipynb（一時ファイル）
   ↓
nbconvert
   ↓
コード非表示のHTMLレポートをデスクトップへ保存
   ↓
output_report.ipynbを削除
```

## 補足

このプロジェクトは、Jupyter Notebookを単なる分析用ノートとしてだけでなく、
「対話的な分析」と「定型レポートの自動生成」の両方に利用するための
シンプルなサンプルとして作成しています。

表で正確な数値を確認し、グラフで設備間の違いや傾向を視覚的に把握できる
レポートを目指しています。
