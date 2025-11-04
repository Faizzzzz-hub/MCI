#include "heap_driver.h"
#include <stdint.h>
#include <stddef.h>
#include <string.h>

#define HEAP_START_ADDR ((uint8_t*)0x20001000)
#define HEAP_SIZE       (4 * 1024)   // 4 KB heap
#define BLOCK_SIZE      16           // Each block = 16 bytes
#define BLOCK_COUNT     (HEAP_SIZE / BLOCK_SIZE)

// Static heap memory region (simulated, points to SRAM)
static uint8_t* const heap_base = HEAP_START_ADDR;

// Block allocation table: 0 = free, 1 = allocated
static uint8_t block_map[BLOCK_COUNT];

/**
 * @brief Initialize the heap by marking all blocks as free.
 */
void heap_init(void)
{
    memset(block_map, 0, sizeof(block_map));
}

/**
 * @brief Allocate a memory region of 'size' bytes.
 *
 * @param size Number of bytes requested.
 * @return Pointer to allocated region, or NULL if not enough memory.
 */
void* heap_alloc(size_t size)
{
    if (size == 0)
        return NULL;

    // Compute how many 16-byte blocks are needed
    size_t blocks_needed = (size + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // Search for contiguous free blocks
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
                // Found enough space — mark as used
                for (size_t j = start_index; j < start_index + blocks_needed; j++)
                    block_map[j] = 1;

                // Compute pointer to start of allocated region
                return (void*)(heap_base + (start_index * BLOCK_SIZE));
            }
        }
        else
        {
            free_count = 0; // Reset search
        }
    }

    // No enough contiguous space
    return NULL;
}

/**
 * @brief Free a previously allocated block of memory.
 *
 * @param ptr Pointer to memory previously returned by heap_alloc().
 */
void heap_free(void* ptr)
{
    if (ptr == NULL)
        return;

    // Compute block index from pointer
    uintptr_t offset = (uint8_t*)ptr - heap_base;

    if (offset >= HEAP_SIZE)
        return; // Pointer not within heap

    size_t index = offset / BLOCK_SIZE;

    // Free contiguous allocated blocks until a free one is found
    for (size_t i = index; i < BLOCK_COUNT && block_map[i] == 1; i++)
        block_map[i] = 0;
}
