

#Task 1 Decoding Attributes(2.45/3marks)

def zbini_attrs(type_id):
    hair_hat=["wavy", "curly", "beanie", "cap"]
    colour=["red", "blue", "yellow", "green"]
    accessory=["sneakers", "bowtie", "sunglasses", "scarf"]
    social=["tiktok", "instagram", "discord", "snapchat"]
    # list all possible values for each attribute 
    hindex=int(type_id) // 4 ** 3 % 4 
    cindex=int(type_id) // 4 ** 2 % 4
    aindex=int(type_id) // 4 % 4
    sindex=int(type_id) % 4
    # index of each attribute 
    if not 0<=int(type_id)<255:
        return None 
        # the range of type_id
    else:
        return(hair_hat[hindex], colour[cindex],\
               accessory[aindex], social[sindex])
    
#Task 2 Checking group validity(2.02 marks)

def valid_study_group(zbinis, group):
    members=[]
    type_id=[]
    common_subjects=set()
    if len(group) !=3 and len(group) != 4:
        return(False, None)
    # A valid group can only have either 3 or 4 members
    for i in group:
        if i not in members:
            members.append(zbinis[i])  # finding all members
        else:
            return(False, None)
    for member in members:
        type_id.append(member[0]) 
        # finding type_id
    if len(set(type_id))!=len(type_id):
        return(False, None)
    # make suere differnt type_id of each member in group
    for member in members:
        if not common_subjects:
            common_subjects=set(member[1])
        else:
            common_subjects &= set(member[1])
            # finding common_subjects
    if not common_subjects:
        return (False, None)
    else:
        return(True, len(common_subjects))
    
#Task 3 Possible study groups (4/4marks)
    
from itertools import combinations

def possible_study_groups(zbinis):
    valid_score=[]
    for group_size in [3, 4]:
        for group_possible in combinations(range(len(zbinis)), group_size):
            # listing all possible group
            if valid_study_group(zbinis, group_possible)[0]:
                # checking whether it is True of False
                common_subjects=valid_study_group(zbinis, group_possible)[1]
                # finding common_subjects
                score= int(common_subjects) * 3 + (len(group_possible) - 2)
    # adding three points for each subject shared by all members of the group
    # Add one point if the group has three members, 
    # or two points if the group has four members.
                valid_score.append((group_possible, score))
                valid_score.sort(key=lambda x: (-x[1], x[0]))
            # sorting valid_score
    return valid_score


#Task 4 Allocating study groups(2.6/5 marks)
'''To be honest, When i was working on task4, i didn't finish this one cuz some bugs :( So i put sample solutions here'''

def remove_overlapping(group, groups):
    """
    Given a `group` and a list of `groups` represented as (group, score)
    tuples, return only the groups (as a list of tuples of the same form) that
    do not have any indices in common with `group`.
    """
    return [(g, s) for g, s in groups if not g & group]


def find_optimal_grouping(groups, num_zbinis):
    """
    Given a list of possible `groups`, each represented as a (group, score)
    tuple where `group` is a set of indices and `score` is a precomputed group
    score, as well as the `num_zbinis` that are yet to be allocated to a group,
    this function recursively computes and returns a tuple of two values:

     -- a list of groups that minimises the number of Zoomerbinis that are
        not allocated to a group (that is, an "optimal grouping"), and;

     -- a "ranking metric", which in itself is a tuple of two values 
        (-num_remaining, combined_score) where `num_remaining` is the number of
        Zoomerbinis that are not allocated to a group after selecting the
        optimal grouping, and `combined_score` is the sum of the scores of the
        groups in the optimal grouping.
        
        The negation of `num_remaining` ensures that the number of remaining
        Zoomerbinis is minimised, and the combined score is used as a secondary
        tiebreaker in the case there are multiple optimal groupings.
            
    Note that the ranking metric tuple is used to determine the optimal group
    selection as part of the recursive call chain and isn't needed in the final
    result. See the `alloc_study_groups` function for more details.
    """
    if len(groups) == 0:
        return [], (-num_zbinis, 0)
    
    best_rank = (-num_zbinis, 0)
    best = []
    for group, group_score in groups:
        rem_groups = remove_overlapping(group, groups)
        rem_groups, (rem_num_zbinis, rem_score) = \
            find_optimal_grouping(rem_groups, num_zbinis - len(group))
        
        curr_rank = (rem_num_zbinis, rem_score + group_score)

        if curr_rank > best_rank:
            best_rank = curr_rank
            best = [(group, group_score)] + rem_groups
        
    return best, best_rank


def alloc_study_groups(zbinis):
    """
    Given a list of Zoomerbinis `zbinis`, each represented as a (type_id,
    subjects) tuple, return a list of tuples representing the optimal grouping
    of Zoomerbinis.

    This approach uses a "brute force" approach to find the optimal grouping by
    computing all possible valid study groups and then recursively selecting
    the optimal grouping based on the ranking metrics defined in the task.
    """
    possible_groups = [
        (set(group), score)
        for group, score in possible_study_groups(zbinis)
    ]

    optimal_grouping, _ = find_optimal_grouping(possible_groups, len(zbinis))

    return [tuple(sorted(group)) for group, _ in optimal_grouping]


