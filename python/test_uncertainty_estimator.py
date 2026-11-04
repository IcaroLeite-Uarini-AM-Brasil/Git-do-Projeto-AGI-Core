import unittest

from uncertainty_estimator import EpistemicUncertaintyEstimator


class UncertaintyEstimatorTests(unittest.TestCase):
    def test_confident_predictions_have_low_entropy(self):
        result = EpistemicUncertaintyEstimator().estimate_uncertainty([
            [0.85, 0.10, 0.05], [0.80, 0.15, 0.05], [0.88, 0.08, 0.04],
        ])
        self.assertLess(result.shannon_entropy, 1.5)
        self.assertFalse(result.is_high_uncertainty)

    def test_rejects_invalid_probability_rows(self):
        with self.assertRaises(ValueError):
            EpistemicUncertaintyEstimator().estimate_uncertainty([[0.2, 0.2]])

    def test_rejects_empty_samples(self):
        with self.assertRaises(ValueError):
            EpistemicUncertaintyEstimator().estimate_uncertainty([])


if __name__ == "__main__":
    unittest.main()
