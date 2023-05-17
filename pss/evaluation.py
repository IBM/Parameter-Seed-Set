from tarski.grounding import LPGroundingStrategy
import gtimer as gt

def compare_action_spaces(pddl_task, parameter_seeds, estimate=True):
    print("Comparing action spaces.\n")
    if not estimate:
        # Compare reduction
        print("--- Begin PDDL to SAS grounding ---")
        grounder = LPGroundingStrategy(pddl_task)
        print("\n--- End PDDL to SAS grounding ---\n")
        gt.stamp("PDDL to SAS grounding", unique=False)
        reduced_action_labels = set()
        ground_operator_count = 0
        for a, groundings in grounder.ground_actions().items():
            ground_operator_count += len(groundings)
            for o in groundings:
                reduced_operator = [a] + [ o[i] for i in parameter_seeds[a]]
                reduced_action_labels.add("_".join(reduced_operator))
        return ground_operator_count, len(reduced_action_labels)
    else:
        n_operators, n_reduced_operators = 0, 0
        for  _ , action in pddl_task.actions.items():
            seed_count, operator_count = 1, 1
            seeds = parameter_seeds[action.name]
            for i, param in enumerate(action.parameters):
                count = len(param.sort._domain)
                if count == 0:
                    seed_count = 0
                    operator_count = 0
                    break
                if i in seeds:
                    seed_count = seed_count * count
                operator_count = operator_count * count
            n_operators += operator_count
            n_reduced_operators += seed_count
        return n_operators, n_reduced_operators
