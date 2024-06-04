from node import *

class RedBlackTree:
    def __init__(self):
        """
        Red-Black 트리 자료구조 구현

        NIL_LEAF : 리프노드를 의미
        root : 트리의 루트 노드
        
        Red-Black 트리의 속성 : 루트/리프 노드는 모두 Black
        """
        self.NIL_LEAF = Node(0, 0, color="black")
        self.root = self.NIL_LEAF

    def insert(self, start, size):
        """
        새로운 노드 삽입.

        start : 메모리 블록의 시작 주소
        size : 메모리 블록의 크기
        """
        # 처음 노드 삽입 시 색은 Red(default)
        new_node = Node(start, size)
        # 삽입할 새로운 노드에 리프 노드 달아놓기
        new_node.left = self.NIL_LEAF
        new_node.right = self.NIL_LEAF
        # 새로운 노드 삽입 후, Red-Black 트리 속성 유지 위한 수선 작업 수행
        self._insert(new_node)
        self._fix_insert(new_node)

    def _insert(self, new_node):
        """
        트리에 새로운 노드 삽입하는 내부 메소드

        new_node : 삽입할 새로운 노드
        """
        y = self.NIL_LEAF
        x = self.root
        while x != self.NIL_LEAF:
            y = x
            if new_node.start < x.start:
                x = x.left
            else:
                x = x.right
        new_node.parent = y
        if y == self.NIL_LEAF:
            self.root = new_node
        elif new_node.start < y.start:
            y.left = new_node
        else:
            y.right = new_node
        new_node.color = "red"

    def _fix_insert(self, k):
        """
        삽입 후, Red-Black 트리의 속성을 유지하기 위해 트리를 수선하는 내부 메소드

        k : 삽입된 노드
        """
        # k 의 parent 가 red 일 경우만 수선 작업이 필요함 (조건 맞을 때까지 반복)
        while k != self.root and k.parent.color == "red":
            # parent 의 형제노드 파악 위해 parent 노드가 어딨는지 확인
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right # parent 의 형제노드
                # parent 의 형제노드가 Red 일 경우, parent 와 형제노드 Black 로 바꾸고, p^2 노드를 Red 로 변경후, 새롭게 삽입된 노드로 취급 
                if u.color == "red":
                    k.parent.color = "black"
                    u.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                # parent 의 형제노드가 Black 일 경우
                else:
                    # 오른쪽 자식일 경우, parent 를 기준으로 좌회전
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    # 왼쪽 자식일 경우, parent 의 parent 을 기준으로 우회전 후 parent 와 parent, parent 의 색상 바꿈
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self._right_rotate(k.parent.parent)
            # parent 의 형제노드 파악 위해 parent 노드가 어딨는지 확인
            else:
                u = k.parent.parent.left # parent 의 형제노드
                if u.color == "red":
                    k.parent.color = "black"
                    u.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self._left_rotate(k.parent.parent)
        self.root.color = "black"

    def _left_rotate(self, x):
        """
        수선 위해 좌회전 수행하는 내부 메서드

        x : 회전의 중심 노드
        """
        y = x.right
        x.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL_LEAF:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """
        수선위해 우회전 수행 메소드

        x : 회전의 중심 노드
        """
        y = x.left
        x.left = y.right
        if y.right != self.NIL_LEAF:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL_LEAF:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, start):
        """
        특정 시작 주소 가진 노드 삭제

        start : 삭제할 노드의 시작 주소
        """
        node_to_delete = self._search_tree_helper(self.root, start)
        if node_to_delete != self.NIL_LEAF:
            self._delete(node_to_delete)

    def _delete(self, node):
        """
        트리에서 노드를 삭제하는 내부 메소드

        node : 지정된 삭제할 노드
        """
        z = node
        y = z
        y_original_color = y.color
        if z.left == self.NIL_LEAF:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.NIL_LEAF:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self._fix_delete(x)

    def _fix_delete(self, x):
        """
        삭제 후 Red-Black 트리의 속성을 유지하기 위해 트리를 수정하는 내부 메소드

        x : 삭제된 노드의 자리를 채운 노드
        """
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.right.color == "black":
                        w.left.color = "black"
                        w.color = "red"
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = "black"

    def _rb_transplant(self, u, v):
        """
        트리에서 두 노드의 자리를 교체하는 내부 메소드

        u, v : 교체될 노드
        """
        if u.parent == self.NIL_LEAF:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _search_tree_helper(self, node, key):
        """
        트리에서 특정 키 값을 가진 노드를 검색하는 내부 메소드

        node : 현재 노드
        key : 검색할 키 값

        반환 : 검색된 노드
        """
        if node == self.NIL_LEAF or key == node.start:
            return node
        if key < node.start:
            return self._search_tree_helper(node.left, key)
        return self._search_tree_helper(node.right, key)

    def _minimum(self, node):
        """
        특정 서브 트리에서 가장 작은 값을 가진 노드를 찾는 내부 메소드

        node : 서브 트리의 루트 노드
        """
        while node.left != self.NIL_LEAF:
            node = node.left
        return node

    def search(self, size):
        """
        주어진 크기 이상의 메모리 블록 검색

        size : 검색할 메모리 블록의 크기

        검색된 메모리 블록을 포함하는 노드
        """
        return self._search(self.root, size)

    def _search(self, root, size):
        """
        주어진 크기 이상의 메모리 블록을 검색하는 내부 메소드

        root : 현재 검색 진행중인 노드
        size : 검색할 메모리 블록의 크기

        검색된 메모리 블록을 가진 노드 반환
        """
        if not root or root == self.NIL_LEAF or root.size >= size:
            return root
        if root.size < size:
            return self._search(root.right, size)
        return self._search(root.left, size)

    def inorder(self):
        return self._inorder(self.root)
        
    def _inorder(self, root):
        """
        중위 순회를 통해 트리의 모든 노드를 리스트로 반환

        root : 현재 노드
        list : 중위 순회된 노드들의 리스트
        """
        if root == self.NIL_LEAF:
            return []
        return self._inorder(root.left) + [root] + self._inorder(root.right)
