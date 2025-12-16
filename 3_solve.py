from s_box_sub import S_BOXES


def get_bit(value, position, total_bits):
    bit_index = total_bits - position
    return (value >> bit_index) & 1


def calculate_bias_for_sbox(sbox_index, verbose=False):
    
    sbox = S_BOXES[sbox_index]
    count_zero = 0
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"S{sbox_index + 1} Box Analysis: X2 XOR Y1 XOR Y2 XOR Y3 XOR Y4")
        print(f"{'='*70}")
        print(f"Input:  X = X1X2X3X4X5X6 (6 bits)")
        print(f"Output: Y = Y1Y2Y3Y4 (4 bits)")
        print(f"S-box lookup: Row = X1X6, Col = X2X3X4X5\n")
        print(f"{'X(dec)':<8} {'X(bin)':<10} {'X2':<4} {'Row':<5} {'Col':<5} "
              f"{'Y(dec)':<8} {'Y(bin)':<8} {'Result':<8}")
        print("-" * 70)
    
    # 遍历所有64种可能的6位输入
    for x in range(64):
        x1 = get_bit(x, 1, 6)
        x2 = get_bit(x, 2, 6)
        x3 = get_bit(x, 3, 6)
        x4 = get_bit(x, 4, 6)
        x5 = get_bit(x, 5, 6)
        x6 = get_bit(x, 6, 6)
        
        row = (x1 << 1) | x6
        col = (x2 << 3) | (x3 << 2) | (x4 << 1) | x5
        
        y = sbox[row][col]
        
        y1 = get_bit(y, 1, 4)
        y2 = get_bit(y, 2, 4)
        y3 = get_bit(y, 3, 4)
        y4 = get_bit(y, 4, 4)
        
        expression = x2 ^ y1 ^ y2 ^ y3 ^ y4
        
        if expression == 0:
            count_zero += 1
        
        if verbose:
            print(f"{x:<8} {x:06b}     {x2:<4} {row:<5} {col:<5} "
                  f"{y:<8} {y:04b}     {expression:<8}")
    
    count_one = 64 - count_zero
    probability = count_zero / 64
    bias = abs(probability - 0.5)
    
    if verbose:
        print("-" * 70)
        print(f"\nStatistics:")
        print(f"  Count(expression = 0): {count_zero}")
        print(f"  Count(expression = 1): {count_one}")
        print(f"  Pr(X2 XOR Y1 XOR Y2 XOR Y3 XOR Y4 = 0) = {count_zero}/64 = {probability:.4f}")
        print(f"\nBias Calculation:")
        print(f"  e = |Pr(expr=0) - 1/2|")
        print(f"  e = |{count_zero}/64 - 32/64|")
        print(f"  e = |{count_zero - 32}|/64")
        print(f"  e = {abs(count_zero - 32)}/64 = {bias:.4f}")
    
    return bias, count_zero, probability


def main():
    print("=" * 70)
    print("DES S-box Linear Approximation Analysis")
    print("Calculate bias of: X2 XOR Y1 XOR Y2 XOR Y3 XOR Y4")
    print("=" * 70)
    
    print("\n[Theory Background]")
    print("-" * 70)
    print("In linear cryptanalysis, bias measures the deviation from randomness.")
    print("Definition: bias e = |Pr(linear expression = 0) - 1/2|")
    print("If e = 0: completely random (no correlation)")
    print("If e > 0: bias exists (linear correlation)")
    print("-" * 70)
    
    results = []
    
    # 对第一个S盒显示详细过程
    print("\n" + "=" * 70)
    print("STEP-BY-STEP CALCULATION FOR S1 BOX")
    print("=" * 70)
    bias, count_zero, prob = calculate_bias_for_sbox(0, verbose=True)
    results.append((1, bias, count_zero, prob))
    
    # 对其他S盒只计算结果
    print("\n" + "=" * 70)
    print("CALCULATING FOR REMAINING S-BOXES (S2-S8)")
    print("=" * 70)
    
    for i in range(1, 8):
        bias, count_zero, prob = calculate_bias_for_sbox(i, verbose=False)
        results.append((i + 1, bias, count_zero, prob))
        print(f"S{i+1}: Count(=0)={count_zero:2d}, Pr(=0)={prob:.4f}, bias={bias:.4f} ({abs(count_zero-32)}/64)")
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("SUMMARY OF ALL S-BOXES")
    print("=" * 70)
    print(f"\n{'S-box':<10} {'Pr(=0)':<15} {'Count(=0)':<12} {'Bias e':<15}")
    print("-" * 55)
    
    for sbox_num, bias, count_zero, prob in results:
        print(f"S{sbox_num:<9} {prob:.4f}          {count_zero:<12} {bias:.4f} ({abs(count_zero-32)}/64)")
    
    print("-" * 55)
    
    max_bias = max(results, key=lambda x: x[1])
    min_bias = min(results, key=lambda x: x[1])
    
    print(f"\nMax bias: S{max_bias[0]} box, e = {max_bias[1]:.4f}")
    print(f"Min bias: S{min_bias[0]} box, e = {min_bias[1]:.4f}")
    
    print("\n[Conclusion]")
    print("-" * 70)
    print("The results show the bias for linear approximation")
    print("X2 XOR Y1 XOR Y2 XOR Y3 XOR Y4 = 0 for each S-box.")
    print("Larger bias indicates stronger linear correlation,")
    print("which can be exploited in linear cryptanalysis attacks.")
    print("Ideal S-boxes should have all biases close to 0.")


if __name__ == "__main__":
    main()
