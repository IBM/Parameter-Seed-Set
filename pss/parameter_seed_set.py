import re, sys

import numpy as np
import gtimer as gt

from tarski.syntax.formulas import Connective, is_atom, CompoundFormula, unwrap_conjunction_or_atom
from tarski.syntax.builtins import BuiltinPredicateSymbol, is_builtin_function, is_builtin_predicate
from .util.cpddl_util import get_LMG_atoms
from .util.templates import *
from .util.planner_util import get_plan



def is_relevant(action, lmg_atom, precondition, pddl_task):
    if lmg_atom[0] != precondition.predicate.name:
            return False
    for pre_arg, lmg_param in zip(precondition.subterms, lmg_atom[1]):
        lmg_param_type = pddl_task.language.get_sort(lmg_param.split(":")[1]) #Assuming all LMGs are lifted.
        if lmg_param_type != pre_arg.sort and lmg_param_type not in pddl_task.language.ancestor_sorts[pre_arg.sort]:
            return False
    return True

def get_hyperedges(action, lmg_atoms, pddl_task):
    preconditions = unwrap_conjunction_or_atom(action.precondition)

    
    hyperedge = [ set() for _ in action.parameters]
    for precondition_index, precondition in enumerate(preconditions):
        if  type(precondition) == CompoundFormula or is_builtin_predicate( precondition.predicate) or is_builtin_function(precondition.predicate):
            continue
        for lmg_index, lmg_atom in enumerate(lmg_atoms):
            if is_relevant(action, lmg_atom, precondition, pddl_task):
                fixed_indexes, counting_indexes = lmg_atom[2]
                fixed = [action.parameters.index_[precondition.subterms[i].symbol] for i in fixed_indexes if '?'  in precondition.subterms[i].symbol ]
                for i in counting_indexes:
                    if '?'  in precondition.subterms[i].symbol:
                        hyperedge[action.parameters.index_[precondition.subterms[i].symbol]].add((f"{lmg_index}_{precondition_index}_{i}", tuple(fixed)))
    return hyperedge

def get_costs(counts):
    if len(counts)<=1:
        return counts
    count_values = np.array([x for x in counts if x != 0])
    diff_array = np.diff(np.sort(np.log(count_values)))
    diff_array = diff_array[diff_array > 0]
    if len(diff_array)>1:
        diff = diff_array.min()
    else:
        return counts
    return np.round(counts / diff)

def generate_planning_problem(action, lmg_atoms, pddl_task):
    """ Generate planning problem """
    objects = " ".join([f"x{i}" for i, v in enumerate(action.parameters)])
    goal = " ".join([f"(mark x{i})" for i, v in enumerate(action.parameters)])

    hyperedge = get_hyperedges(action, lmg_atoms, pddl_task)

    operators = []
    index=0
    cost = get_costs([len(param.sort._domain) for param in action.parameters])
    for i, param in enumerate(action.parameters):
        operators.append(SEED_TEMPLATE.format(parameter=f"x{i}",comment=f"parameter `{i}' of type "+
                            f"`{param.sort.name}' with `{len(param.sort._domain)}' objects",
                                              cost=cost[i]))
        i_operators = []
        for edge_label, required_parameters  in hyperedge[i]:
            if len(required_parameters) == 0:
                i_operators= [GET_TEMPLATE.format(index=f"{index}_{i}_{edge_label}",requires=" ",achieve=f"x{i}",
                                       comment=edge_label)]
                index += 1
                break
            requires = ' '.join([f"(mark x{j})\n" for j in required_parameters])
            i_operators.append(GET_TEMPLATE.format(index=f"{index}_{i}_{edge_label}",requires=requires,achieve=f"x{i}",comment=edge_label))
            index += 1
        operators += i_operators
    domain_txt = DOMAIN_TEMPLATE.format(aname=action.name, objects=objects, operators="".join(operators))
    problem_txt = PROBLEM_TEMPLATE.format(aname=action.name,goal=goal)
    return domain_txt, problem_txt

def read_plan(plan_file, lmg_atoms):
    reader = open(plan_file)
    plan = reader.read().split("\n")
    r_params = []
    info = {}
    for p in plan[:-2]:
        if p.startswith("(seed"):
            r_params.append(int(re.search("[0-9]+", p).group(0)))
        else:
            _, parameter_index, lmg_index, precondition_index, arg_index = p.replace(")","").strip().split("_")
            fixed_args, counting_args = lmg_atoms[int(lmg_index)][2]
            info[int(parameter_index)] = (int(precondition_index), int(arg_index), len(fixed_args))+tuple(fixed_args)
    r_params.sort()
    reader.close()
    return r_params, info


def find_parameter_seed_set(action, lmg_atoms, pddl_task):
    """Solves the parameter seed set problem.
    We first generate a planning problem for the given action
    and Lifted Mutex groups, and then solve the planning problem
    using a planner. The plan obtained from the planner provides
    the seed set.

    We use two different approaches to obtain the parameter seed set.
    One is to use Fast Downward planner to return smallest possible seed set
    Second is to use TopK planner to get all the plans and use a count approximation to
    estimate the best seed set.

    Refer Kokel et al. 2022 PRL@ICAPS for further details.
    """
    if len(action.parameters) == 0:
        # If action does not have any parameter, return empty list
        return []
    domain_txt, problem_txt = generate_planning_problem(action, lmg_atoms, pddl_task)
    parameter_seeds = []
    final_info = []
    plan_files = []
    # Find smallest possible seed set using Fast Downward
    plan_file = get_plan(domain_txt, problem_txt, pddl_task.domain_name,
            action.name)
    parameter_seeds, final_info = read_plan(plan_file, lmg_atoms)
    plan_files.append(plan_file)
    return parameter_seeds, final_info, plan_files



def find_parameter_seed_sets(pddl_task, lifted_mutex_groups, 
                           writer=None, write_file=None, seed_set_dict={}, verbose=True):
    """
    `type_predicate_list` is an optional field. It is a domain dependent list of predicates that
    represents type of objects.
    For example, [gripper, ball, room] for domain with (gripper g1) (room r1) etc.
    Current experiments assume typed PDDL files, and don't use this field
    """
    parameter_seeds, info = {}, {}
    if verbose:
            print("Finding parameter seed sets.\n")
    if verbose:
        print("---Begin Parameter Seed Set---")
        format_row = "{:>20} {:>30} {:>40}    {:<40}"
        print(format_row.format("Action", "seed set indices", "parameters", "plan", "# plans"))
    for _, action in pddl_task.actions.items():
        if len(action.parameters) == 0:
            if verbose:
                print(f"Skipping the action {action.name} with zero parameters.")
            parameter_seeds[action.name] = []
            continue
        parameter_seeds[action.name], info[action.name], plans = find_parameter_seed_set(action, lifted_mutex_groups, pddl_task)

        gt.stamp(f"Found {action.name} seed sets", unique=False)
        if verbose:
            print("Action name: ", action.name)
            print("Non seed info")
            # for index, param_info in info[action.name].items():
            #     print(f"Parameter {index}:{action.parameters[index]}")
            #     print(f"can be infered from precondition {param_info[0]}:{action.precondition.subterms[param_info[0]]} as counting argument {param_info[1]}")
            print(format_row.format(action.name,  str(parameter_seeds[action.name]),str(action.parameters),str(info[action.name]), str(len(plans))))
        if writer is not None:
            seed_set_dict['action'] = action.name
            seed_set_dict['parameters'] =  str(action.parameters)
            seed_set_dict['seed set'] =  str(parameter_seeds[action.name])
            seed_set_dict['# params'] =  len(action.parameters)
            seed_set_dict['# seeds'] =  len(parameter_seeds[action.name])
            seed_set_dict['plan'] =  str(info[action.name])
            seed_set_dict['# plans'] =  len(plans)
            writer.writerow(seed_set_dict)
            if write_file is not None:
                write_file.flush()
    if verbose:
        print("\n---End Parameter Seed Set---\n")
    return parameter_seeds, info


def get_parameter_seed(domain_file, problem_file, pddl_task, use_count_approximation=False, verbose=False):
    lifted_mutex_groups = get_LMG_atoms(domain_file, problem_file, verbose=verbose)
    return find_parameter_seed_sets(pddl_task, lifted_mutex_groups, use_count_approximation=use_count_approximation, verbose=verbose)
