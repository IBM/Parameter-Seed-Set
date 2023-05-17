import os
from subprocess import PIPE, Popen
import sys
from xml import dom

from .planner_util import print_error


if sys.version_info.major < 3:
    print("Require Python 3.6 or above")
    sys.exit()
lmg_kwargs = {"stdout": PIPE,
            "stderr": PIPE}
if sys.version_info.minor >= 7:
    lmg_kwargs['text']=True
else:
    lmg_kwargs['universal_newlines']=True


def lmgs_path():
    return os.environ.get("CPDDL_LMGS_PATH", "./dependencies/cpddl/bin/pddl-lifted-mgroups")

def call_cppdl_lmgs(domain_file, problem_file):
    process = Popen([lmgs_path(),"-q", "--disable-static",domain_file,problem_file], **lmg_kwargs)
    stdout, stderr = process.communicate()
    if process.wait() != 0 or len(str(stderr))>0:
        print_error(process.wait(), stdout, stderr)
        return False
    return str(stdout).split("\n")

def get_LMG_atoms(domain_file, problem_file, verbose=True):
    """Gets LMGs from CPDDL and splits it to single atom.
    This is justified as subset of LMG is an LMG."""
    lifted_mutex_groups = call_cppdl_lmgs(domain_file, problem_file)
    lmgs = []
    for m in lifted_mutex_groups:
        if m == '':
            continue
        atoms = m.split("{")[1].replace("}", "").split(",")
        lmgs += atoms
    lmg_atoms = set()
    pg_atoms = set() # partially grounded atoms
    for atom in lmgs:
        pg  = False
        a = atom.strip().split(" ")
        fixed, counting= set(), set()
        for i, v in enumerate(a[1:]):
            if v.startswith("C") and ":" in v:
                counting.add(i)
            elif v.startswith("V") and ":" in v:
                fixed.add(i)
            else:
                pg = True
                fixed.add(i)
        lmg= (a[0], tuple(a[1:]), (frozenset(fixed), frozenset(counting)))
        if not pg:
            lmg_atoms.add(lmg)
        else:
            pg_atoms.add(lmg)
    """Ignoring all the partially grounded LMGs,
    only returning completely lifted mutex groups."""
    if verbose:
        print("partially grounded mutex groups (ignored): {}\n".format(str(pg_atoms)))
    return list(lmg_atoms)
