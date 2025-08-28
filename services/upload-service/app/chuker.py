import hashlib
from typing import Generator

class ContentDefinedChunker:
    def __init__(self, avg_chunk_size: int = 8192, window_size: int = 48):
        self.avg_chunk_size = avg_chunk_size
        self.window_size = window_size
        self.prime = 1000000007
        self.base = 256
        self.mod_mask = (1 << 61) - 1

    def _calc_hash(self, data: bytes) -> int:
        h = 0
        for byte in data:
            h = (h * self.base + byte) % self.mod_mask
        return h

    def chunk_stream(self, file_stream) -> Generator[bytes, None, None]:
        from collections import deque
        window = deque(maxlen=self.window_size)
        current_chunk = bytearray()
        
        while True:
            byte = file_stream.read(1)
            if not byte:
                break

            current_chunk.append(byte[0])
            window.append(byte[0])
            
            if len(window) < self.window_size:
                continue

            win_hash = self._calc_hash(bytes(window))
            
            if win_hash % self.avg_chunk_size == (self.avg_chunk_size - 1):
                yield bytes(current_chunk)
                current_chunk = bytearray()
                window.clear()

        if current_chunk:
            yield bytes(current_chunk)

    def calculate_chunk_hash(self, chunk_data: bytes) -> str:
        return hashlib.sha256(chunk_data).hexdigest()
