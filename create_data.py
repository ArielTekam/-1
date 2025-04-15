import random
import os


def generate_binary_file(filename='data.bin', size_gb=2):
    """Génère un fichier binaire d'entiers 32 bits non signés"""
    size_bytes = size_gb * 1024 ** 3
    num_ints = size_bytes // 4

    with open(filename, 'wb') as f:
        for _ in range(num_ints):
            # Génère un entier strictement inférieur à 2^32
            num = random.randint(0, 2 ** 32 - 1)
            f.write(num.to_bytes(4, byteorder='big'))

    print(f"Fichier {filename} créé. Taille : {os.path.getsize(filename) / 1024 ** 3:.2f} GB")


if __name__ == '__main__':
    generate_binary_file()