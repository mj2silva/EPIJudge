from test_framework import generic_test


def reverse_bits(x: int) -> int:
    rev = 0
    for i in range(64):
        rev = rev << 1 | (x & 1)
        x >>= 1
    return rev


# IA Generated answer
def reverse_bits_optimized(x: int) -> int:
    x = ((x >> 1) & 0x5555555555555555) | (
        (x & 0x5555555555555555) << 1)
    x = ((x >> 2) & 0x3333333333333333) | (
        (x & 0x3333333333333333) << 2)
    x = ((x >> 4) & 0x0F0F0F0F0F0F0F0F) | (
        (x & 0x0F0F0F0F0F0F0F0F) << 4)
    x = ((x >> 8) & 0x00FF00FF00FF00FF) | (
        (x & 0x00FF00FF00FF00FF) << 8)
    x = ((x >> 16) & 0x0000FFFF0000FFFF) | (
        (x & 0x0000FFFF0000FFFF) << 16)
    return (x >> 32) | ((x & 0xFFFFFFFF) << 32)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_bits.py', 'reverse_bits.tsv',
                                       reverse_bits_optimized))
