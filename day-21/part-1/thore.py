from collections import Counter

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        allergen_candidates = dict()
        ingredients_counter = Counter()
        for ingredients, allergens in map(self.parse_line, s.splitlines()):
            for allergen in allergens:
                if allergen in allergen_candidates:
                    allergen_candidates[allergen] &= set(ingredients)
                else:
                    allergen_candidates[allergen] = set(ingredients)
            ingredients_counter.update(ingredients)

        no_allergen_ingredients = ingredients_counter.keys() - set.union(
            *allergen_candidates.values()
        )
        return sum(ingredients_counter[i] for i in no_allergen_ingredients)

    @staticmethod
    def parse_line(line):
        ingredients_str, allergens_str = line.split(" (")
        ingredients = ingredients_str.split()
        allergens = allergens_str[9:-1].split(", ")
        return ingredients, allergens


def test_day21_part1():
    assert (
        ThoreSubmission().run(
            """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
        )
        == 5
    )
