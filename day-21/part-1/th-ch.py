from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # Parse input
        all_ingredients = set()
        nb_lists_by_ingredient = {}
        possible_ingredients_by_allergen = {}
        for line in s.split("\n"):
            ingredients, allergens = line.split(" (contains ")
            ingredients = set(ingredients.split(" "))
            allergens = allergens[:-1].split(", ")
            for allergen in allergens:
                if allergen not in possible_ingredients_by_allergen:
                    possible_ingredients_by_allergen[allergen] = []
                possible_ingredients_by_allergen[allergen].append(ingredients)
                all_ingredients.update(ingredients)
            for ingredient in ingredients:
                if ingredient not in nb_lists_by_ingredient:
                    nb_lists_by_ingredient[ingredient] = 0
                nb_lists_by_ingredient[ingredient] += 1

        # Compute ingredients that have no allergens
        ingredients_no_allergens = all_ingredients.difference(
            set.union(
                *[
                    set.intersection(*possible_ingredients)
                    for _, possible_ingredients in possible_ingredients_by_allergen.items()
                ]
            )
        )

        # Compute how many times these ingredient without allergens appear
        return sum(
            nb_lists_by_ingredient[ingredient]
            for ingredient in ingredients_no_allergens
        )
