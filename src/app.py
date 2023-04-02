import tkinter as tk
import speech_recognition as sr
import openai
import wave
import pyautogui
import pyperclip
import threading
import json
import queue

class App:
    def __init__(self, master):

        # JSONファイルからAPIキーを読み取る
        with open('./config.json', 'r') as f:
            config = json.load(f)
            openai.api_key = config['openai_api_key']
            self.api_key = config['openai_api_key']

        self.master = master
        master.title("音声入力アプリ")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)


        # マイク選択用のラベル
        self.label = tk.Label(master, text="マイクを選択してください:")
        self.label.pack()

        # ドロップダウンリストによるマイク選択
        self.mic_options = sr.Microphone.list_microphone_names()
        self.mic_var = tk.StringVar(value=self.mic_options[0])
        self.mic_dropdown = tk.OptionMenu(master, self.mic_var, *self.mic_options)
        self.mic_dropdown.pack()

        # 音声入力開始ボタン
        self.start_button = tk.Button(master, text="音声入力開始", command=self.start_recording)
        self.start_button.pack()

        # 音声入力停止ボタン
        self.stop_button = tk.Button(master, text="音声入力停止", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        # テキストボックスを追加する
        self.text_box = tk.Text(master, height=10, width=50)
        self.text_box.pack()

        self.canvas = None

        # 音声認識オブジェクトの作成
        self.r = sr.Recognizer()

        # スレッド用のフラグ
        self.continue_recording = threading.Event()

        self.thread = None
        self.transcribe_thread = None

        # APIキー入力用のラベルとテキストボックスを追加する
        self.api_key_label = tk.Label(master, text="OpenAI APIキー:")
        self.api_key_label.pack()
        self.api_key_entry = tk.Entry(master, show="*")
        self.api_key_entry.pack()
        self.api_key_entry.insert(0, self.api_key)
        # APIキー保存ボタンを追加する
        self.save_api_key_button = tk.Button(master, text="APIキーを保存する", command=self.save_api_key)
        self.save_api_key_button.pack()

        self.audio_queue = queue.Queue()

    def on_closing(self):
        # 音声入力を停止する
        self.stop_recording()
        # ウィンドウを閉じる
        self.master.destroy()

    def save_api_key(self):
        # 入力されたAPIキーをJSONファイルに保存する
        self.api_key = self.api_key_entry.get()
        openai.api_key = self.api_key_entry.get()
        config = {"openai_api_key": self.api_key}
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.continue_recording.set()
        # 音声入力スレッドを開始する
        self.thread = threading.Thread(target=self.process_audio)
        self.thread.start()
        # 音声認識スレッドを開始する
        self.transcribe_thread = threading.Thread(target=self.transcribe_audio)
        self.transcribe_thread.start()

    def stop_recording(self):
        self.continue_recording.clear()
        if self.thread is not None:
            if self.thread.is_alive():
                print("スレッド待ち(音声入力)")
                self.thread.join()
                print("音声入力停止")
        if self.transcribe_thread is not None:
            if self.transcribe_thread.is_alive():
                print("スレッド待ち(音声認識)")
                self.transcribe_thread.join()
                print("音声認識停止")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        # 赤い丸を消す
        if self.canvas is not None:
            self.canvas.destroy()

    def process_audio(self):
        # 赤い丸を表示する
        self.canvas = tk.Canvas(self.master, width=20, height=20)
        self.canvas.create_oval(0, 0, 20, 20, fill='red')
        self.canvas.pack(side='left', padx=5)
        with sr.Microphone(device_index=self.get_selected_mic_index()) as source:
            self.r.adjust_for_ambient_noise(source)
            while self.continue_recording.is_set():
                print("音声入力開始...")
                try:
                    audio = self.r.listen(source,3)
                except:
                    continue
                try:
                    with wave.open("audio.wav", "wb") as f:
                        f.setnchannels(1)
                        f.setsampwidth(2)
                        f.setframerate(36000)
                        f.writeframesraw(audio.get_raw_data())
                    # 音声ファイルをキューに追加する
                    audio_file= open("audio.wav", "rb")
                    self.audio_queue.put(audio_file)
                    print("キュー追加完了")
                except sr.UnknownValueError:
                    print("音声が認識できませんでした")
                except sr.RequestError as e:
                    print("エラー:", e)
                    error_message = "エラーが発生しました: {}".format(e)
                    self.text_box.insert(tk.END, error_message + "\n")

    def transcribe_audio(self):
        while self.continue_recording.is_set():
            try:
                # キューから音声ファイルを取り出す
                audio = self.audio_queue.get(timeout=1)
                transcript = openai.Audio.transcribe("whisper-1", audio)
                text = transcript["text"]
                print("認識結果:", text)
                # 認識結果をテキストボックスに追加する
                self.text_box.insert(tk.END, text + '\n')
                # クリップボードに認識結果をコピーする
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
            except queue.Empty:
                continue
            except openai.error.AuthenticationError as e:
                print("エラー:", e)
                error_message = "OpenAIのAPIキーが不正です。APIキーを確認してください。"
                self.text_box.insert(tk.END, error_message + "\n")
            # キューからのアイテムを処理し終わったので、キューから削除する
            self.audio_queue.task_done()
        print("音声認識停止（関数内）")


    def get_selected_mic_index(self):
        mic_name = self.mic_var.get()
        mic_names = sr.Microphone.list_microphone_names()
        return mic_names.index([x for x in mic_names if x.startswith(mic_name)][0])

root = tk.Tk()
app = App(root)
root.mainloop()
