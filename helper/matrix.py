def mat_add(move_a, move_b):
    return [a + b for a, b in zip(move_a, move_b)]

def mat_movement(move):
    return any(move)

def mat_nul():
    return [
        0, 0, 0, 0
    ]