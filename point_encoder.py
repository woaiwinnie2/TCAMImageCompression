
import math

def point_encoding(point, W,h):
    
    logh = h.bit_length() - 1
    prefix_keep = W - logh + 1
    
    gray = point ^ (point >> 1)  # BRGC conversion
    brgc_str = format(gray, f'0{W}b')  # Pad to 'bits' length
    
    extra_bits = []
    for i in range(h):
        if i == 0 or i == h // 2:
            continue
        val = ((point - i) // h) % 2
        extra_bits.append(str(1 - int(val)))

    BRGC_prefix= brgc_str[:prefix_keep]

    result=list(BRGC_prefix) + extra_bits
    
    return "".join(result)

def encode_block_point(data_stream, W, h): #encode 8*8 block
    
    encoded_bits = []
    for p in data_stream:
        encoded = point_encoding(p, W, h)
        encoded_bits.append(encoded)

    return "".join(encoded_bits)

