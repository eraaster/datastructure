import time
from node import Node
from redBlackTree import RedBlackTree

class Allocator:
    def __init__(self):
        """
        Allocator 클래스 초기화:
        - chunk_size: 16KB로 설정
        - free_tree: 자유 공간을 관리하는 Red-Black Tree
        - allocated_blocks: 할당된 블록을 저장하는 딕셔너리
        - total_memory: 총 할당된 메모리 크기
        - used_memory: 사용 중인 메모리 크기
        - merge_interval: 병합 주기 (초기값 100)
        - request_count: 요청 수
        """
        self.chunk_size = 16 * 1024  # 16KB
        self.free_tree = RedBlackTree()
        self.allocated_blocks = {}
        self.total_memory = 0
        self.used_memory = 0
        self.merge_interval = 100  # 초기 병합 주기
        self.request_count = 0

    def _allocate_new_chunk(self):
        """
        새로운 메모리 청크를 할당하여 free_tree에 삽입
        """
        self.free_tree.insert(self.total_memory, self.chunk_size)
        self.total_memory += self.chunk_size

    def _check_and_merge(self):
        """
        주기적으로 병합을 수행
        - merge_interval에 도달하면 병합 수행
        - 병합 후 merge_interval 줄임
        """
        self.request_count += 1
        if self.request_count >= self.merge_interval:
            self.merge()
            self.request_count = 0
            self.merge_interval = max(10, self.merge_interval // 2)  # 병합 주기 줄이기

    def malloc(self, id, size):
        """
        메모리 할당 요청 처리
        - 요청한 크기 이상의 블록을 free_tree에서 검색
        - 적합한 블록이 없으면 새로운 청크 할당
        - 적합한 블록이 있으면 블록 할당 및 분할 후 나머지 삽입
        """
        while True:
            block = self.free_tree.search(size)
            if block and block != self.free_tree.NIL_LEAF:
                self.free_tree.delete(block.start)
                if block.size > size:
                    self.free_tree.insert(block.start + size, block.size - size)
                self.allocated_blocks[id] = (block.start, size)
                self.used_memory += size
                break
            else:
                self._allocate_new_chunk()
            self._check_and_merge()

    def free(self, id):
        """
        메모리 해제 요청 처리
        - 요청된 블록을 allocated_blocks에서 제거
        - free_tree에 해제된 블록 삽입
        - 해제 후 병합 조건 검사
        """
        if id in self.allocated_blocks:
            start, size = self.allocated_blocks.pop(id)
            self.free_tree.insert(start, size)
            self.used_memory -= size
            self._check_and_merge()
        else:
            print(f"Block with ID {id} not found")

    def merge(self):
        """
        인접한 자유 블록들을 병합
        - 중위 순회를 통해 자유 블록을 가져옴
        - 인접한 블록 병합
        - 병합 후 새로운 Red-Black Tree에 삽입
        """
        nodes = self.free_tree.inorder()
        if not nodes:
            return
        merged_nodes = [nodes[0]]
        for i in range(1, len(nodes)):
            if merged_nodes[-1].start + merged_nodes[-1].size == nodes[i].start:
                merged_nodes[-1].size += nodes[i].size
            else:
                merged_nodes.append(nodes[i])
        self.free_tree = RedBlackTree()
        for node in merged_nodes:
            self.free_tree.insert(node.start, node.size)

    def print_stats(self):
        """
        메모리 사용 통계 출력
        """
        total_arena = self.total_memory / (1024 * 1024)
        in_use = self.used_memory / (1024 * 1024)
        utilization = self.used_memory / self.total_memory if self.total_memory > 0 else 0
        print(f"Arena: {total_arena:.2f} MB")
        print(f"In-use: {in_use:.2f} MB")
        print(f"Utilization: {utilization:.2%}")

if __name__ == "__main__":
    import time
    allocator = Allocator()
    
    start_time = time.time()
    with open("./input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            if n % 100 == 0:
                print(n, "...")
            
            n += 1
    
    end_time = time.time()
    allocator.print_stats()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
