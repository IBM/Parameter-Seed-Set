---
layout: default
title: Action Space Reduction for Planning Domains
---
# Abstract

Planning tasks succinctly represent labeled transition systems, with each ground action corresponding to a label. This granularity, however, is not necessary for solving planning tasks and can be harmful, especially for model-free methods. In order to apply such methods, the label sets are often manually reduced. In this work, we propose automating this manual process. We characterize a valid label reduction for classical planning tasks and propose an automated way of obtaining such valid reductions by leveraging lifted mutex groups. Our experiments show a significant reduction in the action label space size across a wide collection of planning domains. We demonstrate the benefit of our automated label reduction in two separate use cases 1. improved sample complexity of model-free reinforcement learning algorithms and 2. speeding up successor generation in lifted planning. 


## Code 

The code for identifying parameter seed sets is available [here](https://github.com/IBM/Parameter-Seed-Set). Additionally, the code to use the parameter seeds in Powerlifted, a lifted successor generator, is available [here](https://github.com/IBM/Powerlifted-PSS).


## Citation

If you build on this code or the ideas of this paper, please use the following citation.

    @inproceedings{KokelLKSS23,
     	title={Action Space Reduction for Planning Domains},
     	journal={IJCAI},
     	author={Kokel, Harsha and Lee, Junkyu and Katz, Michael and Srinivas, Kavitha and Sohrabi, Shirin},
     	year={2023}
    }

## LICENSE

This code is licensed under the [Eclipse Public License, Version 1.0 (EPL-1.0)](../LICENSE).
