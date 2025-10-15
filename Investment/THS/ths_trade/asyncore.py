
# 模拟asyncore模块，为Python 3.13+提供兼容支持

class dispatcher:
    def __init__(self, sock=None, map=None):
        self.socket = sock
        self.map = map or {}
        if sock:
            self.add_channel(self.map)
    
    def add_channel(self, map=None):
        if map is None:
            map = self.map
        if self.socket:
            map[self.socket.fileno()] = self
    
    def del_channel(self, map=None):
        if map is None:
            map = self.map
        if self.socket and self.socket.fileno() in map:
            del map[self.socket.fileno()]
    
    def readable(self):
        return True
    
    def writable(self):
        return False
    
    def handle_read(self):
        pass
    
    def handle_write(self):
        pass
    
    def handle_connect(self):
        pass
    
    def handle_close(self):
        self.close()
    
    def handle_error(self):
        import traceback
        traceback.print_exc()
    
    def close(self):
        if self.socket:
            self.del_channel()
            self.socket.close()
            self.socket = None

class dispatcher_with_send(dispatcher):
    def __init__(self, sock=None, map=None):
        super().__init__(sock, map)
        self.out_buffer = b''
    
    def writable(self):
        return bool(self.out_buffer)
    
    def handle_write(self):
        if self.out_buffer:
            try:
                sent = self.socket.send(self.out_buffer)
                self.out_buffer = self.out_buffer[sent:]
            except Exception:
                self.handle_error()
    
    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.out_buffer = self.out_buffer + data

# 基本的循环函数
def loop(timeout=30.0, use_poll=False, map=None, count=None):
    import time
    if map is None:
        import socket
        map = {}
    
    iterations = 0
    while map and (count is None or iterations < count):
        iterations += 1
        time.sleep(timeout)

# 导出函数
_loop = loop
