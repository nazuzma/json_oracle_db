from io import RawIOBase
import threading
import time

KB = 1024**1
MB = 1024**2


class ChunkBytesIO(RawIOBase):
    """IO Bytes Stream that splits and writes data in fixed sized buckets."""

    def __init__(self, chunk_size=50*MB, max_chunks=4):
        self.chunk_size = chunk_size
        self.max_chunks = max_chunks
        self.chunks = [bytearray()]
        self.bytes_written = 0
        self.mutex = threading.Lock()

    def _free_all_chunks(self):
        with self.mutex:
            while self.chunks:
                del self.chunks[0]

    def close(self):
        self._free_all_chunks()

    def tell(self):
        return self.bytes_written

    def write(self, data):
        if data:
            if len(self.chunks) > self.max_chunks:
                while len(self.chunks) > self.max_chunks:
                    time.sleep(0)
            with self.mutex:
                n = len(data)
                i = 0
                while n - i > 0:
                    available = self.chunk_size - len(self.chunks[-1])
                    if available == 0:
                        self.chunks.append(bytearray())
                        available = self.chunk_size
                    q = min(available, n - i)
                    self.chunks[-1] += data[i:i+q]
                    i += q
                self.bytes_written += n

    def get_first_chunk(self, force=False):
        with self.mutex:
            return self.chunks.pop(0) if self.chunks and (force or len(self.chunks[0]) == self.chunk_size) else None
