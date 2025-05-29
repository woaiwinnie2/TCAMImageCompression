
import math

def interval_encoding(p, W, h):
    
    half_h = h // 2
    start = max(0, p - half_h)
    end = start + h-1
 
    if W is None:
        max_val = max(start, end)
        W = max_val.bit_length() if max_val != 0 else 1
    
    logh = h.bit_length() - 1
    prefix_keep = W - logh + 1

    # Generate all numbers in the interval 
    numbers = range(start, end + 1)
    
    # Compute BRGC for each number and format as binary strings
    brgc_strings = []
    for n in numbers:
        gray = n ^ (n >> 1)  # BRGC conversion
        brgc_str = format(gray, f'0{W}b')  # Pad to 'bits' length
        brgc_strings.append(brgc_str)
    
    # Determine ternary pattern by checking common bits
    pattern = []
    for i in range(W):
        bits_at_pos = [s[i] for s in brgc_strings]
        if all(b == bits_at_pos[0] for b in bits_at_pos):
            pattern.append(bits_at_pos[0])
        else:
            pattern.append('*')
    

    BRGC_prefix= ''.join(pattern)[:prefix_keep]

    extra_bits = []
    for i in range(h):
            if i == 0 or i == h // 2:
                continue
            if start % h == i:
                val = ((start - i) // h) % 2
                extra_bits.append(str(1 - int(val)))
            else:
                extra_bits.append('*')

    result=list(BRGC_prefix) + extra_bits

    return "".join(result)

def encode_block_interval(data_stream, W, h):
    
    encoded_bits = []
    for p in data_stream:
        encoded = interval_encoding(p, W, h)
        encoded_bits.append(encoded)

    return "".join(encoded_bits)
