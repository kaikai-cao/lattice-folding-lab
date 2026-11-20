"""Toy demonstration: public linear hints can reveal a witness over F_7.

This is an educational linear-algebra example only. It is NOT an attack on
LatticeBlindFold and does not implement Sum-check, Ajtai commitments, or ABDLOP.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

P = 7
Matrix2 = Tuple[Tuple[int, int], Tuple[int, int]]
Vector2 = Tuple[int, int]


def mat_vec_mod(matrix: Matrix2, vector: Vector2, modulus: int = P) -> Vector2:
    return tuple(sum(a * b for a, b in zip(row, vector)) % modulus for row in matrix)  # type: ignore[return-value]


def recover_witness_2x2(
    matrix: Matrix2, hints: Vector2, modulus: int = P
) -> Vector2:
    """Recover x from Mx=y over F_p for a 2x2 matrix with nonzero determinant."""
    (a, b), (c, d) = matrix
    det = (a * d - b * c) % modulus
    if det == 0:
        raise ValueError("matrix is singular over the selected finite field")

    det_inv = pow(det, -1, modulus)
    y1, y2 = hints
    x1 = (det_inv * (d * y1 - b * y2)) % modulus
    x2 = (det_inv * (-c * y1 + a * y2)) % modulus
    return x1, x2


def run_demo() -> tuple[Vector2, Vector2, Vector2]:
    witness: Vector2 = (2, 3)
    matrix: Matrix2 = ((1, 1), (2, 1))
    hints = mat_vec_mod(matrix, witness)
    recovered = recover_witness_2x2(matrix, hints)
    return witness, hints, recovered


if __name__ == "__main__":
    original, public_hints, recovered = run_demo()
    print(f"Field: F_{P}")
    print(f"Original witness: {original}")
    print(f"Public linear hints: {public_hints}")
    print(f"Recovered witness: {recovered}")
    print(f"Recovery successful: {original == recovered}")
