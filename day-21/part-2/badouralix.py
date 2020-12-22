from tool.runners.python import SubmissionPy

from collections import defaultdict
from queue import Queue


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        allergens = dict()  # Mapping of allergens to their potential ingredients
        ingredients = defaultdict(
            set
        )  # Mapping of ingredients to their potential allergens
        queue = Queue()

        for food in s.split("\n"):
            food_ingredients, food_allergens = food[:-1].split(" (contains ")

            # Yolo retype food_ingredients, the string is not used anyway
            food_ingredients = set(food_ingredients.split())

            for allergen in food_allergens.split(", "):
                if allergen not in allergens:
                    # If the allergen is unknown, we assume that it can be associated with any of the ingredients in the food
                    allergens[allergen] = food_ingredients.copy()
                else:
                    # Otherwise the allergen is in both the previous ingredients and the current ingredients
                    allergens[allergen].intersection_update(food_ingredients)

        # Build ingredients for allergens reverse lookup
        for allergen in allergens:
            for ingredient in allergens[allergen]:
                ingredients[ingredient].add(allergen)

            # Enqueue ingredient for later processing
            queue.put(allergen)

        # Recursively propagate the discovery of an allergen-ingredient association
        while not queue.empty():
            # Pick the next allergen to propagate in a breadth first traversal
            allergen = queue.get()
            if len(allergens[allergen]) != 1:
                continue

            # Pick the only ingredient associated with the allergen
            ingredient = next(iter(allergens[allergen]))

            # Remove the ingredient from its other potential allergens and put these allergens in the processing queue
            for a in ingredients[ingredient]:
                if a != allergen:
                    allergens[a].discard(ingredient)
                    queue.put(a)

            # Also update the reverse lookup map to remember that we found its associated allergen
            ingredients[ingredient] = {allergen}

        # Yolo assume that we perfectly found all allergen-ingredient association
        return ",".join(
            next(iter(allergens[allergen])) for allergen in sorted(allergens)
        )


def test_badouralix():
    assert (
        BadouralixSubmission().run(
            """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""".strip()
        )
        == "mxmxvkd,sqjhc,fvjkl"
    )
