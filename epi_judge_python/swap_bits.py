from test_framework import generic_test


def swap_bits(x, i, j):
    i_mask = 1 << i
    j_mask = 1 << j

    ith_value = (x & i_mask) >> i
    jth_value = (x & j_mask) >> j

    if ith_value != jth_value:
        x ^= (i_mask | j_mask)

    return x


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('swap_bits.py', 'swap_bits.tsv',
                                       swap_bits))
