import glob
import os
import sys
from subprocess import PIPE, Popen

DOMAIN_FILE = "domain.pddl"
PROBLEM_FILE = "problem.pddl"
PLAN_FILE = "plan.txt"

if sys.version_info.major < 3:
    print("Require Python 3.6 or above")
    sys.exit()
process_kwargs = {"stdout": PIPE,
            "stderr": PIPE}
if sys.version_info.minor >= 7:
    process_kwargs['text']=True
else:
    process_kwargs['universal_newlines']=True

def problem_path():
    path = os.environ.get("REDUCTION_PROBLEMS","./reduction_problems")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def solution_path():
    path = os.environ.get("REDUCTION_SOLUTIONS","./reduction_problems")
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path+"/fd"):
        os.makedirs(path+"/fd")
    return path

PROBLEM_PATH = problem_path()
SOLUTION_PATH = solution_path()

def downward_path():
    return os.environ.get("FAST_DOWNWARD_PATH", "./dependencies/forbiditerative/fast-downward.py")

def print_error(code, stdout, stderr):
    print("There were some errors")
    print("============================")
    print("returncode: ", code)
    print("ERROR:")
    print(stderr)
    print("OUTPUT: ")
    print(stdout)
    print("============================")

def call_fast_downward(domain_file, problem_file, plan_file):
    process = Popen([downward_path(),"--plan-file", plan_file,
                    domain_file, problem_file, "--search", "astar(lmcut())"], **process_kwargs)
    stdout, stderr = process.communicate()
    if process.wait() != 0 or str(stderr) != '':
        print_error(process.wait(),stdout,stderr)
        return False
    return plan_file

def get_plan(reduction_domain, reduction_problem, domain, action):
    domain_file = f"{PROBLEM_PATH}/{domain}_{action}_{DOMAIN_FILE}"
    problem_file = f"{PROBLEM_PATH}/{domain}_{action}_{PROBLEM_FILE}"
    dfile = open(domain_file, "w")
    dfile.write(reduction_domain)
    pfile = open(problem_file, "w")
    pfile.write(reduction_problem)
    dfile.close()
    pfile.close()
    return call_fast_downward(domain_file,
                        problem_file,
                        f"{SOLUTION_PATH}/fd/{PLAN_FILE}")
