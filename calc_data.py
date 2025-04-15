import argparse
import struct
import multiprocessing
import time
import os
import sys


def sequential_read(filename):
    """Lecture séquentielle du fichier"""
    min_val = 2 ** 32
    max_val = 0
    total = 0

    with open(filename, 'rb') as f:
        while chunk := f.read(4):
            num = struct.unpack('>I', chunk)[0]
            total += num
            min_val = min(min_val, num)
            max_val = max(max_val, num)

    return total, min_val, max_val


def process_chunk(args):
    """Traitement d'un segment du fichier (picklable)"""
    filename, start, end = args
    min_local = 2 ** 32
    max_local = 0
    total_local = 0

    with open(filename, 'rb') as f:
        f.seek(start)
        while f.tell() < end:
            chunk = f.read(4)
            if not chunk or len(chunk) != 4:
                break
            num = struct.unpack('>I', chunk)[0]
            total_local += num
            min_local = min(min_local, num)
            max_local = max(max_local, num)

    return total_local, min_local, max_local


def parallel_read(filename):
    """Lecture parallèle avec 4 processus fixes"""
    file_size = os.path.getsize(filename)
    chunk_size = (file_size // 4) & ~3  # Alignement sur 4 octets

    pool = multiprocessing.Pool(processes=4)
    try:
        results = pool.map(
            process_chunk,
            [(filename, i, min(i + chunk_size, file_size))
             for i in range(0, file_size, chunk_size)]
        )
    finally:
        pool.close()
        pool.join()

    total = sum(r[0] for r in results)
    min_val = min(r[1] for r in results)
    max_val = max(r[2] for r in results)
    return total, min_val, max_val


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--parallel', action='store_true', help="Mode parallèle")
    args = parser.parse_args()

    filename = 'data.bin'
    if not os.path.exists(filename):
        print("Erreur: data.bin introuvable. Exécutez d'abord create_data.py")
        sys.exit(1)

    start_time = time.time()

    if args.parallel:
        print("Mode parallèle activé...")
        total, min_val, max_val = parallel_read(filename)
    else:
        print("Mode séquentiel activé...")
        total, min_val, max_val = sequential_read(filename)

    print(f"Résultats:\n  Somme: {total}\n  Min: {min_val}\n  Max: {max_val}")
    print(f"Temps écoulé: {time.time() - start_time:.2f} secondes")
    sys.exit(0)


if __name__ == '__main__':
    main()