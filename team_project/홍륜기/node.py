class Node:
    def __init__(self, start, size, color="red"):
        """
        Red-Black 트리에서 사용되는 노드를 정의

        start : 메모리 블록의 시작 주소
        size : 메모리 블록의 크기
        color : 노드의 색상 (기본값 : red)
        parent : 부모 노드
        left/right : 왼쪽/오른쪽 자식 노드
        """
        self.start = start
        self.size = size
        self.color = color  # Red or Black
        self.parent = None
        self.left = None
        self.right = None
