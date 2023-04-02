# 概要
このプログラムは、Python(Tkinter)を使用してGUIを作成し、SpeechRecognitionとOpenAI whisper APIを使用した音声入力アプリケーションです。  
![image](https://user-images.githubusercontent.com/72239675/229275806-7be7de7f-f0fa-43a7-a463-06ae254cbc16.png)

# 機能
- マイクの選択
- 音声入力の開始/停止
- OpenAI whisper APIを使用した音声認識
- 認識されたテキストの表示
- 認識されたテキストのクリップボードへのコピーとカーソル自動ペースト
- APIキーの保存と変更
# 実行方法
まずは[API KEY](https://auto-worker.com/blog/?p=6988)を取得してください。
## 例１
[Releases](https://github.com/akitomonam/whisper-api-GUI/releases)からファイルをダウンロードして設定ファイルを記述して、.exeファイルを実行する。(windowsのみ対応)  
この場合、環境構築の必要はありません。
## 例２
1. 必要なPythonライブラリをインストールする。
2. config.jsonファイルにOpenAI APIキーを保存する。
3. main.pyを実行する。
# 依存ライブラリ
- tkinter
- speech_recognition
- openai
- wave
- pyautogui
- pyperclip
# 動作環境
- Python 3
- windows
# 注意事項
- このプログラムは、音声認識にOpenAI APIを使用しています。OpenAI APIを使用するには、APIキーが必要です。
- このプログラムを実行する前に、config.jsonファイルにOpenAI APIキーを保存してください。
