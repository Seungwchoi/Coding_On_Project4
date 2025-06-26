import socket
import threading
import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("채팅 클라이언트")
        self.master.configure(bg='#f3e1ff')

        # 채팅 박스 영역
        self.canvas = Canvas(master, bg='#f3e1ff', width=500, height=400)
        self.scrollbar = Scrollbar(master, command=self.canvas.yview)
        self.chat_frame = Frame(self.canvas, bg='#f3e1ff')
        self.chat_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.chat_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 메시지 입력
        self.msg_entry = tk.Entry(master, width=40, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.msg_entry.bind("<Return>", self.send_message)

        # 전송 버튼
        self.send_button = tk.Button(master, text="📨 보내기", command=self.send_message, font=("Arial", 12), bg="#f4e1ff")
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        self.nickname = "나"  # 고정 닉네임

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(("127.0.0.1", 15410))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.add_message(f"[오류] 서버 연결 실패: {e}", is_self=False)

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            try:
                self.socket.send(f"{self.nickname}: {msg}".encode('utf-8'))
                self.add_message(f"{msg}", is_self=True)
            except Exception as e:
                self.add_message(f"[오류] 메시지 전송 실패: {e}", is_self=False)
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                msg = data.decode('utf-8')
                # "나" 제외하고는 상대방으로 처리
                if not msg.startswith(f"{self.nickname}:"):
                    self.add_message(msg, is_self=False)
            except:
                break
        self.add_message("서버 연결 종료됨.", is_self=False)

    def add_message(self, message, is_self=False):
        wrapper = Frame(self.chat_frame, bg='#f3e1ff')
        wrapper.pack(anchor='e' if is_self else 'w', padx=10, pady=5, fill='x')

        name = tk.Label(wrapper, text="나" if is_self else "상대방", bg='#f3e1ff', fg='#888', font=("Arial", 9, "bold"))
        name.pack(anchor='e' if is_self else 'w')

        bubble = tk.Label(
            wrapper,
            text=message,
            bg='#f9f1fe' if is_self else '#e6e6e6',
            fg='#000',
            font=("Arial", 11),
            padx=10,
            pady=5,
            wraplength=300,
            justify='left',
            relief='solid',
            bd=1
        )
        bubble.pack(anchor='e' if is_self else 'w', padx=5)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()
