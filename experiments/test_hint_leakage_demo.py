import unittest

from hint_leakage_demo import mat_vec_mod, recover_witness_2x2, run_demo


class HintLeakageDemoTests(unittest.TestCase):
    def test_demo_recovers_original_witness(self):
        original, hints, recovered = run_demo()
        self.assertEqual(hints, (5, 0))
        self.assertEqual(recovered, original)

    def test_singular_matrix_is_rejected(self):
        with self.assertRaises(ValueError):
            recover_witness_2x2(((1, 2), (2, 4)), (1, 2))

    def test_forward_and_inverse_agree(self):
        matrix = ((1, 1), (2, 1))
        witness = (4, 6)
        hints = mat_vec_mod(matrix, witness)
        self.assertEqual(recover_witness_2x2(matrix, hints), witness)


if __name__ == "__main__":
    unittest.main()
