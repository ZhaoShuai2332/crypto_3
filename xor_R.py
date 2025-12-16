"""
DES XOR Module - X = E(R) ⊕ K
"""

from e_expend import expand_R
from pc_ import get_subkey


def bin_to_hex(bin_str):
    """Convert binary to hex string."""
    return hex(int(bin_str, 2))[2:].upper().zfill((len(bin_str) + 3) // 4)


def xor_bits(bits1, bits2):
    """XOR two bit strings of equal length."""
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bits1, bits2))


def compute_xor(R_bits, K_bits, verbose=False):
    """
    Compute X = E(R) ⊕ K.
    
    Args:
        R_bits: 32-bit binary string
        K_bits: 48-bit binary string (subkey)
    Returns:
        48-bit binary string
    """
    E_R = expand_R(R_bits)
    X = xor_bits(E_R, K_bits)
    if verbose:
        print(f"E(R):    {bin_to_hex(E_R)}")
        print(f"K:       {bin_to_hex(K_bits)}")
        print(f"X=E(R)⊕K: {bin_to_hex(X)}")
    return X


if __name__ == "__main__":
    R = "11111111111111111111111111111111"
    K = get_subkey("55555555555555", 1)
    compute_xor(R, K, verbose=True)
