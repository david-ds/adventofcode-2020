from collections import Counter

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        self.allergen_candidates = dict()
        for ingredients, allergens in map(self.parse_line, s.splitlines()):
            for allergen in allergens:
                if allergen in self.allergen_candidates:
                    self.allergen_candidates[allergen] &= set(ingredients)
                else:
                    self.allergen_candidates[allergen] = set(ingredients)

                # if we found the ingredient containing this allergen, remove it
                # from the candidates for other allergens
                if len(self.allergen_candidates[allergen]) == 1:
                    ingredient = next(iter(self.allergen_candidates[allergen]))
                    self.remove_ingredient_from_candidates(ingredient, allergen)

        return ",".join(
            next(iter(ingredient))
            for allergen, ingredient in sorted(self.allergen_candidates.items())
        )

    @staticmethod
    def parse_line(line):
        ingredients_str, allergens_str = line.split(" (")
        ingredients = ingredients_str.split()
        allergens = allergens_str[9:-1].split(", ")
        return ingredients, allergens

    def remove_ingredient_from_candidates(self, ingredient, allergen):
        for a, ingredients in self.allergen_candidates.items():
            if a != allergen and ingredient in ingredients:
                ingredients.remove(ingredient)
                # if we found the ingredient containing this allergen, remove it
                # from the candidates for other allergens
                if len(ingredients) == 1:
                    i = next(iter(ingredients))
                    self.remove_ingredient_from_candidates(i, a)


def test_day21_part2():
    assert (
        ThoreSubmission().run(
            """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
        )
        == "mxmxvkd,sqjhc,fvjkl"
    )
