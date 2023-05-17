from collections import defaultdict
import io
import unittest

from pss.parameter_seed_set import find_parameter_seed_set, read_plan
from tarski.io import PDDLReader


class TestPlannerUtil(unittest.TestCase):


    def test_parameter_seed_set_blocks(self):
        domain_file = "./unittests/sample_pddl_files/blocks_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/blocks_problem-10-0.pddl"
        lifted_mutex_groups = [('handempty', (), (frozenset(), frozenset())),
            ('holding', tuple(['C0:object']), (frozenset(), frozenset([0]))),
            ('on', tuple(['V0:object', 'C1:object']), (frozenset([0]), frozenset([1]))),
            ('ontable', tuple(['V0:object']), (frozenset([0]), frozenset([]))),
            ('holding', tuple(['V0:object']), (frozenset([0]), frozenset([]))),
            ('on', tuple(['C1:object', 'V0:object']), (frozenset([1]), frozenset([0]))),
            ('clear', tuple(['V0:object']), (frozenset([0]), frozenset([])))]
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain_file)
        pddl_task = reader.parse_instance(problem_file)
        action = pddl_task.actions['pick-up']
        seed_set, _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[0])
        action= pddl_task.actions['put-down'] #pickup
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups,  pddl_task)
        self.assertListEqual(seed_set,[])
        action= pddl_task.actions['stack'] #stack
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['unstack'] #unstack
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[0])

    def test_parameter_seed_set_elevators(self):
        domain_file = "./unittests/sample_pddl_files/elevators_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/elevators_problem-s28-1.pddl"
        lifted_mutex_groups = [('destin', ('V0:passenger', 'C1:floor'), (frozenset({0}), frozenset({1}))),
         ('above', ('V0:floor', 'V1:floor'), (frozenset({0, 1}), frozenset())),
         ('lift-at', ('C0:floor',), (frozenset(), frozenset({0}))),
         ('destin', ('V0:passenger', 'V1:floor'), (frozenset({0, 1}), frozenset())),
         ('origin', ('V0:passenger', 'C1:floor'), (frozenset({0}), frozenset({1}))),
         ('origin', ('V0:passenger', 'V1:floor'), (frozenset({0, 1}), frozenset()))]
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain_file)
        pddl_task = reader.parse_instance(problem_file)
        action = pddl_task.actions['board'] #board
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['depart'] #depart
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['up'] #up
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['down'] #down
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])

        type_count_map =  {'Object': 87, 'passenger': 29, 'floor': 58}
        action = pddl_task.actions['board'] #board
        parameter_type_map = {'?f': 'floor', '?p': 'passenger'}
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['depart'] #depart
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['up'] #up
        parameter_type_map = {'?f1': 'floor', '?f2': 'floor'}
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])
        action= pddl_task.actions['down'] #down
        seed_set,  _, _ = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)
        self.assertListEqual(seed_set,[1])

