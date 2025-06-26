import socket
import threading
import tkinter as tk
from tkinter import ttk

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("채팅 클라이언트")
        self.master.configure(bg='#f3e1ff')

        # 채팅 프레임 (스크롤 가능)
        self.chat_frame = tk.Frame(master, bg='#f3e1ff')
        self.canvas = tk.Canvas(self.chat_frame, bg='#f3e1ff', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f3e1ff')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 메시지 입력창
        self.msg_entry = tk.Entry(master, width=40, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.msg_entry.bind("<Return>", self.send_message)

        # 보내기 버튼
        self.send_button = tk.Button(master, text="📨 보내기", command=self.send_message, font=("Arial", 12), bg="#f4e1ff")
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        # TCP 연결
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("192.168.1.223", 15410))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.add_message(f"[오류] 서버 연결 실패: {e}", sender="system")

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            try:
                self.socket.send(msg.encode('utf-8'))
                self.add_message(msg, sender="me")
            except Exception as e:
                self.add_message(f"[오류] 메시지 전송 실패: {e}", sender="system")
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                msg = data.decode('utf-8')
                self.add_message(msg, sender="other")
            except:
                break
        self.add_message("서버 연결 종료됨.", sender="system")

    def add_message(self, text, sender="other"):
        wrapper = tk.Frame(self.scrollable_frame, bg="#f3e1ff")
        wrapper.pack(fill="both", pady=3, anchor="e" if sender == "me" else "w", padx=10)

        if sender == "me":
            bg_color = "#f9f1fe"
            anchor = "e"
            name = "나"
        elif sender == "other":
            bg_color = "#f2f2f2"
            anchor = "w"
            name = "상대방"
        else:
            bg_color = "#ffecec"
            anchor = "center"
            name = "🔔"

        name_label = tk.Label(wrapper, text=name, font=("Arial", 9), bg='#f3e1ff', fg='#555')
        name_label.pack(anchor=anchor)

        msg_label = tk.Label(
            wrapper,
            text=text,
            font=("Arial", 12),
            bg=bg_color,
            wraplength=300,
            padx=10,
            pady=5,
            justify="left",
            relief="ridge",
            bd=2
        )
        msg_label.pack(anchor=anchor)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()
