import pulp
from collections import defaultdict


class Optimizer:
    """
    A class used to perform optimization on ingredients problem: finds n ingredients with which you can make
    the largest amount of different cocktails
    """
    def __init__(self, ingredients, cocktails_and_ingredients):
        self.ingredients = ingredients
        self.cocktails_and_ingredients = cocktails_and_ingredients

    def _optimize_cocktail_ingredients(self, df, num_ingredients):
        """
        Finds n ingredients with which you can make the largest amount of different cocktails, and return it along with
        the cocktails you can make, and their usage
        :param df: Cocktails and ingredients dataframe
        :param num_ingredients:
        :return: Dictionary of 'selected_ingredients', 'num_cocktails', 'makeable_cocktails', 'ingredient_usage'
        """

        # Create mappings of cocktails to ingredients
        cocktail_ingredients = defaultdict(set)
        all_ingredients = set()
        for _, row in df.iterrows():
            cocktail_ingredients[row['cocktail_name']].add(row['ingredient_name'])
            all_ingredients.add(row['ingredient_name'])

        prob = pulp.LpProblem("Cocktail_Optimizer", pulp.LpMaximize)

        x = pulp.LpVariable.dicts("ingredient",
                                  all_ingredients,
                                  cat='Binary')

        y = pulp.LpVariable.dicts("cocktail",
                                  cocktail_ingredients.keys(),
                                  cat='Binary')

        prob += pulp.lpSum(y[c] for c in cocktail_ingredients.keys())

        prob += pulp.lpSum(x[i] for i in all_ingredients) == num_ingredients

        for cocktail, ingredients in cocktail_ingredients.items():
            for ingredient in ingredients:
                prob += y[cocktail] <= x[ingredient]

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        selected_ingredients = [i for i in all_ingredients if x[i].value() == 1]
        makeable_cocktails = [c for c in cocktail_ingredients.keys()
                              if y[c].value() == 1]

        ingredient_usage = defaultdict(int)
        for cocktail in makeable_cocktails:
            for ingredient in cocktail_ingredients[cocktail]:
                if ingredient in selected_ingredients:
                    ingredient_usage[ingredient] += 1

        return {
            'selected_ingredients': selected_ingredients,
            'num_cocktails': len(makeable_cocktails),
            'makeable_cocktails': sorted(makeable_cocktails),
            'ingredient_usage': ingredient_usage
        }

    def print_results(self, result):
        """
        Function to print results from dictionary with optimization data
        :param result: Result dictionary you get from _optimize_cocktail_ingredients function
        :return:
        """
        print(
            f"With {len(result['selected_ingredients'])} ingredients, you can make {result['num_cocktails']} cocktails!\n")

        print("Selected ingredients and their usage:")
        for i, ingredient in enumerate(sorted(result['selected_ingredients'],
                                              key=lambda x: result['ingredient_usage'][x],
                                              reverse=True), 1):
            uses = result['ingredient_usage'][ingredient]
            print(f"{i}. {ingredient} (used in {uses} cocktails)")

        if 'rest_of_ingredients' in result:
            print("\nRest of needed ingredients:")
            for ingredient in result['rest_of_ingredients']:
                print(f"{ingredient}")

        print("\nCocktails you can make:")
        for cocktail in result['makeable_cocktails']:
            print(f"- {cocktail}")

    def find_n_ingredients_to_make_largest_amount_of_cocktails(self, n_ingredients, only_alcoholic=False):
        """
        Finds n ingredients with which you can make the largest amount of different cocktails
        :param n_ingredients:
        :param only_alcoholic: If we are taking into account only alcoholic ingredients or not
        :return: Dictionary of 'selected_ingredients', 'num_cocktails', 'makeable_cocktails', 'ingredient_usage',
        'rest_of_ingredients' if only_alcoholic is True
        """
        if only_alcoholic:
            result_df = self.cocktails_and_ingredients.set_index('ingredient_id').join(
                self.ingredients[['generalized_type']],
                how='left')
            cocktails_bases = result_df.query('generalized_type == "Alcoholic"')

            result = self._optimize_cocktail_ingredients(cocktails_bases, n_ingredients)

            makeable_cocktails = result['makeable_cocktails']

            result['rest_of_ingredients'] = \
                result_df.query('cocktail_name in @makeable_cocktails & generalized_type != "Alcoholic"')[
                    'ingredient_name'].unique()

            return result
        else:
            result = self._optimize_cocktail_ingredients(self.cocktails_and_ingredients, n_ingredients)

            return result
