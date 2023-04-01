# 概要
このプログラムは、Tkinterを使用してGUIを作成し、SpeechRecognitionとOpenAIを使用して音声認識を行う音声入力アプリケーションです。

# 機能
- マイクの選択
- 音声入力の開始/停止
- OpenAIを使用した音声認識
- 認識されたテキストの表示
- 認識されたテキストのクリップボードへのコピー
- APIキーの保存と変更
# 実行方法
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
- threading
- json
# 動作環境
- Python 3
# 注意事項
- このプログラムは、音声認識にOpenAI APIを使用しています。OpenAI APIを使用するには、APIキーが必要です。
- このプログラムを実行する前に、config.jsonファイルにOpenAI APIキーを保存してください。
- このプログラムを実行する前に、必要なPythonライブラリをインストールしてください。
