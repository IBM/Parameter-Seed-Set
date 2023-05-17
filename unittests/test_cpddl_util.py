import unittest

from pss.util.cpddl_util import call_cppdl_lmgs, get_LMG_atoms


class TestCPDDLUtil(unittest.TestCase):

    def test_call_cpddl_lmg(self):
        domain_file = "./unittests/sample_pddl_files/blocks_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/blocks_problem-10-0.pddl"
        lmgs = call_cppdl_lmgs(domain_file,problem_file)
        self.assertNotEqual(lmgs, False)

    def test_call_cpddl_lmg_htg(self):
        domain_file = "/home/hk/planning.domains/htg-domains/visitall-multidimensional/3-dim-visitall-CLOSE-g1/domain.pddl"
        problem_file = "/home/hk/planning.domains/htg-domains/visitall-multidimensional/3-dim-visitall-CLOSE-g1/p0.pddl"
        lmgs = call_cppdl_lmgs(domain_file,problem_file)
        self.assertNotEqual(lmgs, False)

    def test_get_LMG_atoms_blocks(self):
        domain_file = "./unittests/sample_pddl_files/blocks_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/blocks_problem-10-0.pddl"
        expected_lmgs = {('handempty', (), (frozenset(), frozenset())),
            ('holding', tuple(['C0:object']), (frozenset(), frozenset([0]))),
            ('on', tuple(['V0:object', 'C1:object']), (frozenset([0]), frozenset([1]))),
            ('ontable', tuple(['V0:object']), (frozenset([0]), frozenset([]))),
            ('holding', tuple(['V0:object']), (frozenset([0]), frozenset([]))),
            ('on', tuple(['C1:object', 'V0:object']), (frozenset([1]), frozenset([0]))),
            ('clear', tuple(['V0:object']), (frozenset([0]), frozenset([])))}
        lmgs = get_LMG_atoms(domain_file, problem_file)
        self.assertSetEqual(expected_lmgs, set(lmgs))

    def test_get_LMG_atoms_elevators(self):
        domain_file = "./unittests/sample_pddl_files/elevators_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/elevators_problem-s28-3.pddl"
        expected_lmgs = {('destin', ('V0:passenger', 'C1:floor'), (frozenset({0}), frozenset({1}))),
                ('above', ('V0:floor', 'V1:floor'), (frozenset({0, 1}), frozenset())),
                ('lift-at', ('C0:floor',), (frozenset(), frozenset({0}))),
                ('destin', ('V0:passenger', 'V1:floor'), (frozenset({0, 1}), frozenset())),
                ('origin', ('V0:passenger', 'C1:floor'), (frozenset({0}), frozenset({1}))),
                ('origin', ('V0:passenger', 'V1:floor'), (frozenset({0, 1}), frozenset()))}
        lmgs = get_LMG_atoms(domain_file, problem_file)
        self.assertSetEqual(expected_lmgs, set(lmgs))