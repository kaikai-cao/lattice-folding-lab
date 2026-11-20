"""Unit tests for the s2 anchoring toy (educational algebra only).

These tests verify the Lemma 3.10 salt/message substitution identity and that
it is sensitive to a tampered target. They verify NOTHING about Module-SIS,
exact-ell_2 norm certificates, zero knowledge, or the real Pi_anc protocol.
"""

from __future__ import annotations

import unittest

from s2_anchor_toy import (
    P,
    anchoring_identity,
    commit_abdlop,
    run_demo,
)


class S2AnchorToyTests(unittest.TestCase):
    def test_commitment_uses_shared_B(self):
        A1 = [[1, 2], [3, 1]]
        A2 = [[2, 1], [1, 4]]
        B = [[1, 3], [2, 1]]
        s1, s2, m = [2, 1], [1, 2], [4, 5]
        tA, tB = commit_abdlop(A1, A2, B, s1, s2, m)
        # t_B = B*s2 + m must hold coordinate-wise.
        expected_tB = [((1 * 1 + 3 * 2) + 4) % P, ((2 * 1 + 1 * 2) + 5) % P]
        self.assertEqual(list(tB), expected_tB)
        # t_A = A1*s1 + A2*s2 (two output rows, each a 1-vector after dot).
        self.assertEqual(len(tA), 2)

    def test_honest_substitution_identity_holds(self):
        out = run_demo()
        self.assertTrue(out["honest_match"])
        self.assertEqual(out["u_from_tB"], out["r_from_m"])

    def test_tampered_target_breaks_identity(self):
        out = run_demo()
        self.assertTrue(out["tampered_match"] is False)
        self.assertNotEqual(out["tampered_u"], out["tampered_r"])

    def test_identity_is_bidirectional_on_weights(self):
        """Different public weights still yield the substitution identity."""
        A1 = [[1, 0], [0, 1]]
        A2 = [[1, 1], [1, 1]]
        B = [[2, 1], [1, 3]]
        s1, s2, m = [1, 1], [2, 1], [3, 4]
        _tA, tB = commit_abdlop(A1, A2, B, s1, s2, m)
        # True s2 aggregate with weights w=(1,2), iota=(0,1):
        # (B*s2)_0 = 2*2+1*1 = 5; (B*s2)_1 = 1*2+3*1 = 5 -> agg = 1*5+2*5 = 15 mod 31
        # With weight w=3, iota=0: true aggregate u_star = 3*(B*s2)_0 = 3*5 = 15.
        u_star = 15
        u, r = anchoring_identity([tB], [m], [3], [0], u_star)
        # tB[0] = 5+3 = 8 -> u = 3*8 - 15 = 9; r = 3*m[0] = 3*3 = 9.
        self.assertEqual(u, 9)
        self.assertEqual(r, 9)
        self.assertEqual(u, r)


if __name__ == "__main__":
    unittest.main()
