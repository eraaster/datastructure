import time

class ListNode:
    """
    이중 연결 리스트의 노드를 나타내는 클래스
    """
    def __init__(self, start, size):
        self.start = start  # 메모리 블록의 시작 주소
        self.size = size    # 메모리 블록의 크기
        self.prev = None    # 이전 노드에 대한 포인터
        self.next = None    # 다음 노드에 대한 포인터

class TreeNode:
    """
    AVL 트리의 노드를 나타내는 클래스
    """
    def __init__(self, start, size):
        self.start = start  # 메모리 블록의 시작 주소
        self.size = size    # 메모리 블록의 크기
        self.height = 1     # 노드의 높이
        self.left = None    # 왼쪽 자식 노드에 대한 포인터
        self.right = None   # 오른쪽 자식 노드에 대한 포인터

class Allocator:
    """
    메모리 할당자 클래스
    """
    def __init__(self):
        self.chunk_size = 4096  # 4KB의 chunk 크기
        self.arena = []          # 할당된 메모리 블록을 저장하는 리스트 [(id, size)]
        self.free_blocks_list_head = ListNode(0, 0)  # 이중 연결 리스트의 더미 헤드 노드
        self.free_blocks_tree = None  # 빈 블록을 저장하는 AVL 트리

    def print_stats(self):
        """
        메모리 할당 통계를 출력합니다.
        """
        total_memory = len(self.arena) * self.chunk_size
        in_use = sum(block[1] for block in self.arena)
        utilization = in_use / total_memory if total_memory != 0 else 0

        print("Arena: {} KB".format(total_memory // 1024))
        print("In-use: {} KB".format(in_use // 1024))
        print("Utilization: {:.2f}".format(utilization))

    def height(self, node):
        """
        노드의 높이를 반환합니다.
        """
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        """
        노드의 균형인수를 계산합니다.
        """
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        """
        우로 회전합니다.
        """
        x = y.left
        T2 = x.right

        # 회전
        x.right = y
        y.left = T2

        # 높이 업데이트
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1

        return x

    def rotate_left(self, x):
        """
        좌로 회전합니다.
        """
        y = x.right
        T2 = y.left

        # 회전
        y.left = x
        x.right = T2

        # 높이 업데이트
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1

        return y

    def insert_into_tree(self, root, start, size):
        """
        AVL 트리에 새로운 노드를 삽입합니다.
        """
        if root is None:
            return TreeNode(start, size)
        
        if start < root.start:
            root.left = self.insert_into_tree(root.left, start, size)
        else:
            root.right = self.insert_into_tree(root.right, start, size)

        # 노드의 높이 업데이트
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # 균형인수 계산
        balance = self.balance_factor(root)

        # 불균형이 발생한 경우 회전 수행
        if balance > 1:
            if start < root.left.start:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
        if balance < -1:
            if start > root.right.start:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def find_block(self, root, size):
        """
        요청 크기보다 크거나 같은 블록을 찾습니다.
        """
        if root is None:
            return None
        
        if root.size >= size:
            return root

        if root.right is not None:
            return self.find_block(root.right, size)
        return self.find_block(root.left, size)

    def malloc(self, id, size):
        """
        메모리를 할당합니다.
        """
        block = self.find_block(self.free_blocks_tree, size)

        if block is not None:
            self.arena.append((id, size))
            if block.size > size:
                self.free_blocks_tree = self.insert_into_tree(self.free_blocks_tree, block.start + size, block.size - size)
        else:
            self.arena.append((id, self.chunk_size))

    def insert_into_list(self, node, start, size):
        """
        이중 연결 리스트에 새로운 노드를 삽입합니다.
        """
        new_node = ListNode(start, size)
        new_node.next = node.next
        new_node.prev = node
        if node.next:
            node.next.prev = new_node
        node.next = new_node

    def merge_adjacent_free_blocks(self, node):
        """
        인접한 빈 블록들을 병합합니다.
        """
        # 이전 노드와 병합 (현재 노드의 시작 주소가 이전 노드의 끝 주소와 동일한지 확인)
        if node.prev and node.prev.start + node.prev.size == node.start:
            node.prev.size += node.size  # 이전 노드의 크기를 현재 노드의 크기만큼 증가
            node.prev.next = node.next  # 이전 노드의 다음 포인터를 현재 노드의 다음 포인터로 설정
            if node.next:
                node.next.prev = node.prev  # 현재 노드의 다음 노드가 존재하면, 그 노드의 이전 포인터를 이전 노드로 설정
            node = node.prev  # 현재 노드를 병합된 이전 노드로 업데이트

        # 다음 노드와 병합 (현재 노드의 끝 주소가 다음 노드의 시작 주소와 동일한지 확인)
        if node.next and node.start + node.size == node.next.start:
            node.size += node.next.size  # 현재 노드의 크기를 다음 노드의 크기만큼 증가
            node.next = node.next.next  # 현재 노드의 다음 포인터를 다음 노드의 다음 포인터로 설정
            if node.next:
                node.next.prev = node  # 다음 노드의 다음 노드가 존재하면, 그 노드의 이전 포인터를 현재 노드로 설정

    def free(self, id):
        """
        메모리를 해제합니다.
        """
        for i, (block_id, size) in enumerate(self.arena):
            if block_id == id:
                # 해제된 블록을 이중 연결 리스트에 삽입
                self.insert_into_list(self.free_blocks_list_head, i * self.chunk_size, size)
                # 삽입된 노드와 인접한 빈 블록들을 병합
                self.merge_adjacent_free_blocks(self.free_blocks_list_head.next)
                del self.arena[i]  # 해제된 블록을 arena에서 삭제
                break

if __name__ == "__main__":
    allocator = Allocator()

    with open("./input.txt", "r") as file:
        start_time = time.time()
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] ==  'f':
                allocator.free(int(req[1]))

        end_time = time.time()
        execution_time = end_time - start_time

    allocator.print_stats()  # 통계 출력
    print("Execution Time:", execution_time)  # 실행 시간 출력

