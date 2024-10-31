import pandas as pd
import re


def _create_ingredients_table(cocktails):
    ingredients = pd.DataFrame(columns=['ingredient'])

    for index, row in cocktails.iterrows():
        for ingredient in row['ingredients']:
            ingredients = pd.concat([ingredients, pd.DataFrame({'ingredient': [ingredient]})], ignore_index=True)

    for index, row in ingredients.iterrows():
        for key, val in row['ingredient'].items():
            ingredients.loc[index, key] = val

    ingredients.drop(columns=['ingredient', 'measure', 'createdAt', 'updatedAt'], inplace=True)
    ingredients.drop_duplicates(inplace=True)
    ingredients.sort_values(by='name', inplace=True)
    ingredients['id'] = ingredients['id'].astype(int)
    ingredients.set_index('id', inplace=True)

    return ingredients


def _create_cocktails_and_ingredients_table(cocktails):
    cocktails_and_ingredients = pd.DataFrame(
        columns=['cocktail_id', 'cocktail_name', 'ingredient_id', 'ingredient_name', 'measure'])

    for index, row in cocktails.iterrows():
        cocktail_name = row['name']
        # Extract ingredients
        for ingredient in row['ingredients']:
            ingredient_id = ingredient['id']
            ingredient_name = ingredient['name']
            try:
                measure = ingredient['measure']
            except:
                measure = None

            # Append to the cocktails_and_ingredients DataFrame
            cocktails_and_ingredients = pd.concat([cocktails_and_ingredients,
                                                   pd.DataFrame(
                                                       {'cocktail_id': [index], 'cocktail_name': [cocktail_name],
                                                        'ingredient_id': [ingredient_id],
                                                        'ingredient_name': [ingredient_name],
                                                        'measure': [measure]})],
                                                  ignore_index=True)

    cocktails.drop(columns=['ingredients'], inplace=True)

    return cocktails_and_ingredients


def _clean_cocktails_table(cocktails):
    cocktails.drop(columns=['id', 'imageUrl', 'alcoholic', 'createdAt', 'updatedAt'],
                   inplace=True)  # Not needed for analysis


def _clean_ingredients_table(ingredients):
    ingredients.drop(columns=['imageUrl'], inplace=True)


def _preprocess_cocktails_table(cocktails, ingredients, cocktails_and_ingredients):
    result_df = cocktails_and_ingredients.set_index('ingredient_id').join(
        ingredients[['percentage', 'generalized_type']], how='left')

    # Calculate ABV for each cocktail
    def calculate_abv():
        for cocktail_id, group in result_df.groupby('cocktail_name'):
            essential_ingrs = []
            lack_of_data = False

            for index, row in group.iterrows():
                gen_type = row['generalized_type'] if pd.notna(row['generalized_type']) else "Unknown"
                volume_oz = row['volume_oz']
                percentage = row['percentage']

                if gen_type in ['Non-Alcoholic', 'Alcoholic'] and (pd.isna(volume_oz) or pd.isna(
                        percentage)):  # Absence of data for Fruit ingredients doesn't lead to mistakes, as all
                    # measures that have influence on ABV are present in dataset (see upper section)
                    essential_ingrs.clear()
                    lack_of_data = True

                    # break
                elif gen_type in ['Non-Alcoholic', 'Alcoholic', 'Fruit'] and pd.notna(volume_oz) and pd.notna(
                        percentage):
                    essential_ingrs.append([row['percentage'], row['volume_oz']])

            if not lack_of_data:
                total_volume, total_alcohol_volume, abv = 0, 0, 0

                for percentage, volume in essential_ingrs:
                    total_volume += volume
                    total_alcohol_volume += (percentage / 100) * volume

                if total_volume > 0 and total_alcohol_volume > 0:
                    abv = (total_alcohol_volume / total_volume) * 100
                else:
                    abv = None

                cocktails.loc[cocktails['name'] == cocktail_id, 'abv'] = abv
            else:
                cocktails.loc[cocktails['name'] == cocktail_id, 'abv'] = pd.NA

        cocktails['abv'] = cocktails['abv'].astype(float)

    calculate_abv()

    # Categorize cocktails based on ABV
    def categorize_abv(abv):
        if pd.isna(abv):
            return 'Unknown'
        elif abv < 10:
            return 'Weak'
        elif 10 <= abv < 20:
            return 'Moderate'
        elif 20 <= abv < 30:
            return 'Strong'
        else:
            return 'Very Strong'

    # Apply the function to the ABV column to create the 'strength' column
    cocktails['strength'] = cocktails['abv'].apply(categorize_abv)

    # Cocktails instructions length
    cocktails['instruction_length'] = cocktails['instructions'].str.len()
    cocktails.head(3)

    # Cocktails number of ingredients
    ingredients_counts = cocktails_and_ingredients.groupby('cocktail_id')['ingredient_id'].count().sort_values(
        ascending=False)
    cocktails['num_ingredients'] = ingredients_counts
    cocktails.head(3)

    # Cocktails preparation method
    cocktails['prep_method'] = cocktails['instructions'].str.extract(r'(?i)\b(Stir|Blend|Shake)\b')

    cocktails.loc[cocktails['prep_method'].isna(), 'prep_method'] = cocktails['instructions'].str.extract(
        r'(?i)\b(Pour)\b', expand=False)

    cocktails['prep_method'] = cocktails['prep_method'].fillna('Unknown')
    cocktails['prep_method'] = cocktails['prep_method'].str.capitalize()


def _preprocess_ingredients_table(ingredients):
    ingredients.loc[ingredients['type'] == 'Liquer', 'type'] = 'Liqueur'
    ingredients.loc[ingredients['type'] == 'Bitters', 'type'] = 'Bitter'
    ingredients.loc[ingredients['type'] == 'Beverage', 'type'] = 'Brandy'

    # Creating less specific types of ingredients for future analysis
    def ingredient_type_mapper(ingr_type):
        ingredient_mapping = {
            'Liqueur': 'Alcoholic',
            'Bitter': 'Alcoholic',
            'Brandy': 'Alcoholic',
            'Rum': 'Alcoholic',
            'Whiskey': 'Alcoholic',
            'Whisky': 'Alcoholic',
            'Spirit': 'Alcoholic',
            'Wine': 'Alcoholic',
            'Fortified Wine': 'Alcoholic',
            'Gin': 'Alcoholic',
            'Vodka': 'Alcoholic',
            'Water': 'Non-Alcoholic',
            'Soft Drink': 'Non-Alcoholic',
            'Juice': 'Non-Alcoholic',
            'Syrup': 'Non-Alcoholic',
            'Soda': 'Non-Alcoholic',
            'Tea': 'Non-Alcoholic',
            'Cream': 'Toppings',
            'Sauce': 'Toppings',
            'Mineral': 'Toppings',
            'Fruit': 'Fruit',
            'Flower': 'Decoration'
        }

        return ingredient_mapping.get(ingr_type, pd.NA)

    ingredients['generalized_type'] = ingredients['type'].apply(ingredient_type_mapper)

    def fill_percentage_data():
        # Filling percentage data for ingredients
        ingredients['percentage'] = ingredients['percentage'].astype(float)

        alcoholic_types_with_percentage = ingredients[ingredients['percentage'].notna()]['type'].unique()

        for ingr_type in alcoholic_types_with_percentage:
            mean_percentage = ingredients.query(f'type == "{ingr_type}"')['percentage'].mean()

            ingredients.loc[ingredients['type'] == ingr_type, 'percentage'] = ingredients.loc[
                ingredients['type'] == ingr_type, 'percentage'].fillna(mean_percentage)

        # Specifically filling values for Whisky
        mean_percentage = ingredients.query('type == "Whiskey"')['percentage'].mean()
        ingredients.loc[ingredients['type'] == 'Whisky', 'percentage'] = ingredients.loc[
            ingredients['type'] == 'Whisky', 'percentage'].fillna(mean_percentage)

        # For rest of generalized_types fill percentage column with zeroes
        ingredients.loc[ingredients['generalized_type'] != 'Alcoholic', 'percentage'] = 0

    fill_percentage_data()

    # Filling generalized_types for some ingredients
    ingredients.loc[53, 'generalized_type'] = 'Alcoholic'
    ingredients.loc[56, 'generalized_type'] = 'Alcoholic'
    ingredients.loc[127, 'generalized_type'] = 'Non-Alcoholic'
    ingredients.loc[296, 'generalized_type'] = 'Alcoholic'
    ingredients.loc[170, 'generalized_type'] = 'Non-Alcoholic'

    # Set percentage to NaN where generalized_type is 'Alcoholic' and percentage is 0
    ingredients.loc[
        (ingredients['generalized_type'] == 'Alcoholic') & (ingredients['percentage'] == 0), 'percentage'] = pd.NA


def _preprocess_cocktails_and_ingredients_table(cocktails_and_ingredients):
    # Measures parsing
    def parse_oz_measure(measure):
        # Regex pattern to capture ranges like '2-3 oz' and fractions like '1/2 oz'
        if 'oz' not in measure:
            return None

        range_pattern = re.match(r'(\d+)-(\d+)', measure)
        fraction_pattern = re.match(r'(\d+)\s(\d+/\d+)', measure)
        simple_fraction_pattern = re.match(r'(\d+/\d+)', measure)
        simple_value_pattern = re.match(r'(\d+)', measure)

        if range_pattern:
            # Handle ranges like '2-3 oz', return the average
            low, high = range_pattern.groups()
            return (float(low) + float(high)) / 2

        elif fraction_pattern:
            # Handle mixed fractions like '1 2/3 oz'
            whole_part, fraction = fraction_pattern.groups()
            fraction_value = eval(fraction)  # Safely evaluate the fraction '2/3'
            return float(whole_part) + fraction_value

        elif simple_fraction_pattern:
            # Handle fractions like '1/2 oz'
            fraction_value = eval(simple_fraction_pattern.group(0))
            return fraction_value

        elif simple_value_pattern:
            # Handle simple values like '1 oz'
            return float(simple_value_pattern.group(0))

        # If none of the patterns match, return None
        return None

    def parse_juice_of_fruit_measure(measure, is_lemon=True):
        # Define juice volumes (in oz)
        lemon_juice_per_fruit = 1.52  # oz of juice from 1 lemon
        lime_juice_per_fruit = 1.01  # oz of juice from 1 lime

        # Select the correct juice amount based on the fruit type
        juice_per_fruit = lemon_juice_per_fruit if is_lemon else lime_juice_per_fruit

        # Remove the 'Juice of' part and strip extra spaces
        measure = measure.replace('Juice of', '').strip()

        # Handle different fractions or whole numbers
        if measure == '1':
            return juice_per_fruit
        elif measure == '1/2':
            return juice_per_fruit / 2
        elif measure == '1/4':
            return juice_per_fruit / 4
        else:
            return None

    def parse_juice_measure(row):
        if 'juice' not in row['measure'].lower():
            return None

        if "lemon" in row['ingredient_name'].lower():
            return parse_juice_of_fruit_measure(row['measure'], True)
        elif "lime" in row['ingredient_name'].lower():
            return parse_juice_of_fruit_measure(row['measure'], False)

    def parse_spoon_measure(measure):
        tblsp = 0.47
        tsp = 0.135
        # Extract numerical part of the measure using regex to handle fractions
        pattern = r"(\d+(\s*\d+/\d+)?|\d+/\d+)\s*(tsp|tblsp)"
        match = re.search(pattern, measure)

        if match:
            quantity = match.group(1).strip()  # '1', '1/2', '1 1/2', etc.
            unit = match.group(3).strip()  # 'tsp' or 'tblsp'

            # Convert quantity to float, including handling fractions like '1 1/2' or '1/4'
            def fraction_to_float(frac):
                parts = frac.split()
                if len(parts) == 2:  # handle mixed numbers like '1 1/2'
                    return float(parts[0]) + eval(parts[1])
                return eval(parts[0])

            quantity = fraction_to_float(quantity)

            # Convert based on unit
            if unit == 'tsp':
                return quantity * tsp  # return in oz
            elif unit == 'tblsp':
                return quantity * tblsp  # return in oz
        else:
            return None

    def parse_measure(row):
        res = parse_oz_measure(row['measure'])

        if res is not None:
            return res

        res = parse_spoon_measure(row['measure'])

        if res is not None:
            return res

        res = parse_juice_measure(row)

        if res is not None:
            return res

        return None

    # Converting measures to volume in oz
    cocktails_and_ingredients['measure'] = cocktails_and_ingredients['measure'].astype(str)
    cocktails_and_ingredients['volume_oz'] = cocktails_and_ingredients.apply(parse_measure, axis=1)


def preprocess():
    # Read json
    init_table = pd.read_json(
        "https://raw.githubusercontent.com/Solvro/rekrutacja/refs/heads/main/data/cocktail_dataset.json")

    # Tables creation
    cocktails = init_table
    ingredients = _create_ingredients_table(cocktails)
    cocktails_and_ingredients = _create_cocktails_and_ingredients_table(cocktails)

    # Tables cleaning
    _clean_cocktails_table(cocktails)
    _clean_ingredients_table(ingredients)

    # Tables preprocessing
    _preprocess_ingredients_table(ingredients)
    _preprocess_cocktails_and_ingredients_table(cocktails_and_ingredients)
    _preprocess_cocktails_table(cocktails, ingredients, cocktails_and_ingredients)

    return cocktails, ingredients, cocktails_and_ingredients
