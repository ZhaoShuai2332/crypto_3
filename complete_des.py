"""
Complete DES Encryption (16 Rounds)
Calls: ip_sub, pc_, e_expend, xor_R, s_box_sub, p_box
"""

from ip_sub import get_L0_R0, apply_ip_inverse, bin_to_hex
from pc_ import generate_all_subkeys
from xor_R import compute_xor, xor_bits
from s_box_sub import apply_s_boxes
from p_box import apply_p_box


def feistel_f(R, K):
    """Feistel function F(R, K) = P(S(E(R) ⊕ K))"""
    X = compute_xor(R, K)
    S_out = apply_s_boxes(X)
    P_out = apply_p_box(S_out)
    return P_out


def des_round(L, R, K):
    """One round of DES: (L', R') = (R, L ⊕ F(R, K))"""
    F_out = feistel_f(R, K)
    return R, xor_bits(L, F_out)


def des_encrypt(plaintext_hex, key_hex, verbose=True):
    """
    Complete 16-round DES encryption.
    
    Args:
        plaintext_hex: 16-char hex (64-bit plaintext)
        key_hex: 14-char hex (56-bit key, no parity)
    Returns:
        16-char hex ciphertext
    """
    if verbose:
        print("=" * 60)
        print("DES Complete Encryption")
        print("=" * 60)
        print(f"Plaintext: {plaintext_hex}")
        print(f"Key:       {key_hex}\n")
    
    # Generate all subkeys
    subkeys = generate_all_subkeys(key_hex, verbose=verbose)
    
    # IP permutation
    L, R = get_L0_R0(plaintext_hex, verbose=verbose)
    if verbose:
        print()
    
    # 16 Feistel rounds
    for i in range(16):
        L, R = des_round(L, R, subkeys[i])
        if verbose:
            print(f"Round {i+1:2d}: L={bin_to_hex(L)} R={bin_to_hex(R)}")
    
    # Final swap and IP^-1
    combined = R + L  # R16 || L16
    ciphertext_bin = apply_ip_inverse(combined, verbose=verbose)
    ciphertext_hex = bin_to_hex(ciphertext_bin)
    
    if verbose:
        print(f"\nCiphertext: {ciphertext_hex}")
    
    return ciphertext_hex


def des_encrypt_n_rounds(plaintext_hex, key_hex, num_rounds, verbose=True):
    """DES encryption for specified number of rounds (without IP^-1)."""
    subkeys = generate_all_subkeys(key_hex)
    L, R = get_L0_R0(plaintext_hex)
    
    if verbose:
        print(f"L0={bin_to_hex(L)} R0={bin_to_hex(R)}")
    
    for i in range(min(num_rounds, 16)):
        L, R = des_round(L, R, subkeys[i])
        if verbose:
            print(f"Round {i+1:2d}: L={bin_to_hex(L)} R={bin_to_hex(R)}")
    
    return L, R


if __name__ == "__main__":
    ciphertext = des_encrypt("FEFEFEFEFEFEFEFE", "55555555555555", verbose=True)
