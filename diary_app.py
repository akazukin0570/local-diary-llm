import sys, os, json, subprocess
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QDateEdit, QComboBox,
    QLineEdit, QCheckBox, QDialog, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QTextDocument
from PyQt6.QtPrintSupport import QPrinter

# -------------------------------
# ディレクトリ設定
# -------------------------------
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "LocalDiaryLLM")
BACKUP_DIR = os.path.join(SAVE_DIR, "backup")
CHAT_BACKUP_DIR = os.path.join(SAVE_DIR, "chat_backup")
PROMPT_DIR = os.path.join(SAVE_DIR, "prompt")
CONFIG_FILE = os.path.join(SAVE_DIR, "config.json")
PROMPT_FILE = os.path.join(PROMPT_DIR, "prompt.txt")

for d in [SAVE_DIR, BACKUP_DIR, CHAT_BACKUP_DIR, PROMPT_DIR]:
    os.makedirs(d, exist_ok=True)

# -------------------------------
# 設定管理
# -------------------------------
def load_config(key, default=None):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)
        return data.get(key, default)
    return default

def save_config(key, value):
    data={}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)
    data[key]=value
    with open(CONFIG_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

# -------------------------------
# LLM管理
# -------------------------------
llm_model = load_config("llm_model", "llama3:8b")
LLM_COMMAND = load_config("llm_command", "ollama")

def query_llm(prompt: str) -> str:
    try:
        prompt = "必ずユーザーの入力言語で回答してください。\n\n" + prompt

        result = subprocess.run(
            [LLM_COMMAND, "run", llm_model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        response = result.stdout

        if not response:
            return "LLMから応答がありません"

        return response.strip()

    except FileNotFoundError:
        return "Ollamaが見つかりません。PATHに追加されているか確認してください。"

    except Exception as e:
        return f"LLMエラー: {e}"

# -------------------------------
# プロンプト管理
# -------------------------------
def load_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE,"r",encoding="utf-8") as f:
            return f.read()
    # 初回はデフォルト
    return "日記用プロンプト\nあなたは思考整理をサポートするAIアシスタントです。\n私は今日の出来事や感情を自由に書きます。\nあなたは次のことを行ってください：\n1. 内容を整理し、要点を簡潔にまとめる\n2. 必要に応じて、深掘りできる質問を1〜3個提示する\n3. 改善案や別の視点があれば、穏やかに提案する\n注意：\n- 外部ネットワークへ送信しない前提で動作する\n- 批判せず、理解と整理を最優先にする\n- 個人的な内容は機密として扱う\n- 回答はユーザーが入力した言語で行う"
def save_prompt(content):
    with open(PROMPT_FILE,"w",encoding="utf-8") as f:
        f.write(content)

# -------------------------------
# テーマカラー
# -------------------------------
THEMES = {
    "default": {
        "window_bg": "#F0F0F0",
        "text_bg": "#FFFFFF",
        "text_color": "#000000",
        "button_bg": "#D3D3D3",
        "button_text": "#000000"
    },
    "win98": {
        "window_bg": "#C0C0C0",
        "text_bg": "#FFFFFF",
        "text_color": "#000000",
        "button_bg": "#C0C0C0",
        "button_text": "#000000"
    }
}

# -------------------------------
# メインアプリ
# -------------------------------
class DiaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Diary LLM ver0.0.1")
        self.resize(900,600)
        self.layout=QVBoxLayout()
        self.setLayout(self.layout)

        # フォント
        self.font_size = load_config("font_size",14)
        self.main_font = QFont("Consolas",self.font_size)

        # 日付
        date_layout=QHBoxLayout()
        date_layout.addWidget(QLabel("日付:"))
        self.date_edit=QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFont(self.main_font)
        date_layout.addWidget(self.date_edit)
        self.layout.addLayout(date_layout)

        # 日記テキスト
        self.text_edit = QTextEdit()
        self.text_edit.setFont(self.main_font)
        self.layout.addWidget(self.text_edit)

        # 上段ボタン
        top_layout=QHBoxLayout()
        self.save_btn = QPushButton("保存")
        self.load_btn = QPushButton("読み込み")
        self.template_btn = QPushButton("テンプレート")
        self.summary_btn = QPushButton("今日まとめ生成")
        self.html_btn = QPushButton("HTML/PDF出力")
        for btn in [self.save_btn,self.load_btn,self.template_btn,self.summary_btn,self.html_btn]:
            btn.setFont(self.main_font)
            top_layout.addWidget(btn)
        self.layout.addLayout(top_layout)

        # 下段ボタン
        bottom_layout=QHBoxLayout()
        self.llm_btn = QPushButton("LLM相談")
        self.ai_chat_btn = QPushButton("AI会話")
        self.settings_btn = QPushButton("設定")
        for btn in [self.llm_btn,self.ai_chat_btn,self.settings_btn]:
            btn.setFont(self.main_font)
            bottom_layout.addWidget(btn)
        self.layout.addLayout(bottom_layout)

        # ボタン接続
        self.save_btn.clicked.connect(self.save_diary)
        self.load_btn.clicked.connect(self.load_diary)
        self.template_btn.clicked.connect(self.insert_template)
        self.summary_btn.clicked.connect(self.generate_summary)
        self.html_btn.clicked.connect(self.export_html_pdf)
        self.llm_btn.clicked.connect(self.llm_consult)
        self.ai_chat_btn.clicked.connect(self.ai_chat)
        self.settings_btn.clicked.connect(self.show_settings)

        # テーマ
        self.current_theme = load_config("theme","default")
        self.apply_theme(self.current_theme)

    # ---------------------------
    # テーマ適用
    # ---------------------------
    def apply_theme(self, theme_name):
        theme = THEMES.get(theme_name, THEMES["default"])
        self.setStyleSheet(f"background-color:{theme['window_bg']};")
        self.text_edit.setStyleSheet(f"background-color:{theme['text_bg']}; color:{theme['text_color']};")
        for btn in [self.save_btn,self.load_btn,self.template_btn,self.summary_btn,self.html_btn,
                    self.llm_btn,self.ai_chat_btn,self.settings_btn]:
            btn.setStyleSheet(f"background-color:{theme['button_bg']}; color:{theme['button_text']};")

    # ---------------------------
    # 日記操作
    # ---------------------------
    def get_filename(self):
        date_str=self.date_edit.date().toString("yyyy-MM-dd")
        return os.path.join(SAVE_DIR,f"{date_str}.txt")

    def save_diary(self):
        filename=self.get_filename()
        if os.path.exists(filename):
            backup_file=os.path.join(BACKUP_DIR,os.path.basename(filename))
            with open(filename,"r",encoding="utf-8") as f: data=f.read()
            with open(backup_file,"w",encoding="utf-8") as f: f.write(data)
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename,"w",encoding="utf-8") as f:
            f.write(f"[{now}]\n")
            f.write(self.text_edit.toPlainText())
        QMessageBox.information(self,"保存","日記を保存しました")

    def load_diary(self):
        filename=self.get_filename()
        if os.path.exists(filename):
            with open(filename,"r",encoding="utf-8") as f: self.text_edit.setPlainText(f.read())
        else:
            self.text_edit.clear()

    def insert_template(self):
        template="今日の気分:\n出来事:\n反省:\n明日の目標:\n"
        self.text_edit.insertPlainText(template)

    # ---------------------------
    # LLM生成
    # ---------------------------
    def generate_summary(self):
        prompt=f"以下の日記をまとめてください:\n{self.text_edit.toPlainText()}"
        summary=query_llm(prompt)
        self.text_edit.append("\n--- まとめ ---\n"+summary)

    # ---------------------------
    # HTML/PDF出力
    # ---------------------------
    def export_html_pdf(self):
        filename=self.get_filename().replace(".txt",".html")
        try:
            with open(filename,"w",encoding="utf-8") as f:
                f.write("<html><body><pre>")
                f.write(self.text_edit.toPlainText())
                f.write("</pre></body></html>")

            pdf_file=filename.replace(".html",".pdf")
            doc=QTextDocument()
            doc.setPlainText(self.text_edit.toPlainText())
            printer=QPrinter()
            printer.setOutputFileName(pdf_file)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            doc.print(printer)

            QMessageBox.information(self,"出力",f"{filename} と {pdf_file} に出力しました")
        except Exception as e:
            QMessageBox.warning(self,"出力エラー",str(e))

    # ---------------------------
    # LLM相談
    # ---------------------------
    def llm_consult(self):
        prompt=f"{load_prompt()}\n日記内容:\n{self.text_edit.toPlainText()}"
        response=query_llm(prompt)
        self.text_edit.append("\n--- LLM相談 ---\n"+response)

    # ---------------------------
    # AI会話
    # ---------------------------
    def ai_chat(self):
        dlg=QDialog(self)
        dlg.setWindowTitle("AIと会話")
        dlg.resize(900,600)
        layout=QVBoxLayout()
        dlg.setLayout(layout)
        font=QFont("Consolas",self.font_size)
        theme = THEMES.get(self.current_theme, THEMES["default"])
        dlg.setStyleSheet(f"background-color:{theme['window_bg']};")

        # プロンプト編集
        prompt_label=QLabel("日記用プロンプト")
        prompt_label.setFont(font)
        prompt_label.setStyleSheet("color:black;")
        prompt_edit=QTextEdit()
        prompt_edit.setFont(font)
        prompt_edit.setStyleSheet("background-color:#FFFACD;color:black;border:1px solid gray;")
        prompt_edit.setPlainText(load_prompt())
        prompt_label.setVisible(False)
        prompt_edit.setVisible(False)
        toggle_btn=QPushButton("プロンプト編集")
        toggle_btn.setFont(font)
        toggle_btn.clicked.connect(lambda:(prompt_label.setVisible(not prompt_label.isVisible()),
                                          prompt_edit.setVisible(not prompt_edit.isVisible())))
        layout.addWidget(toggle_btn)
        layout.addWidget(prompt_label)
        layout.addWidget(prompt_edit)

        # 会話履歴
        chat_history=QTextEdit()
        chat_history.setFont(font)
        chat_history.setReadOnly(True)
        chat_history.setStyleSheet(f"background-color:{theme['text_bg']}; color:{theme['text_color']}; border:1px solid gray;")
        layout.addWidget(chat_history)

        # 入力欄
        input_edit=QLineEdit()
        input_edit.setFont(font)
        input_edit.setStyleSheet("background-color:white;color:black;border:1px solid gray;")
        input_edit.setPlaceholderText("文字を入力する")
        layout.addWidget(input_edit)

        # 送信ボタン
        send_btn=QPushButton("送信")
        send_btn.setFont(font)
        send_btn.setStyleSheet("background-color:#D3D3D3;border:1px solid gray;font-weight:bold;")
        layout.addWidget(send_btn)

        def update_btn_color(text):
            if text.strip():
                send_btn.setStyleSheet("background-color:#ADD8E6;border:1px solid gray;font-weight:bold;")
            else:
                send_btn.setStyleSheet("background-color:#D3D3D3;border:1px solid gray;font-weight:bold;")
        input_edit.textChanged.connect(update_btn_color)

        def send_message():
            user_text=input_edit.text()
            if not user_text.strip(): return
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chat_history.append(f"[{timestamp}] <span style='color:blue'>ユーザー</span>: {user_text}")
            full_prompt=prompt_edit.toPlainText()+"\n日記内容:\n"+self.text_edit.toPlainText()+"\n質問:\n"+user_text
            ai_response=query_llm(full_prompt)
            chat_history.append(f"[{timestamp}] <span style='color:green'>AI</span>: {ai_response}")
            chat_history.verticalScrollBar().setValue(chat_history.verticalScrollBar().maximum())
            # バックアップ
            backup_file=os.path.join(CHAT_BACKUP_DIR,f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt")
            with open(backup_file,"a",encoding="utf-8") as f:
                f.write(f"[{timestamp}] ユーザー: {user_text}\n")
                f.write(f"[{timestamp}] AI: {ai_response}\n")
            # プロンプト保存
            if prompt_edit.isVisible():
                save_prompt(prompt_edit.toPlainText())
            input_edit.clear()

        send_btn.clicked.connect(send_message)
        input_edit.returnPressed.connect(send_message)
        dlg.exec()

    # ---------------------------
    # 設定画面
    # ---------------------------
    def show_settings(self):
        dlg=QDialog(self)
        dlg.setWindowTitle("設定")
        layout=QVBoxLayout()
        dlg.setLayout(layout)

        # モデル選択
        layout.addWidget(QLabel("使用するモデル:"))
        model_combo=QComboBox()
        model_combo.addItems(["Mistral 7B","llama3:8b"])
        model_combo.setCurrentText(load_config("llm_model","llama3:8b"))
        layout.addWidget(model_combo)

        # 文字サイズ設定
        layout.addWidget(QLabel("文字サイズ:"))
        font_size_combo=QComboBox()
        font_size_combo.addItems([str(s) for s in range(10,25)])
        font_size_combo.setCurrentText(str(self.font_size))
        layout.addWidget(font_size_combo)

        # テーマ選択
        layout.addWidget(QLabel("テーマ:"))
        theme_combo=QComboBox()
        theme_combo.addItems(list(THEMES.keys()))
        theme_combo.setCurrentText(load_config("theme","default"))
        layout.addWidget(theme_combo)

        # OK/Cancel
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        def on_ok():
            save_config("llm_model",model_combo.currentText())
            new_size=int(font_size_combo.currentText())
            save_config("font_size",new_size)
            self.font_size=new_size
            self.main_font.setPointSize(new_size)
            # UI反映
            self.text_edit.setFont(self.main_font)
            self.date_edit.setFont(self.main_font)
            for btn in [self.save_btn,self.load_btn,self.template_btn,self.summary_btn,self.html_btn,
                        self.llm_btn,self.ai_chat_btn,self.settings_btn]:
                btn.setFont(self.main_font)
            # テーマ
            save_config("theme",theme_combo.currentText())
            self.current_theme = theme_combo.currentText()
            self.apply_theme(self.current_theme)
            QMessageBox.information(dlg,"反映完了","設定を反映しました")
            dlg.accept()

        buttons.accepted.connect(on_ok)
        buttons.rejected.connect(dlg.reject)
        dlg.exec()

# -------------------------------
# アプリ起動
# -------------------------------
app=QApplication(sys.argv)
win=DiaryApp()
win.show()
sys.exit(app.exec())