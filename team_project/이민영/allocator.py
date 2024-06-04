class Node:
    # 노드 클래스 초기화 : 메모리 블록을 나타낸다.
    def __init__(self, id, start, size, free=True):
        self.id = id # 블록 식별자
        self.start = start # 블록 시작 주소
        self.size = size # 블록 크기
        self.free = free # 사용 가능 여부
        self.next = None # 다음 노드에 대한 링크

class Allocator:
    # 할당기 클래스 초기화
    def __init__(self): # 메모리 리스트의 시작 노드
        self.head = None # 전체 할당된 메모리의 양
        self.total_memory = 0 # 사용중인 메모리 양
        self.used_memory = 0 # 사용 중인 메모리 양
        self.allocations = {}  # 할당된 메모리 블록을 ID로 관리

    # 메모리 사용 통계 출력
    def print_stats(self):
        print("Arena:", self.total_memory, "bytes")
        print("In-use:", self.used_memory, "bytes")
        utilization = (self.used_memory / self.total_memory) * 100 if self.total_memory > 0 else 0
        print("Utilization: {:.2f}%".format(utilization))

    # 메모리 할당 함수
    def malloc(self, id, size):
        print(f"Allocating {size} bytes for ID {id}...")
        current = self.head
        prev = None
        while current:
            if current.free and current.size >= size:
                if current.size == size:
                    current.free = False
                    self.used_memory += size
                    self.allocations[id] = current.start
                    print(f"Allocated at {current.start} (exact fit).")
                    return current.start
                else:
                    new_node = Node(id, current.start, size, False)
                    new_node.next = current
                    if prev:
                        prev.next = new_node
                    else:
                        self.head = new_node
                    current.start += size
                    current.size -= size
                    self.used_memory += size
                    self.allocations[id] = new_node.start
                    print(f"Allocated at {new_node.start} (split block).")
                    return new_node.start
            prev = current
            current = current.next
            
        # 적합한 블록이 없을 경우 새로운 블록을 할당
        new_start = self.total_memory
        new_node = Node(id, new_start, size, False)
        if prev:
            prev.next = new_node
        else:
            self.head = new_node
        self.total_memory += size
        self.used_memory += size
        self.allocations[id] = new_start
        print(f"Allocated at new start {new_start}.")
        return new_start

    # 메모리 해제 함수
    def free(self, id):
        print(f"Freeing memory for ID {id}...")
        if id in self.allocations:
            addr = self.allocations[id]
            current = self.head
            while current:
                if current.start == addr and not current.free:
                    current.free = True
                    self.used_memory -= current.size
                    del self.allocations[id]
                    print(f"Freed memory at address {addr}.")
                    return
                current = current.next
        print("Error: Address not found or already free for ID", id)

# 메인 실행 부분
if __name__ == "__main__":
    allocator = Allocator()
    file_path = "/Users/imin-yeong/Documents/2024/자료구조/팀플/input.txt"

    # 입력 파일 처리
    with open(file_path, "r") as file:
        for line in file:
            req = line.split()
            if req[0] == 'a': # 할당 요청 처리
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f': # 해제 요청 처리
                allocator.free(int(req[1]))
    
    # 최종 메모리 상태 출력
    allocator.print_stats()
    
    