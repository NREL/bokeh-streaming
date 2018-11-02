from threading import Thread
import receiver

def on_server_loaded(server_context):
    t = Thread(target=receiver.stream_receive, daemon=True)
    t.start()

