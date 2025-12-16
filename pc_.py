"""
DES Key Schedule Module - Generate 16 subkeys from 56-bit key
"""

PC2_TABLE = [
    14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,  16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Cache for subkeys
_subkey_cache = {}


def hex_to_bin(hex_str, bits=56):
    """Convert hex to binary string."""
    return bin(int(hex_str, 16))[2:].zfill(bits)


def bin_to_hex(bin_str):
    """Convert binary to hex string."""
    return hex(int(bin_str, 2))[2:].upper().zfill((len(bin_str) + 3) // 4)


def circular_left_shift(bits, count):
    """Circular left shift."""
    return bits[count:] + bits[:count]


def pc2_permutation(key_bits):
    """Apply PC-2 permutation (56-bit -> 48-bit)."""
    return ''.join(key_bits[pos - 1] for pos in PC2_TABLE)


def generate_all_subkeys(hex_key, verbose=False):
    """Generate all 16 48-bit subkeys from 56-bit key."""
    if hex_key in _subkey_cache:
        return _subkey_cache[hex_key]
    
    bin_key = hex_to_bin(hex_key, 56)
    C, D = bin_key[:28], bin_key[28:]
    
    subkeys = []
    for i in range(16):
        C = circular_left_shift(C, SHIFT_SCHEDULE[i])
        D = circular_left_shift(D, SHIFT_SCHEDULE[i])
        subkey = pc2_permutation(C + D)
        subkeys.append(subkey)
        if verbose:
            print(f"K{i+1:2d}: {bin_to_hex(subkey)}")
    
    _subkey_cache[hex_key] = subkeys
    return subkeys


def get_subkey(hex_key, round_num, verbose=False):
    """Get subkey for a specific round (1-16)."""
    subkeys = generate_all_subkeys(hex_key)
    subkey = subkeys[round_num - 1]
    if verbose:
        print(f"K{round_num}: {bin_to_hex(subkey)}")
    return subkey


if __name__ == "__main__":
    generate_all_subkeys("55555555555555", verbose=True)
