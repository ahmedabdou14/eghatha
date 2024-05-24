import random


def gen_location() -> tuple[float, float]:
    return (random.uniform(-90, 90), random.uniform(-180, 180))