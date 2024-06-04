import time
class Allocator:
    def __init__(self):
        self.chunk_size = 4096  # 4KB
        self.arena = []
        self.allocations = {}  # 각 ID에 할당된 청크를 추적하는 딕셔너리
        self.free_chunks = {}  # 해제된 청크를 관리하는 딕셔너리 (키: 청크 인덱스, 값: True)

    def print_stats(self):
        total_chunks = len(self.arena)
        allocated_chunks = sum(len(chunks) for chunks in self.allocations.values())
        arena_size = total_chunks * self.chunk_size / (1024 * 1024)  # MB
        in_use_size = allocated_chunks * self.chunk_size / (1024 * 1024)  # MB
        utilization = in_use_size / arena_size if arena_size > 0 else 0
        print(f"Arena: {arena_size:.2f} MB")
        print(f"In-use: {in_use_size:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def hash_function(self, index):
        return index  # 간단한 해시 함수: 청크 인덱스를 그대로 반환

    def malloc(self, id, size):
        chunks_needed = (size + self.chunk_size - 1) // self.chunk_size
        allocated_chunks = []

        # 해제된 청크 중에서 할당할 청크를 찾기 위해 해시 테이블을 사용
        for chunk_index in list(self.free_chunks.keys()):
            if chunks_needed == 0:
                break
            allocated_chunks.append(chunk_index)
            del self.free_chunks[chunk_index]  # 사용한 청크를 해제 목록에서 제거
            chunks_needed -= 1

        # 추가 청크가 필요한 경우 새로운 청크를 arena에 추가
        while chunks_needed > 0:
            chunk = len(self.arena)
            self.arena.append(chunk)
            allocated_chunks.append(chunk)
            chunks_needed -= 1

        self.allocations[id] = allocated_chunks

    def free(self, id):
        if id in self.allocations:
            freed_chunks = self.allocations.pop(id)
            for chunk in freed_chunks:
                hashed_chunk = self.hash_function(chunk)
                self.free_chunks[hashed_chunk] = True  # 해제된 청크를 free_chunks 딕셔너리에 추가

if __name__ == "__main__":
    start = time.time()
    allocator = Allocator()

    with open("Memory\input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            # if n % 100 == 0:
            #     print(n, "...")
            
            n += 1
    print(f"{time.time()-start:.4f} sec")
    allocator.print_stats()
