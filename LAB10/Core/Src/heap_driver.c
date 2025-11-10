#include "heap_driver.h"
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "main.h"     // for HAL_UART_Transmit
#include <stdio.h>

#define HEAP_START_ADDR ((uint8_t*)0x20001000)
#define HEAP_SIZE       (4 * 1024)   // 4 KB heap
#define BLOCK_SIZE      16           // Each block = 16 bytes
#define BLOCK_COUNT     (HEAP_SIZE / BLOCK_SIZE)

static uint8_t* const heap_base = HEAP_START_ADDR;
uint8_t block_map[BLOCK_COUNT]; // made non-static so main.c can access it

extern UART_HandleTypeDef huart1; // from main.c

void heap_print_map(const char* label)
{
    char msg[64];
    snprintf(msg, sizeof(msg), "\r\n[%s]\r\n", label);
    HAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);

    for (int i = 0; i < BLOCK_COUNT; i++) {
        char c = block_map[i] ? '1' : '0';
        HAL_UART_Transmit(&huart1, (uint8_t*)&c, 1, HAL_MAX_DELAY);
        if ((i + 1) % 32 == 0)
            HAL_UART_Transmit(&huart1, (uint8_t*)"\r\n", 2, HAL_MAX_DELAY);
    }
    HAL_UART_Transmit(&huart1, (uint8_t*)"\r\n", 2, HAL_MAX_DELAY);
    HAL_Delay(10);
}


/**
 * Initialize heap: all blocks free
 */
void heap_init(void)
{
    memset(block_map, 0, sizeof(block_map));
    heap_print_map("After heap_init");
}

/**
 * Allocate memory
 */
void* heap_alloc(size_t size)
{
    if (size == 0)
        return NULL;

    size_t blocks_needed = (size + BLOCK_SIZE - 1) / BLOCK_SIZE;
    size_t free_count = 0;
    size_t start_index = 0;

    for (size_t i = 0; i < BLOCK_COUNT; i++)
    {
        if (block_map[i] == 0)
        {
            if (free_count == 0)
                start_index = i;

            free_count++;

            if (free_count == blocks_needed)
            {
                for (size_t j = start_index; j < start_index + blocks_needed; j++)
                    block_map[j] = 1;

                heap_print_map("After heap_alloc");
                return (void*)(heap_base + (start_index * BLOCK_SIZE));
            }
        }
        else
        {
            free_count = 0;
        }
    }

    return NULL; // no space
}

/**
 * Free memory
 */
void heap_free(void* ptr)
{
    if (ptr == NULL)
        return;

    uintptr_t offset = (uint8_t*)ptr - heap_base;
    if (offset >= HEAP_SIZE)
        return;

    size_t index = offset / BLOCK_SIZE;

    for (size_t i = index; i < BLOCK_COUNT && block_map[i] == 1; i++)
        block_map[i] = 0;

    heap_print_map("After heap_free");
}
