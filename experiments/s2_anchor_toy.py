"""Toy algebraic check of LBF Lemma 3.10 (salt/message substitution).

Educational algebra verification ONLY. It is NOT a cryptographic implementation:
it does NOT prove Module-SIS hardness, does NOT implement ABDLOP with Gaussian
salts / rejection sampling, does NOT give any exact-ell_2 norm certificate, and
does NOT implement the LatticeBlindFold anchoring proof of knowledge (Pi_anc).

What it DOES verify, over a small prime field F_p with ell=1 (so ct = constant
coefficient = the single coordinate):

  ABDLOP commitment (LBF eq. 2.5):  t_A = A1*s1 + A2*s2,  t_B = B*s2 + m  (mod q)
  Lemma 3.10 substitution:  B*s2 = t_B - m, hence for public weights w_n and
  row indices iota(n):

      ct( sum_n w_n * (B*s2^(n))_{iota(n)} ) == u_star
      <==>  ct( sum_n w_n * m^(n)_{iota(n)} ) - u == 0,
      where u = sum_n w_n * (t_B^(n))_{iota(n)} - u_star.

This is the exact algebraic identity that lets LBF "reach" the BDLOP salt s2
through committed messages, i.e. the algebraic core of the anchoring relation.
The norm aspect (exact-ell_2 on s2) is deliberately NOT tested here: LBF does
not instantiate it (Remark 4.8), and this toy does not pretend otherwise.
"""

from __future__ import annotations

from typing import List, Sequence

P = 31  # small prime; stands in for q in the identity (no ring structure used)


def _dot_mod(a: Sequence[int], b: Sequence[int], q: int = P) -> int:
    return sum(x * y for x, y in zip(a, b)) % q


def _vec_add(a: Sequence[int], b: Sequence[int], q: int = P) -> List[int]:
    return [(x + y) % q for x, y in zip(a, b)]


def _scalar_vec(c: int, a: Sequence[int], q: int = P) -> List[int]:
    return [(c * x) % q for x in a]


def commit_abdlop(
    A1: Sequence[Sequence[int]],
    A2: Sequence[Sequence[int]],
    B: Sequence[Sequence[int]],
    s1: Sequence[int],
    s2: Sequence[int],
    m: Sequence[int],
    q: int = P,
):
    """Return (t_A, t_B) = (A1*s1 + A2*s2, B*s2 + m) mod q, with ell = len(m)."""
    tA = [_vec_add(_dot_row(A1, r, s1, q), _dot_row(A2, r, s2, q), q) for r in range(len(A1))]
    tB = _vec_add(_mat_vec(B, s2, q), m, q)
    return tA, tB


def _dot_row(matrix: Sequence[Sequence[int]], row: int, vec: Sequence[int], q: int) -> List[int]:
    # row of matrix dotted with vec -> scalar; wrap into length-1 list for uniform handling
    return [_dot_mod(matrix[row], vec, q)]


def _mat_vec(matrix: Sequence[Sequence[int]], vec: Sequence[int], q: int = P) -> List[int]:
    return [_dot_mod(row, vec, q) for row in matrix]


def anchoring_identity(
    tB_list: Sequence[Sequence[int]],
    m_list: Sequence[Sequence[int]],
    weights: Sequence[int],
    iota: Sequence[int],
    u_star: int,
    q: int = P,
):
    """Compute the two sides of Lemma 3.10 and check equivalence.

    Left  (s2-side):   L = sum_n w_n * tB^(n)_{iota(n)} - u_star
                       -- this equals sum_n w_n * (B s2^(n))_{iota(n)} when
                       tB^(n) = B s2^(n) + m^(n).
    Right (m-side):    R = sum_n w_n * m^(n)_{iota(n)}
    Lemma 3.10: (s2 aggregate == u_star)  <=>  R - u == 0,
                where u = sum_n w_n * tB^(n)_{iota(n)} - u_star = L.
    Hence we expect R == L (mod q) whenever the s2 aggregate equals u_star.
    """
    u = sum(w * tB[i] % q for w, tB, i in zip(weights, tB_list, iota)) % q
    u = (u - u_star) % q
    r = sum(w * m[i] % q for w, m, i in zip(weights, m_list, iota)) % q
    return u, r


def run_demo():
    # Two ABDLOP commitments with shared B, ell = 1 (so ct is the single coordinate).
    A1 = [[1, 2], [3, 1]]  # 2 x 2
    A2 = [[2, 1], [1, 4]]  # 2 x 2
    B = [[1, 3], [2, 1]]   # ell=2 rows would need len(m)=2; use ell=2
    # Use ell = len(m) = 2; row index iota in {0,1}.
    s1_list = [[2, 1], [3, 2]]
    s2_list = [[1, 2], [2, 1]]
    m_list = [[4, 5], [1, 3]]

    tB_list = []
    for s1, s2, m in zip(s1_list, s2_list, m_list):
        _tA, tB = commit_abdlop(A1, A2, B, s1, s2, m)
        tB_list.append(tB)

    weights = [3, 5]
    iota = [0, 1]

    # Compute the true s2 aggregate: sum_n w_n * (B s2^(n))_{iota(n)}.
    s2_agg = sum(w * _mat_vec(B, s2)[i] % P for w, s2, i in zip(weights, s2_list, iota)) % P
    u_star = s2_agg  # honest case: V's target equals the true aggregate

    u, r = anchoring_identity(tB_list, m_list, weights, iota, u_star)

    # Wrong case: tamper the target; the m-side no longer matches.
    u_bad, r_bad = anchoring_identity(tB_list, m_list, weights, iota, (u_star + 1) % P)
    return {
        "P": P,
        "s2_aggregate": s2_agg,
        "u_from_tB": u,
        "r_from_m": r,
        "honest_match": (u == r),
        "tampered_u": u_bad,
        "tampered_r": r_bad,
        "tampered_match": (u_bad == r_bad),
    }


if __name__ == "__main__":
    out = run_demo()
    print("Field: F_%d" % out["P"])
    print("s2 aggregate (s2-side):      ", out["s2_aggregate"])
    print("u from public t_B:           ", out["u_from_tB"])
    print("r from committed messages m: ", out["r_from_m"])
    print("Lemma 3.10 honest identity holds (u == r):", out["honest_match"])
    print("Tampered target -> u,r:", out["tampered_u"], out["tampered_r"])
    print("Tampered target breaks identity (u != r):", not out["tampered_match"])
    print("NOTE: teaching algebra only; no exact-ell_2, no Module-SIS, no ZK.")
