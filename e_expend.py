"""
DES E-Expansion Module - 32-bit to 48-bit expansion
"""

E_TABLE = [
    32, 1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]


def bin_to_hex(bin_str):
    """Convert binary to hex string."""
    return hex(int(bin_str, 2))[2:].upper().zfill((len(bin_str) + 3) // 4)


def expand_R(R_bits, verbose=False):
    """
    Expand 32-bit R to 48-bit.
    
    Args:
        R_bits: 32-bit binary string
    Returns:
        48-bit binary string
    """
    expanded = ''.join(R_bits[pos - 1] for pos in E_TABLE)
    if verbose:
        print(f"E(R): {R_bits} -> {expanded}")
        print(f"E(R) hex: {bin_to_hex(expanded)}")
    return expanded


if __name__ == "__main__":
    R = "11111111111111111111111111111111"
    expand_R(R, verbose=True)
