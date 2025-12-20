#!/usr/bin/python3

# prepare_test.py <test>
# read <test>.bin0, append reset vector to output <test>.bin
# read <test>.asm, extract comment between RESULT / END_RESULT
# and output as res_<test>.bin

import sys
import os
import re

def main():
    if len(sys.argv) != 2:
        print("Usage: python prepare_test.py <test>")
        return

    test_name = sys.argv[1]
    bin0_file = f"{test_name}.bin0"
    asm_file = f"{test_name}.asm"
    res_file = f"res_{test_name}.bin"

    # Process .bin0 file
    try:
        with open(bin0_file, "rb") as f:
            bin0_data = f.read()

        if len(bin0_data) < 65536 - 16:
            bin0_data += b'\x00' * (65536 - 16 - len(bin0_data))

        # Append reset vector
        reset_vector = b'\xea\x00\x00\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff'
        combined_data = bin0_data + reset_vector

        with open(f"{test_name}.bin", "wb") as f:
            f.write(combined_data)
        print(f"Created {test_name}.bin with reset vector appended")

    except FileNotFoundError:
        print(f"Error: {bin0_file} not found")
        return

    # Process .asm file
    try:
        with open(asm_file, "r") as f:
            lines = f.readlines()

        result_content = ""
        in_result = False

        for line in lines:
            if re.search(r';\s*RESULT', line, re.IGNORECASE):
                in_result = True
                continue
            if re.search(r';\s*END_RESULT', line, re.IGNORECASE):
                in_result = False
                break
            if in_result:
                s = line.strip()
                if s.startswith(';'):
                    s = s[1:].strip()
                result_content += s + " "

        if not result_content:
            print(f"No RESULT block found in {asm_file}")
            return

        # print('result string: ', result_content)

        # Convert hex string to bytes
        hex_values = result_content.strip().split()
        try:
            res_data = bytes.fromhex("".join(hex_values))
        except ValueError as e:
            print(f"Invalid hex format in {asm_file}: {e}")
            return

        # print("hex: ", res_data)

        with open(res_file, "wb") as f:
            f.write(res_data)
        print(f"Created {res_file} with extracted hex data")

    except FileNotFoundError:
        print(f"Error: {asm_file} not found")

if __name__ == "__main__":
    main()