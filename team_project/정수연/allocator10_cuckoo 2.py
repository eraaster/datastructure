import time
import math

class CuckooHash:
    def __init__(self, size):
        self.size = size
        self.chunk_size = 16 * 1024  # 16KB
        self.table1 = [None] * self.size
        self.table2 = [None] * self.size
        self.hash1 = lambda x: hash(x) % self.size
        self.hash2 = lambda x: (hash(x) // self.size) % self.size
        self.memory_size = self.size * self.chunk_size * 2  # 두 개의 테이블, 각각의 키에 16KB 할당
        self.used_memory = 0

    def insert(self, key):
        if self.search(key):
            print(f"Error: Key {key} already exists.")
            return False

        for _ in range(self.size):
            pos1 = self.hash1(key)
            if self.table1[pos1] is None:
                self.table1[pos1] = key
                self.used_memory += self.chunk_size
                return True
            key, self.table1[pos1] = self.table1[pos1], key

            pos2 = self.hash2(key)
            if self.table2[pos2] is None:
                self.table2[pos2] = key
                self.used_memory += self.chunk_size
                return True
            key, self.table2[pos2] = self.table2[pos2], key

        print("Error: Hash table is full or loop detected")
        return False

    def search(self, key):
        return key == self.table1[self.hash1(key)] or key == self.table2[self.hash2(key)]

    def delete(self, key):
        pos1 = self.hash1(key)
        if self.table1[pos1] == key:
            self.table1[pos1] = None
            self.used_memory -= self.chunk_size
            return True
        pos2 = self.hash2(key)
        if self.table2[pos2] == key:
            self.table2[pos2] = None
            self.used_memory -= self.chunk_size
            return True
        return False

    def print_stats(self, start_time):
        end_time = time.time()
        time_taken = end_time - start_time
        arena_MB = self.memory_size / (1024 * 1024)
        used_MB = self.used_memory / (1024 * 1024)
        utilization = self.used_memory / self.memory_size
        print(f"Arena: {arena_MB:.2f} MB")
        print(f"In-use: {used_MB:.2f} MB")
        print(f"Utilization: {utilization:.2f}")
        print(f"Time taken: {time_taken:.2f} seconds")

if __name__ == "__main__":
    start_time = time.time()
    cuckoo = CuckooHash(131072)  # 큰 해시 테이블

    path = "/Users/jeongjaeung/Desktop/soongsil/ds_2024/assignment04/input.txt"
    with open(path, "r") as file:
        for line in file:
            parts = line.strip().split()
            cmd, key = parts[0], int(parts[1])
            if cmd == 'a':
                cuckoo.insert(key)
            elif cmd == 'd':
                cuckoo.delete(key)

    cuckoo.print_stats(start_time)
