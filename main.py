import socket
import threading
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock


class ServerLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(ServerLayout, self).__init__(**kwargs)

        # Статусная строка с увеличенным шрифтом
        self.status_label = Label(
            text="Сервер остановлен",
            font_size=36,
            halign='center',
            valign='middle',
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # Большая кнопка по центру
        self.toggle_btn = Button(
            text="Запустить\nсервер",
            font_size=32,
            size_hint=(None, None),
            size=(340, 340),  # Сделали крупной и квадратной
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            background_color=(0.1, 0.7, 0.3, 1)
        )
        self.toggle_btn.bind(on_press=self.toggle_server)
        self.add_widget(self.toggle_btn)

        self.server_running = False
        self.tcp_sock = None
        self.udp_sock = None

    def toggle_server(self, instance):
        if not self.server_running:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        self.server_running = True
        self.toggle_btn.text = "Остановить\nсервер"
        self.toggle_btn.background_color = (0.8, 0.2, 0.2, 1)
        self.status_label.text = "Сервер запущен\nОжидание клиента..."

        threading.Thread(target=self.run_tcp_server, daemon=True).start()
        threading.Thread(target=self.run_udp_broadcast, daemon=True).start()

    def stop_server(self):
        self.server_running = False
        self.toggle_btn.text = "Запустить\nсервер"
        self.toggle_btn.background_color = (0.1, 0.7, 0.3, 1)
        self.status_label.text = "Сервер остановлен"

        try:
            if self.tcp_sock:
                self.tcp_sock.close()
            if self.udp_sock:
                self.udp_sock.close()
        except:
            pass

    def run_udp_broadcast(self):
        try:
            self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.udp_sock.bind(('', 45001))
            while self.server_running:
                data, addr = self.udp_sock.recvfrom(1024)
                if data == b"DISCOVER_ACCELERATOR_SERVER":
                    self.udp_sock.sendto(b"ACCELERATOR_SERVER_HERE", addr)
        except Exception as e:
            print(f"UDP Error: {e}")

    def run_tcp_server(self):
        try:
            self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.tcp_sock.bind(('', 45000))
            self.tcp_sock.listen(5)
            while self.server_running:
                conn, addr = self.tcp_sock.accept()
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Клиент подключен:\n{addr[0]}"))
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
        except Exception as e:
            print(f"TCP Error: {e}")

    def handle_client(self, conn):
        try:
            while self.server_running:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(b"OK")
        except:
            pass
        finally:
            conn.close()
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "Сервер запущен\nОжидание клиента..."))


class AcceleratorServerApp(App):
    def build(self):
        return ServerLayout()


if __name__ == '__main__':
    AcceleratorServerApp().run()
