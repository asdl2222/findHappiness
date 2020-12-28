import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_array_to_dict, calculate_happiness_for_room, calculate_stress_for_room
import sys
import random


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    max_groups = []
    max_happiness = 0

    for group_size in range(1, 11):
        nodes = list(G.nodes())
        groups = []
        max_bucket_size = s / group_size

        while len(groups) < group_size and nodes:
            ### (1) we can change how we select the first element in group for diversity.
            group = [nodes.pop(0)]
            ###group = [nodes.pop(random.randrange(len(nodes)))]
            groupStress = 0
            totalStress = 0
            while True:

                # in each iteration, find the greedy node to add to the group
                maxHappinessRatio = 0
                maxHappinessRatioStress = 0
                maxHappinessNode = None

                # find the greedy node ### (2) we can change how we select the greedy node
                for node in nodes:
                    additionalHappiness = 0
                    additionalStress = 0

                    for groupNode in group:
                        edge = G.get_edge_data(node, groupNode)
                        additionalHappiness += edge['happiness']
                        additionalStress += edge['stress']

                    if totalStress + additionalStress <= max_bucket_size:
                        additionalRatio = additionalHappiness / (additionalStress or 1)
                        if additionalRatio > maxHappinessRatio:
                            maxHappinessRatio, maxHappinessRatioStress, maxHappinessNode = additionalRatio, additionalStress, node

                if not maxHappinessNode: break
                group.append(maxHappinessNode)
                nodes.remove(maxHappinessNode)
                totalStress += maxHappinessRatioStress
            groups.append(group)
        if not nodes:
            groupLength = len(groups)
            max_bucket_size = s / groupLength

            # Do this until we cannot change anymore
            while True:
                modified = False

                # see if I can move a node to generate higher happiness

                # if not modified: break # ADD BREAK AND REMOVE BREAK <> TWO TYPES
                # TODO: add a condition where swapping is possible...
                for group in groups:
                    nodeIndex = 0
                    while nodeIndex < len(group):
                        groupElem = group[nodeIndex]

                        for changingGroup in groups:
                            if group == changingGroup: continue
                            changingNodeIndex = 0
                            while changingNodeIndex < len(changingGroup):
                                happinessGroupBefore = calculate_happiness_for_room(group, G)
                                happinessChangingGroupBefore = calculate_happiness_for_room(changingGroup, G)

                                group[nodeIndex], changingGroup[changingNodeIndex] = changingGroup[changingNodeIndex], group[nodeIndex]
                                happinessGroupAfter = calculate_happiness_for_room(group, G)
                                stressGroupAfter = calculate_stress_for_room(group, G)
                                happinessChangingGroupAfter = calculate_happiness_for_room(changingGroup, G)
                                stressChangingGroupAfter = calculate_stress_for_room(changingGroup, G)

                                if stressGroupAfter <= max_bucket_size and stressChangingGroupAfter <= max_bucket_size and (happinessChangingGroupAfter - happinessChangingGroupBefore + happinessGroupAfter - happinessGroupBefore) > 0.000000001:
                                    modified = True
                                    break
                                else:
                                    group[nodeIndex], changingGroup[changingNodeIndex] = changingGroup[changingNodeIndex], group[nodeIndex]
                                changingNodeIndex += 1
                        nodeIndex += 1

                for group in groups:
                    happinessInCurrentGroup = calculate_happiness_for_room(group, G)
                    stressInCurrentGroup = calculate_stress_for_room(group, G)
                    nodeIndex = 0
                    while nodeIndex < len(group):
                        groupElem = group[nodeIndex]
                        group.pop(nodeIndex)
                        happinessWithoutGroupElem = calculate_happiness_for_room(group, G)
                        groupChanged = False

                        for changingGroup in groups:
                            if group == changingGroup: continue
                            happinessBeforeChangingGroup = calculate_happiness_for_room(changingGroup, G)
                            changingGroup.append(groupElem)
                            stressInChangingGroup = calculate_stress_for_room(changingGroup, G)
                            happinessInChangingGroup = calculate_happiness_for_room(changingGroup, G)

                            if stressInChangingGroup <= max_bucket_size and happinessInChangingGroup - happinessBeforeChangingGroup > happinessInCurrentGroup - happinessWithoutGroupElem:
                                modified = True
                                groupChanged = True
                                happinessInCurrentGroup = happinessWithoutGroupElem
                                stressInCurrentGroup = calculate_stress_for_room(group, G)
                                break
                            else:
                                changingGroup.pop()
                                nodeIndex += 1
                        if not groupChanged:
                            group.insert(nodeIndex, groupElem)
                            nodeIndex += 1
                if not modified: break


            new_happiness = calculate_happiness(convert_array_to_dict(groups), G)
            if new_happiness > max_happiness:
                max_happiness = new_happiness
                max_groups = groups
        print('agroy', group_size)

    return convert_array_to_dict(max_groups)
