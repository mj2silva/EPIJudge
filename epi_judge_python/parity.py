from test_framework import generic_test
from test_framework.test_result import TestResult
from test_framework.test_timer import TestTimer
from test_framework.test_utils_console import print_test_info

# No cache
def parity_no_cache(x: int) -> int:
    result = 0
    while x:
        result ^= 1
        x &= x - 1
    return result

PRECOMPUTED_PARITY = []

for i in range(2 ** 16):
    PRECOMPUTED_PARITY.append(parity_no_cache(i))

# Using cache
def parity(x: int) -> int:
    MASK_SIZE = 16
    BIT_MASK = 0xFFFF

    return (PRECOMPUTED_PARITY[x >> (3 * MASK_SIZE)] ^
            PRECOMPUTED_PARITY[(x >> (2 * MASK_SIZE)) & BIT_MASK] ^
            PRECOMPUTED_PARITY[(x >> MASK_SIZE) & BIT_MASK] ^
            PRECOMPUTED_PARITY[x & BIT_MASK])

def variant(x: int) -> int:
    result = x + (x & ~(x - 1)) - 1
    return result

def mod_of_power_2(x: int, power_2) -> int:
    return x & (power_2 - 1)

def test_power_2(n: int) -> bool:
    return n > 0 and n == n & ~(n - 1)

def run_verbose_tests(name, test_function, test_cases) -> None:
    print('\n' + '=' * 60)
    print('INICIO: {}'.format(name))
    print('=' * 60)
    failures = []

    for test_nr, (arguments, expected) in enumerate(test_cases, 1):
        timer = TestTimer()
        actual = '<not returned>'
        timer.start()
        try:
            actual = test_function(*arguments)
            result = TestResult.PASSED if actual == expected else TestResult.FAILED
            if result != TestResult.PASSED:
                failures.append((arguments, expected, actual))
        except Exception as exc:
            result = TestResult.UNKNOWN_EXCEPTION
            failures.append((arguments, expected, exc))
        finally:
            timer.stop()

        diagnostic = ''
        if result != TestResult.PASSED:
            diagnostic = 'expected {}, got {}'.format(expected, actual)
        print_test_info(result, test_nr, len(test_cases), diagnostic, timer)

    print('\n' + '-' * 60)
    if failures:
        print('FIN: {} - {} de {} casos fallaron'.format(
            name, len(failures), len(test_cases)))
    else:
        print('FIN: {} - todos los casos pasaron'.format(name))
    print('=' * 60)
    assert not failures, failures

def test_variant() -> None:
    test_cases = [
        ((0b00000001,), 0b00000001),
        ((0b00000010,), 0b00000011),
        ((0b00000100,), 0b00000111),
        ((0b00001000,), 0b00001111),
        ((0b00010000,), 0b00011111),
        ((0b00011000,), 0b00011111),
        ((0b00101000,), 0b00101111),
        ((0b01010000,), 0b01011111),
        ((0b10000000,), 0b11111111),
        ((0b10010000,), 0b10011111),
    ]
    run_verbose_tests('variant', variant, test_cases)

def test_mod_of_power_2() -> None:
    test_cases = [
        ((77, 64), 13),
        ((0, 2), 0),
        ((1, 2), 1),
        ((2, 2), 0),
        ((15, 8), 7),
        ((16, 8), 0),
        ((255, 128), 127),
        ((256, 256), 0),
        ((1025, 2), 1),
        ((12345, 4096), 57),
    ]
    run_verbose_tests('mod_of_power_2', mod_of_power_2, test_cases)


def test_power_of_two_cases() -> None:
    test_cases = [
        ((0,), False),
        ((1,), True),
        ((2,), True),
        ((3,), False),
        ((4,), True),
        ((6,), False),
        ((8,), True),
        ((12,), False),
        ((16,), True),
        ((18,), False),
    ]
    run_verbose_tests('test_power_2', test_power_2, test_cases)


if __name__ == '__main__':
    test_variant()
    test_mod_of_power_2()
    test_power_of_two_cases()
    # exit(generic_test.generic_test_main('parity.py', 'parity.tsv', parity))
