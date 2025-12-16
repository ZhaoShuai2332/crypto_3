"""
DES Initial Permutation (IP) Module
"""

# IP permutation table (64-bit -> 64-bit)
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# IP^-1 (Inverse Initial Permutation) table
IP_INV_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9,  49, 17, 57, 25
]


def hex_to_bin(hex_str, bits=64):
    """Convert hexadecimal string to binary string."""
    return bin(int(hex_str, 16))[2:].zfill(bits)


def bin_to_hex(bin_str):
    """Convert binary string to hexadecimal string."""
    hex_len = (len(bin_str) + 3) // 4
    return hex(int(bin_str, 2))[2:].upper().zfill(hex_len)


def ip_permutation(input_bits):
    """Apply IP permutation to 64-bit input."""
    return ''.join(input_bits[pos - 1] for pos in IP_TABLE)


def ip_inverse_permutation(input_bits):
    """Apply IP^-1 permutation to 64-bit input."""
    return ''.join(input_bits[pos - 1] for pos in IP_INV_TABLE)


def get_L0_R0(plaintext_hex, verbose=False):
    """
    Get L0 and R0 from 64-bit plaintext after IP permutation.
    
    Returns: Tuple of (L0, R0) as 32-bit binary strings
    """
    bin_input = hex_to_bin(plaintext_hex, 64)
    bin_output = ip_permutation(bin_input)
    L0, R0 = bin_output[:32], bin_output[32:]
    
    if verbose:
        print(f"IP Input:  {plaintext_hex}")
        print(f"L0 (hex):  {bin_to_hex(L0)}")
        print(f"R0 (hex):  {bin_to_hex(R0)}")
    
    return L0, R0


def apply_ip_inverse(L_R_bits, verbose=False):
    """Apply IP^-1 to 64-bit input (R16||L16)."""
    result = ip_inverse_permutation(L_R_bits)
    if verbose:
        print(f"IP^-1 Input:  {bin_to_hex(L_R_bits)}")
        print(f"IP^-1 Output: {bin_to_hex(result)}")
    return result


if __name__ == "__main__":
    L0, R0 = get_L0_R0("FEFEFEFEFEFEFEFE", verbose=True)
