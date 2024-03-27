class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CacheSimulatorLinkedList:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache = {}
        self.head = None
        self.tail = None
        self.cache_hit = 0
        self.tot_cnt = 0

    def do_sim(self, page):
        self.tot_cnt += 1
        if page in self.cache:
            self.cache_hit += 1
            node = self.cache[page]
            if node != self.head:
                if node == self.tail:
                    self.tail = self.tail.next
                node.next = None
                self.head.next = node
                self.head = node
        else:
            if len(self.cache) >= self.cache_slots:
                del self.cache[self.tail.data]
                self.tail = self.tail.next
            new_node = Node(page)
            self.cache[page] = new_node
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.head.next = new_node
                self.head = new_node

    def print_status(self):
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", self.cache_hit / self.tot_cnt)

if __name__ == "__main__":
    data_file = open("./linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulatorLinkedList(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        cache_sim.print_status()
