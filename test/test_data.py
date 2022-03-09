import io
import shutil
import tempfile
import unittest

import NLEval.data
import pytest


class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.mkdtemp()
        print(f"Created temporary directory for testing data: {cls.tmp_dir}")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_dir)
        print(f"Removed temporary directory: {cls.tmp_dir}")

    @pytest.mark.longruns
    def test_biogrid(self):
        graph = NLEval.data.BioGRID(self.tmp_dir)
        self.assertEqual(graph.size, 25711)
        self.assertEqual(graph.num_edges, 1200394)

    def test_bioplex(self):
        graph = NLEval.data.BioPlex(self.tmp_dir)
        self.assertEqual(graph.size, 8364)
        self.assertEqual(graph.num_edges, 71408)

        NLEval.data.BioPlex(self.tmp_dir, reprocess=True)
        NLEval.data.BioPlex(self.tmp_dir, redownload=True)

    @unittest.skip("Sometimes DisGeNet is just not working...")
    def test_disgenet(self):
        lsc = NLEval.data.DisGeNet(self.tmp_dir)

    @pytest.mark.longruns
    def test_funcoup(self):
        graph = NLEval.data.FunCoup(self.tmp_dir)
        self.assertEqual(graph.size, 17783)
        self.assertEqual(graph.num_edges, 10027588)

    @unittest.skip("Need to fix issue with multiple annotated ontology.")
    def test_go(self):
        with self.subTest("GOBP"):
            lsc = NLEval.data.GOBP(self.tmp_dir)

        with self.subTest("GOCC"):
            lsc = NLEval.data.GOCC(self.tmp_dir)

        with self.subTest("GOMF"):
            lsc = NLEval.data.GOMF(self.tmp_dir)

    @pytest.mark.longruns
    def test_hippie(self):
        graph = NLEval.data.HIPPIE(self.tmp_dir)
        self.assertEqual(graph.size, 17955)
        self.assertEqual(graph.num_edges, 770754)

    @pytest.mark.longruns
    def test_humannet(self):
        graph = NLEval.data.HumanNet(self.tmp_dir)
        self.assertEqual(graph.size, 17787)
        self.assertEqual(graph.num_edges, 849002)

    @pytest.mark.longruns
    def test_string(self):
        graph = NLEval.data.STRING(self.tmp_dir)
        self.assertEqual(graph.size, 18513)
        self.assertEqual(graph.num_edges, 11038228)


if __name__ == "__main__":
    unittest.main()
