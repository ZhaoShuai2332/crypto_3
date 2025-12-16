"""
DES Single Round Encryption - Detailed Step-by-Step Output
Calls: ip_sub, pc_, e_expend, xor_R, s_box_sub, p_box
"""

from ip_sub import get_L0_R0, hex_to_bin, bin_to_hex
from pc_ import get_subkey
from e_expend import expand_R
from s_box_sub import apply_s_boxes, S_BOXES
from p_box import apply_p_box, P_TABLE


def xor_bits(bits1, bits2):
    """XOR two bit strings."""
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bits1, bits2))


def print_step(step_num, title):
    """Print step header."""
    print(f"\n{'='*60}")
    print(f"Step {step_num}: {title}")
    print('='*60)


def des_single_round_detailed(plaintext_hex, key_hex, round_num=1):
    """
    Perform single round of DES with detailed output for each step.
    """
    print("=" * 70)
    print("DES Single Round Encryption - Detailed Process")
    print("=" * 70)
    print(f"Input Plaintext M = {plaintext_hex}")
    print(f"Input Key K = {key_hex} (56-bit, no parity)")
    print(f"Round Number = {round_num}")
    
    # ========== Step 1: Convert plaintext to binary ==========
    print_step(1, "Convert Plaintext to Binary")
    plaintext_bin = hex_to_bin(plaintext_hex, 64)
    print(f"M (hex): {plaintext_hex}")
    print(f"M (bin): {plaintext_bin}")
    print(f"Length:  {len(plaintext_bin)} bits")
    
    # ========== Step 2: Initial Permutation (IP) ==========
    print_step(2, "Initial Permutation (IP)")
    L0, R0 = get_L0_R0(plaintext_hex)
    print(f"After IP permutation, split into L0 and R0:")
    print(f"L0 (bin): {L0}")
    print(f"L0 (hex): {bin_to_hex(L0)}")
    print(f"R0 (bin): {R0}")
    print(f"R0 (hex): {bin_to_hex(R0)}")
    
    # ========== Step 3: Get Subkey K1 ==========
    print_step(3, f"Get Subkey K{round_num}")
    K = get_subkey(key_hex, round_num)
    print(f"Key K (hex): {key_hex}")
    print(f"Key K (bin): {hex_to_bin(key_hex, 56)}")
    print(f"After PC-2 permutation and circular shift:")
    print(f"K{round_num} (bin): {K}")
    print(f"K{round_num} (hex): {bin_to_hex(K)}")
    print(f"Length:  {len(K)} bits")
    
    # ========== Step 4: E-Expansion of R0 ==========
    print_step(4, "E-Expansion (32-bit → 48-bit)")
    E_R = expand_R(R0)
    print(f"Input R0 (32-bit):  {R0}")
    print(f"Output E(R0) (48-bit): {E_R}")
    print(f"E(R0) (hex): {bin_to_hex(E_R)}")
    print("\nE-expansion table mapping:")
    print("  32-bit input → 48-bit output (some bits repeated)")
    
    # ========== Step 5: XOR with Subkey ==========
    print_step(5, f"XOR: X = E(R0) ⊕ K{round_num}")
    X = xor_bits(E_R, K)
    print(f"E(R0):  {E_R}")
    print(f"K{round_num}:    {K}")
    print(f"X:      {X}")
    print(f"\nE(R0) (hex): {bin_to_hex(E_R)}")
    print(f"K{round_num} (hex):   {bin_to_hex(K)}")
    print(f"X (hex):     {bin_to_hex(X)}")
    
    # ========== Step 6: S-Box Substitution ==========
    print_step(6, "S-Box Substitution (48-bit → 32-bit)")
    print("X is divided into 8 groups of 6 bits each:")
    print("-" * 60)
    
    S_output = ""
    for i in range(8):
        six_bits = X[i*6:(i+1)*6]
        row = int(six_bits[0] + six_bits[5], 2)
        col = int(six_bits[1:5], 2)
        value = S_BOXES[i][row][col]
        four_bits = bin(value)[2:].zfill(4)
        S_output += four_bits
        
        print(f"S{i+1}: Input = {six_bits}")
        print(f"    Row = b1b6 = {six_bits[0]}{six_bits[5]} = {row}")
        print(f"    Col = b2b3b4b5 = {six_bits[1:5]} = {col}")
        print(f"    S{i+1}[{row}][{col}] = {value} = {four_bits}")
        print()
    
    print("-" * 60)
    print(f"S-box output (32-bit): {S_output}")
    print(f"S-box output (hex):    {bin_to_hex(S_output)}")
    
    # ========== Step 7: P-Box Permutation ==========
    print_step(7, "P-Box Permutation (32-bit → 32-bit)")
    P_output = apply_p_box(S_output)
    print(f"Input (S-box output): {S_output}")
    print(f"P-box table: {P_TABLE}")
    print(f"Output P(S): {P_output}")
    print(f"\nInput (hex):  {bin_to_hex(S_output)}")
    print(f"Output (hex): {bin_to_hex(P_output)}")
    
    # ========== Step 8: Compute L1 and R1 ==========
    print_step(8, "Compute L1 and R1")
    L1 = R0
    R1 = xor_bits(L0, P_output)
    
    print(f"L{round_num} = R{round_num-1}")
    print(f"L{round_num} (bin): {L1}")
    print(f"L{round_num} (hex): {bin_to_hex(L1)}")
    print()
    print(f"R{round_num} = L{round_num-1} ⊕ F(R{round_num-1}, K{round_num})")
    print(f"R{round_num} = L{round_num-1} ⊕ P(S(E(R{round_num-1}) ⊕ K{round_num}))")
    print(f"L{round_num-1}:    {L0}")
    print(f"F output: {P_output}")
    print(f"R{round_num}:      {R1}")
    print(f"R{round_num} (hex): {bin_to_hex(R1)}")
    
    # ========== Final Result ==========
    print("\n" + "=" * 70)
    print("FINAL RESULT - Round 1 Output")
    print("=" * 70)
    print(f"L{round_num} = {bin_to_hex(L1)}")
    print(f"R{round_num} = {bin_to_hex(R1)}")
    print(f"L{round_num}R{round_num} = {bin_to_hex(L1)}{bin_to_hex(R1)}")
    
    return L1, R1


if __name__ == "__main__":
    L1, R1 = des_single_round_detailed("FEFEFEFEFEFEFEFE", "55555555555555", 1)
