from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        allergens = dict()
        foods = list()
        ingredients = set()

        for food in s.split("\n"):
            food_ingredients, food_allergens = food[:-1].split(" (contains ")

            # Yolo retype food_ingredients, the string is not used anyway
            food_ingredients = set(food_ingredients.split())
            foods.append(food_ingredients.copy())
            ingredients.update(food_ingredients)

            for allergen in food_allergens.split(", "):
                if allergen not in allergens:
                    # If the allergen is unknown, we assume that it can be associated with any of the ingredients in the food
                    allergens[allergen] = food_ingredients.copy()
                else:
                    # Otherwise the allergen is in both the previous ingredients and the current ingredients
                    allergens[allergen].intersection_update(food_ingredients)

        for allergen in allergens:
            ingredients.difference_update(allergens[allergen])

        return sum(ingredient in food for food in foods for ingredient in ingredients)


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
        == 5
    )
