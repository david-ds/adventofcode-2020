from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # Parse input
        all_ingredients = set()
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

        # Part 1: compute ingredients that have no allergens
        ingredients_no_allergens = all_ingredients.difference(
            set.union(
                *[
                    set.intersection(*possible_ingredients)
                    for _, possible_ingredients in possible_ingredients_by_allergen.items()
                ]
            )
        )

        # Discard these ingredients without allergens
        for allergen, lists_of_ingredients in possible_ingredients_by_allergen.items():
            possible_ingredients_by_allergen[allergen] = set.intersection(
                *[
                    ingredients.difference(ingredients_no_allergens)
                    for ingredients in lists_of_ingredients
                ]
            )

        # Resolve links ingredient <-> allergen
        resolved_ingredients = set()
        while len(resolved_ingredients) < len(possible_ingredients_by_allergen):
            for allergen, ingredients in possible_ingredients_by_allergen.items():
                if len(ingredients) > 1:
                    possible_ingredients_by_allergen[allergen] = ingredients.difference(
                        resolved_ingredients
                    )

            for allergen, ingredients in possible_ingredients_by_allergen.items():
                if len(ingredients) == 1:
                    ingredient = next(iter(ingredients))
                    resolved_ingredients.add(ingredient)

        # Sort by allergen and return ingredients
        return ",".join(
            ingredient.pop()
            for _, ingredient in sorted(
                possible_ingredients_by_allergen.items(),
                key=lambda allergen_with_ingredient: allergen_with_ingredient[0],
            )
        )
