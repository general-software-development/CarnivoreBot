import uuid
import argparse
import hashlib
import base64

parser = argparse.ArgumentParser()
parser.add_argument("license_file")

args = parser.parse_args()

with open(args.license_file, 'r', encoding='utf8', errors='replace') as f:
    license_text = f.read()

B_ALPHABET = "0123456789" "abcdefghijkl" "ABCDEFGHIJKL" "wxyz" "WXYZ"
BASE = len(B_ALPHABET)  # 42

def bytes_to_base_custom(data: bytes) -> str:
    if not data:
        return ""

    number = int.from_bytes(data, byteorder="big", signed=False)

    if number == 0:
        return B_ALPHABET[0]

    result = []

    while number:
        number, remainder = divmod(number, BASE)
        result.append(B_ALPHABET[remainder])

    return "".join(reversed(result))

print(f"Last modified: xxx\n\n", end='')
print(f"Identifier: {uuid.uuid7()}:{uuid.uuid4()}:SHA3-512-{base64.b85encode(hashlib.sha3_512(license_text.encode('utf-32')).digest()).decode().replace("`", ".")}")
