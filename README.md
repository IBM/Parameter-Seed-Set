# Parameter Seed Set 


This repository contains code and [supplementary material](./supp_material.pdf) for [Kokel et al. 2023](#citation).

> Planning tasks succinctly represent labeled transition systems, with 
each ground action corresponding to a label. This granularity, however, 
is not necessary for solving planning tasks and can be harmful, especially 
for model-free methods. In order to apply such methods, the label sets 
are often manually reduced. In this work, we propose automating this manual 
process. We characterize a valid} label reduction for classical planning 
tasks and propose an automated way of obtaining such valid reductions by 
leveraging lifted mutex groups. Our experiments show a significant reduction 
in the action label space size across a wide collection of planning domains. 
We demonstrate the benefit of our automated label reduction in two separate 
use cases: improved sample complexity of model-free reinforcement learning 
algorithms and speeding up successor generation in lifted planning. 


## Quick Start 

This code has been tested on `Ubuntu 20.04` and `RHEL 8.5` for Python `3.8`. 
It may not work on MacOS due to a [known issue in one of the dependencies](https://gitlab.com/danfis/cpddl/-/issues/1).

### 1. Clone this repo

```
git clone git@github.com:IBM/Parameter-Seed-Set.git
conda create -n pss python=3.8
conda activate pss
cd Parameter-Seed-Set
pip install -r requirement.txt
pip install -e .
```

### 2. Setup dependencies

This code makes system calls to the following libraries.

* [CPDDL](https://gitlab.com/harshakokel/cpddl.git) 
* [Forbid Iterative](https://github.com/IBM/forbiditerative.git) Planner  


:exclamation: If you already have CPDDL or a PDDL-based Planner, skip to step 3.

  Build CPDDL. Following packages are required for successful build `unzip automake autotools-dev`

    ```
    sudo apt-get install unzip automake autotools-dev
    git submodule update --init --recursive -- ./dependencies/cpddl
    cd ./dependencies/cpddl
    ./scripts/build.sh
    cd ../..
    ```

  Build ForbidIterative planner

    ```
    git submodule update --init --recursive -- ./dependencies/forbiditerative
    cd ./dependencies/forbiditerative
    python ./build.py
    cd ../..
    ```


### 3. Set environment variables

**Skip this part if the CPDDL and Planner were installed as part of step 2.** 

Otherwise, configure your respective path to `pddl-lifted-mgroups` and `fast-downward.py` by declaring following environment variables.

```
# For CPDDL Lifted Mutex Groups
export CPDDL_LMGS_PATH=./dependencies/cpddl/bin/pddl-lifted-mgroups
# For Fast Downward planner
export FAST_DOWNWARD_PATH=./dependencies/forbiditerative/fast-downward.py
```

### 4. Run the `runner.py` to find the parameter seed set and compare the action spaces.

```bash
$ python ./runner.py \
--domain-file ~/downward-benchmark/blocks.pddl \
--problem-dir ~/downward-benchmark/blocks \
--use-grounding
```

## Code organization

```bash
Repository
├── README.md                       # this file
├── LICENSE                        #  license file
├── pss/                           # contains core code
|  ├── util/                # utility files interfacing dependencies
|  ├── evaluation.py           # evaluation code
|  └── parameter_seed_set.py   # core formulation and solution.       
├── runner.py            # main runner file    
├── unittests/           # unit test cases
├── dependencies/        # git submodules
└── scripts/             # scripts to replicate empirical results
```


## Citation

If you build on this code or the ideas of this paper, please use the following citation.

    @inproceedings{KokelLKSS23,
     	title={Action Space Reduction for Planning Domains},
     	journal={IJCAI},
     	author={Kokel, Harsha and Lee, Junkyu and Katz, Michael and Srinivas, Kavitha and Sohrabi, Shirin},
     	year={2023}
    }

## LICENSE

This code is licensed under the [Eclipse Public License, Version 1.0 (EPL-1.0)](./LICENSE).
