"""
DES P-Box Permutation Module - 32-bit to 32-bit
"""

P_TABLE = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]


def bin_to_hex(bin_str):
    """Convert binary to hex string."""
    return hex(int(bin_str, 2))[2:].upper().zfill((len(bin_str) + 3) // 4)


def apply_p_box(s_box_output, verbose=False):
    """
    Apply P-box permutation (32-bit -> 32-bit).
    
    Args:
        s_box_output: 32-bit binary string
    Returns:
        32-bit binary string
    """
    result = ''.join(s_box_output[pos - 1] for pos in P_TABLE)
    if verbose:
        print(f"P-box: {bin_to_hex(s_box_output)} -> {bin_to_hex(result)}")
    return result


if __name__ == "__main__":
    s_out = "11100001101000001000101111010110"
    apply_p_box(s_out, verbose=True)
