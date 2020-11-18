# TODO(Mike) Consider wrapping this in a class??
import random
import numpy as np
rg = np.random.default_rng()

class StarRating:
    def __init__(self, star_rating, lower_attr_bound, upper_attr_bound, mean=None, standard_deviation=None):
        self.star_rating = star_rating
        # Fixes if you put the bounds in the wrong place. You shouldn't but whatever. This will correct it if you do.
        if lower_attr_bound > upper_attr_bound:
            tri_bound = upper_attr_bound
            lower_attr_bound = upper_attr_bound
            upper_attr_bound = tri_bound
        self.bounds = (lower_attr_bound, upper_attr_bound)
        if not mean:
            mean = (self.bounds[0] + self.bounds[1]) / 2
        if not standard_deviation:
            # Creates an array from the bottom of the bounds to the top of the bounds, with spacing of 1 int between each value
            standard_deviation = np.std([i for i in range(self.bounds[0], self.bounds[1])])
        self.mean = mean
        self.standard_deviation = standard_deviation

class AttrHandler:
    pass

# TODO(Mike) Define positions?
# def generate_player(star_rating, player_name, primary_position, secondary_position=None):
#     # Standard deviation is 2.8722813232690143 (ish)

#     pass

def generate_team():
# Figure out what all is needed to 'seed' a teams players. 
# Potential things.
# Precreated Team template?
#   - EG: Tier, target overall, offensive play style, defensive play style, target location
#   coaches, salary caps for the team (if applicable), scholorship caps for the team (if applicable), 
#   general model information.
    pass

def generate_player():
    STAR_1_BOUNDS = [40, 49]
    STAR_2_BOUNDS = [50, 59]
    STAR_3_BOUNDS = [60, 69]
    STAR_4_BOUNDS = [70, 79]
    STAR_5_BOUNDS = [80, 89]

    GENERIC_1_STAR = StarRating(1, STAR_1_BOUNDS[0], STAR_1_BOUNDS[1])
    GENERIC_2_STAR = StarRating(2, STAR_2_BOUNDS[0], STAR_2_BOUNDS[1])
    GENERIC_3_STAR = StarRating(3, STAR_3_BOUNDS[0], STAR_3_BOUNDS[1])
    GENERIC_4_STAR = StarRating(4, STAR_4_BOUNDS[0], STAR_4_BOUNDS[1])
    GENERIC_5_STAR = StarRating(5, STAR_5_BOUNDS[0], STAR_5_BOUNDS[1])

'''
    params: lower_bound (number): Lower bound of the range that you wish to pick your random from
    params: upper_bound (number): Upper bound of the range that you wish to pick your random from
    params: break_point (number): Split point between the 2 zones
    params: break_point_bias (number): Which zone to favor if the rand lands on the break point

    returns:
         (winning_bound (number), rng_choice (number)):
            winning_bound: the bound that won the random zone. If the lower_bound won, then we will return the lower bound. Same with the upper bound
            rng_choice (number): returns the chosen rng value
'''
def _rand_zone(lower_bound, upper_bound, break_point, break_point_bias):
    if not break_point_bias or break_point_bias not in [lower_bound, upper_bound]:
        print(f"Break Point Bias must be either lower_bound: {lower_bound} or upper_bound: {upper_bound}")
        raise ValueError()

    _rng = random.randrange(lower_bound, upper_bound)
    winning_zone = break_point_bias if _rng == break_point else None
    if _rng < break_point:
        winning_zone = lower_bound
    elif _rng > break_point:
        winning_zone = upper_bound
    return (winning_zone, _rng)
