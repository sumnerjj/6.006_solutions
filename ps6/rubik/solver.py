import rubik

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    left_checked = {}
    right_checked = {}
    left_current = {start: []}
    right_current = {end: []}
    left_new = {}
    right_new = {}
    left_depth = 0
    right_depth = 0

    while left_depth < 8:
        for x in left_current.keys():
            y = right_current.get(x, None)
            if y is not None:
                ans = left_current[x] + [ rubik.perm_inverse(move) for move in reversed(y) ]
                return ans
        for x in left_current.keys():
            for move in rubik.quarter_twists:
                r = rubik.perm_apply(move,x)
                if not left_checked.get(r, None) and not left_current.get(r, None):
                    left_new[r] = left_current[x] + [move]
            left_checked[x] = left_current[x]
        left_current = left_new
        left_new = {}
        left_depth += 1

    while right_depth < 8:
        for x in right_current.keys():
            y = left_current.get(x, None)
            if y is not None:
                ans = y + [ rubik.perm_inverse(move) for move in reversed(right_current[x]) ]
                return ans
        for x in right_current.keys():
            for move in rubik.quarter_twists:
                r = rubik.perm_apply(move,x)
                if not right_checked.get(r, None) and not right_current.get(r, None):
                    right_new[r] = right_current[x] + [move]
            right_checked[x] = right_current[x]
        right_current = right_new
        right_new = {}
        right_depth += 1

    return None

