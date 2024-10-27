import pulp
from collections import defaultdict


class Optimizer:
    def __init__(self, ingredients, cocktails_and_ingredients):
        self.ingredients = ingredients
        self.cocktails_and_ingredients = cocktails_and_ingredients

    def _optimize_cocktail_ingredients(self, df, num_ingredients):
        # Create mappings of cocktails to ingredients
        cocktail_ingredients = defaultdict(set)
        all_ingredients = set()
        for _, row in df.iterrows():
            cocktail_ingredients[row['cocktail_name']].add(row['ingredient_name'])
            all_ingredients.add(row['ingredient_name'])

        # Create the optimization problem
        prob = pulp.LpProblem("Cocktail_Optimizer", pulp.LpMaximize)

        # Decision variables
        # x[i] = 1 if ingredient i is selected, 0 otherwise
        x = pulp.LpVariable.dicts("ingredient",
                                  all_ingredients,
                                  cat='Binary')

        # y[c] = 1 if cocktail c can be made, 0 otherwise
        y = pulp.LpVariable.dicts("cocktail",
                                  cocktail_ingredients.keys(),
                                  cat='Binary')

        # Objective: Maximize number of possible cocktails
        prob += pulp.lpSum(y[c] for c in cocktail_ingredients.keys())

        # Constraint: Can only select num_ingredients ingredients
        prob += pulp.lpSum(x[i] for i in all_ingredients) == num_ingredients

        # Constraints: A cocktail can only be made if all its ingredients are selected
        for cocktail, ingredients in cocktail_ingredients.items():
            for ingredient in ingredients:
                prob += y[cocktail] <= x[ingredient]

        # Solve the problem
        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        # Get results
        selected_ingredients = [i for i in all_ingredients if x[i].value() == 1]
        makeable_cocktails = [c for c in cocktail_ingredients.keys()
                              if y[c].value() == 1]

        # Calculate how many cocktails each selected ingredient is used in
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
