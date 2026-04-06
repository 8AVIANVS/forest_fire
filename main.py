import numpy as np

OFFSET = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def fire_count(world, r, c, r_world, c_world):  
    count = 0  
    nbhd = [(r + dr, c + dc) for (dr, dc) in OFFSET if 0 <= r + dr < r_world and 0 <= c + dc < c_world]
    for (nr, nc) in nbhd:
        if world[nr][nc] == -20:
            count += 1
    return count


def step(world, p): 
    out = world.copy()
    row_world = world.shape[0]
    col_world = world.shape[1]
    for row in range(row_world):
        for col in range(col_world):
            if world[row][col] == -20: # burning case
                out[row][col] = 2
            elif world[row][col] == 2: # ash case
                out[row][col] = 0
            elif world[row][col] == 0: # empty case
                if np.random.rand() < p:
                    out[row][col] = 1
            elif world[row][col] == 1: # tree case
                if fire_count(world, row, col, row_world, col_world) > 0:
                    out[row][col] = -20
    return out

# -------------------- test or test related --------------------

def build_world():
    out= np.zeros((5, 5))
    out[[1, 1], [1, 2]] = 1
    out[2][2] = -20
    out[3][3] = 2
    return out

    # . . . . .
    # . ^ ^ . .
    # . . X . .
    # . . . * .
    # . . . . .
    # {. : empty, ^ : tree, X : fire, * : ash}

def test_step():
    world = build_world()
    res = step(world, 0.5)

    assert res[1][1] == 1, f"Expected 1 (tree), got {res[1][1]}"
    assert res[1][2] == -20, f"Expected -20 (burning), got {res[1][2]}"
    assert res[2][2] == 2, f"Expected 2 (ash), got {res[2][2]}"
    assert res[3][3] == 0, f"Expected 0 (empty), got {res[3][3]}"
    
def test_step_prob():
    world = build_world()
    res = step(world, 1.0)
    exp = np.ones((5, 5))
    exp[1][2] = -20
    exp[2][2] = 2
    exp[3][3] = 0

    assert np.array_equal(res, exp), f"Expected {exp},\ngot {res}"

if __name__ == "__main__":
    test_step()
    test_step_prob()
    print("All test cases passed!")