import io
import unittest

from pss.util.planner_util import call_fast_downward,  get_plan


class TestPlannerUtil(unittest.TestCase):

    def test_call_fast_downward_sanity(self):
        """Test Fast Downward does not return error"""
        domain_file = "./unittests/sample_pddl_files/blocks_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/blocks_problem-4-0.pddl"
        plan_file = "./temp_blocks_plan.plan"
        plan_file_returned = call_fast_downward(domain_file, problem_file, plan_file)
        self.assertNotEqual(plan_file_returned, False)

    def test_call_fast_downward_plan(self):
        """Test Fast Downward does not return error"""
        domain_file = "./unittests/sample_pddl_files/blocks_domain.pddl"
        problem_file = "./unittests/sample_pddl_files/blocks_problem-4-0.pddl"
        expected_plan_file = "./unittests/sample_pddl_files/blocks_solution-4-0.plan"
        plan_file = "./temp_blocks_plan.plan"
        plan_file_returned = call_fast_downward(domain_file, problem_file, plan_file)
        self.assertListEqual(
                    list(io.open(expected_plan_file)),
                    list(io.open(plan_file_returned)))

    def test_get_plan(self):
        """Verify if the parameter seed set problem can be solved by fast downward"""
        domain = "(define (domain unstack-domain) \n \
                    (:constants x0 x1	)\n \
                    (:predicates (mark ?o)  	) \n \
                    (:functions  	(total-cost) - number  	)\n \
                    (:action seed  \n \
                        :parameters (?o) \n \
                        :precondition (not (mark ?o)) \n \
                        :effect (and (mark ?o) (increase (total-cost) 100))  	)\n \
                    (:action get0 	\n \
                        :parameters () \n \
                        :precondition (and (mark x1) ( not (mark x0)))\n \
                        :effect (and (mark x0) \n \
                                (increase (total-cost) 1)) )\n \
                    (:action get1    \n \
                        :parameters () \n \
                        :precondition (and (mark x0) ( not (mark x1)))\n \
                        :effect (and (mark x1) (increase (total-cost) 1)) 	))"
        problem = "(define (problem unstack) \n \
            (:domain unstack-domain) \n \
            (:init (= (total-cost) 0)) \n \
            (:goal (and (mark x0) (mark x1) ) ) \n \
            (:metric minimize (total-cost))  )"
        expected_plan = ["(seed x0)\n",'(get1 )\n', '; cost = 101 (general cost)\n']
        plan_file_returned = get_plan(domain, problem, "blocks", "unstack")
        self.assertListEqual(
                    expected_plan,
                    list(io.open(plan_file_returned)))

        """Verify if the parameter seed set problem can be solved by fast downward"""
        domain = "(define (domain pick-up-domain)\n     (:constants \n \tx0\n \t) \n    \
             (:predicates \n \t(mark ?o) \n \t) \n     (:functions \n \t(total-cost) - number \n \t)\n   \
                  (:action seed \n \t:parameters (?o) \n \t:precondition (not (mark ?o)) \n       \
                     \t:effect (and (mark ?o)\n \t\t(increase (total-cost) 100)) \n \t)\n\n )\n"
        problem = "(define (problem pick-up)\n         (:domain pick-up-domain)\n     \
                (:init (= (total-cost) 0))\n         (:goal\n             (and (mark x0) )\n     \
                        )\n         (:metric minimize (total-cost))\n     )\n"
        expected_plan = ['(seed x0)\n', '; cost = 100 (general cost)\n']
        plan_file_returned = get_plan(domain, problem, "test_get_plan_2", "pick-up")
        self.assertListEqual(
                    expected_plan,
                    list(io.open(plan_file_returned)))

        """Verify if the parameter seed set problem can be solved by fast downward"""
        domain = "(define (domain put-down-domain)\n     (:constants \n \tx0\n \t) \n   \
              (:predicates \n \t(mark ?o) \n \t) \n     (:functions \n \t(total-cost) - number \n \t)\n  \
                (:action seed \n \t:parameters (?o) \n \t:precondition (not (mark ?o)) \n    \
                \t:effect (and (mark ?o)\n \t\t(increase (total-cost) 100)) \n \t)\n   \
                (:action get0 \n         \t:parameters ()\n         \t; holding\n      \
                \t:precondition (and  \n         \t \t \t ( not (mark x0)))\n     \
                \t:effect (and (mark x0)\n         \t \t \t(increase (total-cost) 1))\n \t)\n\n )\n"
        problem = "(define (problem put-down)\n         (:domain put-down-domain)\n       \
              (:init (= (total-cost) 0))\n         (:goal\n             (and (mark x0) )\n     \
                    )\n         (:metric minimize (total-cost))\n     )\n"
        expected_plan = ['(get0 )\n', '; cost = 1 (general cost)\n']
        plan_file_returned = get_plan(domain, problem, "test_get_plan_3", "unstack")
        self.assertListEqual(
                    expected_plan,
                    list(io.open(plan_file_returned)))

        """Verify if the parameter seed set problem can be solved by fast downward"""
        domain = "(define (domain pick-up-domain)\n     (:constants \n \tx0\n \t) \n    \
             (:predicates \n \t(mark ?o) \n \t) \n     (:functions \n \t(total-cost) - number \n \t)\n   \
                  (:action seed \n \t:parameters (?o) \n \t:precondition (not (mark ?o)) \n       \
                     \t:effect (and (mark ?o)\n \t\t(increase (total-cost) 100)) \n \t)\n\n )\n"
        problem = "(define (problem pick-up)\n         (:domain pick-up-domain)\n     \
                (:init (= (total-cost) 0))\n         (:goal\n             (and (mark x0) )\n     \
                        )\n         (:metric minimize (total-cost))\n     )\n"
        expected_plan = ['(seed x0)\n', '; cost = 100 (general cost)\n']
        plan_file_returned = get_plan(domain, problem, "test_get_plan_4", "pick-up")
        self.assertListEqual(
                    expected_plan,
                    list(io.open(plan_file_returned)))


        """Verify if the parameter seed set problem can be solved by fast downward"""
        domain = "(define (domain stack-domain)\n     (:constants \n \tx0 x1\n \t) \n   \
              (:predicates \n \t(mark ?o) \n \t) \n     (:functions \n \t(total-cost) - number \n \t)\n  \
            (:action seed \n \t:parameters (?o) \n \t:precondition (not (mark ?o)) \n       \
                 \t:effect (and (mark ?o)\n \t\t(increase (total-cost) 100)) \n \t)\n     (:action get0 \n  \
                \t:parameters ()\n         \t; holding\n         \t:precondition (and  \n       \
                \t \t \t ( not (mark x0)))\n         \t:effect (and (mark x0)\n         \t \t \t(increase \
                (total-cost) 1))\n \t)\n\n )\n"
        problem = "(define (problem stack)\n         (:domain stack-domain)\n       \
              (:init (= (total-cost) 0))\n         (:goal\n             (and (mark x0) (mark x1) )\n   \
                      )\n         (:metric minimize (total-cost))\n     )\n"
        expected_plan = ['(seed x1)\n', '(get0 )\n', '; cost = 101 (general cost)\n']
        plan_file_returned = get_plan(domain, problem, "test_get_plan_5", "stack")
        self.assertListEqual(
                    expected_plan,
                    list(io.open(plan_file_returned)))

