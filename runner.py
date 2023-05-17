import argparse
import csv
import glob
import os
import sys
import gtimer as gt
from pss.parameter_seed_set import find_parameter_seed_sets
from pss.util.cpddl_util import get_LMG_atoms
from pss.evaluation import compare_action_spaces
from tarski.io import PDDLReader

argparser = argparse.ArgumentParser()

argparser.add_argument("--domain-file",
                     type=str,
                     required=True,
                     help="Domain file")

argparser.add_argument("--problem-dir",
                     type=str,
                     required=True,
                     help="Directory containing the problem files")

argparser.add_argument("--use-grounding",
                     action='store_true',
                     default=False,
                     help="Use fastdownward grounding to compare action spaces")

argparser.add_argument("--seed-set-csv",
                     type=str,
                     default="parameter_seeds.csv",
                     help="CSV file to write the seed sets")

argparser.add_argument("--reduction-csv",
                     type=str,
                     default="reduction.csv",
                     help="CSV file to write reduction statistics")

args = argparser.parse_args()


def results():
    path = os.environ.get("RESULTS","./results/")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def main():

    results_path = results()
    write_header = True
    seed_set_dict ={}
    seed_set_csv, reduction_csv = None, None
    for problem_file in gt.timed_for(sorted(glob.iglob(os.path.join(args.problem_dir, "*.pddl"))), save_itrs=True):
        if 'domain.pddl' in problem_file:
            continue
        print("\n\n\nStaring problem file:", problem_file)
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(args.domain_file)
        pddl_task = reader.parse_instance(problem_file)
        print(f"Domain: {pddl_task.domain_name}\n")
        gt.stamp("parsing pddl task", unique=False)
        if write_header:
            seed_set_dict = {"domain": "",
                     "task": "",
                     "problem file": "",
                     "action": "",
                     "parameters": "",
                     "seed set": "",
                     "# params": 0,
                     "# seeds": 0,
                     "plan":"",
                     "# plans": 0}

            seed_set_csv = open(results_path+pddl_task.domain_name+"_"+args.seed_set_csv, 'w', newline='')
            seed_set_writer = csv.DictWriter(seed_set_csv,
                                                fieldnames=list(seed_set_dict.keys()))
            seed_set_writer.writeheader()

            reduction_dict = {"domain": "",
                            "task": "",
                            "problem file": "",
                            "# grounded operators": 0,
                            "# reduced action labels": 0}
            reduction_csv = open(results_path+pddl_task.domain_name+"_"+args.reduction_csv, 'w', newline='')
            reduction_writer = csv.DictWriter(reduction_csv,
                                                fieldnames=list(reduction_dict.keys()))
            reduction_writer.writeheader()
            write_header = False
            gt.stamp("writing header", unique=False)

        # normalize.normalize(pddl_task)
        # gt.stamp("normalizing pddl task", unique=False)
        seed_set_dict['domain'] = pddl_task.domain_name
        seed_set_dict['task'] = pddl_task.name
        seed_set_dict['problem file'] = problem_file

        lifted_mutex_groups = get_LMG_atoms(args.domain_file, problem_file)
        gt.stamp("Getting Lifted Mutex Groups", unique=False)
        print("---Begin Lifted Mutex Groups---\n")
        format_row = "{:>30}" * (3)
        print(format_row.format("Predicate( signature )",  "fixed parameter indices", "counted parameter indices"))
        for lmg in lifted_mutex_groups:
            print(format_row.format(f"{lmg[0]}({lmg[1]})", str(lmg[2][0]), str(lmg[2][1])))
        print("\n---End Lifted Mutex Groups---\n")

        parameter_seeds, plans = find_parameter_seed_sets(pddl_task, lifted_mutex_groups,
                                                    writer=seed_set_writer,
                                                    write_file=seed_set_csv,
                                                    seed_set_dict=seed_set_dict)
        print("Found all seed sets.")
        gt.stamp("Found all seed sets", unique=False)


        reduction_dict['domain'] = pddl_task.domain_name
        reduction_dict['task'] = pddl_task.name
        reduction_dict['problem file'] = problem_file
        ground_operators_size, reduced_operator_size = compare_action_spaces(pddl_task, parameter_seeds, estimate=not args.use_grounding)
        gt.stamp("Evaluate Reduction", unique=False)
        print(f"In {problem_file} , Number of operators were reduced from {ground_operators_size} to {reduced_operator_size}")

        reduction_dict["# grounded operators"] = ground_operators_size
        reduction_dict[ "# reduced action labels"] = reduced_operator_size
        reduction_writer.writerow(reduction_dict)
        reduction_csv.flush()
    if seed_set_csv is not None:
        seed_set_csv.close()
    if reduction_csv is not None:
        reduction_csv.close()
    gt.stamp("Finished Run", unique=False)
    print(gt.report())
    print("Finished Run")

if __name__ == '__main__':
    main()
