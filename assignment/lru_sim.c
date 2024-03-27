#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CACHE_SLOTS 1000

typedef struct Node {
    char *data;
    struct Node *next;
} Node;

typedef struct {
    int cache_slots;
    Node *cache[CACHE_SLOTS];
    Node *head;
    Node *tail;
    int cache_hit;
    int tot_cnt;
} CacheSimulatorLinkedList;

void init_cache_simulator(CacheSimulatorLinkedList *cache_sim, int cache_slots) {
    cache_sim->cache_slots = cache_slots;
    cache_sim->head = NULL;
    cache_sim->tail = NULL;
    cache_sim->cache_hit = 0;
    cache_sim->tot_cnt = 0;
    for (int i = 0; i < CACHE_SLOTS; i++) {
        cache_sim->cache[i] = NULL;
    }
}

void do_sim(CacheSimulatorLinkedList *cache_sim, char *page) {
    cache_sim->tot_cnt++;
    int idx = atoi(page) % cache_sim->cache_slots;
    if (cache_sim->cache[idx] != NULL && cache_sim->cache[idx]->data != NULL && strcmp(cache_sim->cache[idx]->data, page) == 0) {
        cache_sim->cache_hit++;
        Node *node = cache_sim->cache[idx];
        if (node != cache_sim->head) {
            if (node == cache_sim->tail) {
                cache_sim->tail = cache_sim->tail->next;
            }
            node->next = NULL;
            cache_sim->head->next = node;
            cache_sim->head = node;
        }
    } else {
        if (cache_sim->cache[idx] != NULL) {
            free(cache_sim->cache[idx]->data); // 데이터 해제
            free(cache_sim->cache[idx]); // 노드 해제
        }
        Node *new_node = (Node *)malloc(sizeof(Node));
        new_node->data = strdup(page);
        new_node->next = NULL;
        cache_sim->cache[idx] = new_node;
        if (cache_sim->head == NULL) {
            cache_sim->head = new_node;
            cache_sim->tail = new_node;
        } else {
            cache_sim->head->next = new_node;
            cache_sim->head = new_node;
        }
    }
}

void print_status(CacheSimulatorLinkedList *cache_sim) {
    printf("cache_slot = %d cache_hit = %d hit ratio = %lf\n", cache_sim->cache_slots, cache_sim->cache_hit, (double)cache_sim->cache_hit / cache_sim->tot_cnt);
}

int main() {
    FILE *data_file = fopen("/Users/imin-yeong/Documents/2024/자료구조/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("Error opening file\n");
        return 1;
    }
    char line[255];
    CacheSimulatorLinkedList cache_sim;
    for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        init_cache_simulator(&cache_sim, cache_slots);
        while (fgets(line, sizeof(line), data_file)) {
            char *page = strtok(line, " ");
            do_sim(&cache_sim, page);
        }
        fseek(data_file, 0, SEEK_SET);
        print_status(&cache_sim);
    }
    fclose(data_file);
    return 0;
}
