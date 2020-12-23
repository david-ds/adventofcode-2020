from collections import defaultdict
from typing import  List
from tool.runners.python import SubmissionPy
from copy import copy

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        # parse
        lines: List[str] = s.strip().split("\n")
        recipes = []
        all_ingredients = set()
        for l in lines:
            ingredients, allergens = l.split(" (contains ")
            ingredients = ingredients.split()
            all_ingredients.update(ingredients)
            allergens = allergens.rstrip(")").split(", ")
            recipes.append((ingredients, allergens))

        allergens_in = defaultdict(list)
        for (ingredients, allergens) in recipes:
            for allergen in allergens:
                allergens_in[allergen].append(set(ingredients))
        
        # take the intersection
        possible_ingredients_by_allergen = dict()
        for allergen in allergens_in:
            possible_ingredients_by_allergen[allergen] = set.intersection(*allergens_in[allergen])

        possible_ingredients_with_allergen = set.union(*possible_ingredients_by_allergen.values())
        ingredients_without_allergen = set()
        for ingredient in all_ingredients:
            if ingredient not in possible_ingredients_with_allergen:
                ingredients_without_allergen.add(ingredient)

        remaining_allergens = set(possible_ingredients_by_allergen.keys())
        while remaining_allergens:
            for allergen in copy(remaining_allergens):
                if len(possible_ingredients_by_allergen[allergen]) == 1:
                    ing = list(possible_ingredients_by_allergen[allergen])[0]
                    remaining_allergens.remove(allergen)
                    for a2 in possible_ingredients_by_allergen:
                        if a2 != allergen:
                            possible_ingredients_by_allergen[a2].discard(ing)

        # now we have the definitive list, build the output
        return ",".join(
            list(possible_ingredients_by_allergen[allergen])[0] for allergen in sorted(list(possible_ingredients_by_allergen.keys())))


def test_coco():
    assert CocoSubmission().run("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""") == 5
