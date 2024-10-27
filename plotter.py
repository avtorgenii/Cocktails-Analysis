import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Plotter:
    def __init__(self, cocktails, ingredients, cocktails_and_ingredients):
        self.cocktails = cocktails
        self.ingredients = ingredients
        self.cocktails_and_ingredients = cocktails_and_ingredients

    # Cocktails
    def plot_cocktail_categories(self):
        # Cocktails Categories
        top_categories = self.cocktails['category'].value_counts()

        # Create a bar plot using seaborn
        plt.figure(figsize=(12, 6))

        # Pie Chart
        wedges, texts, autotexts = plt.pie(top_categories, labels=top_categories.index, autopct='%1.1f%%',
                                           startangle=180, colors=sns.color_palette('coolwarm', len(top_categories)))

        # Add labels and title
        plt.title('Cocktails Categories')

        # Create custom labels for the legend that include category and number of cocktails
        legend_labels = [f'{count} cocktails' for count in top_categories]

        # Add the legend
        plt.legend(wedges, legend_labels, title="Number of Cocktails", loc="upper right", bbox_to_anchor=(1.1, 1))

        # Show the plot
        plt.show()

    def plot_cocktails_preparation_methods(self):
        # Cocktails methods of preparation
        prep_methods = self.cocktails['prep_method'].value_counts()

        # Create a bar plot using seaborn
        plt.figure(figsize=(12, 6))

        # Pie Chart
        wedges, texts, autotexts = plt.pie(prep_methods, labels=prep_methods.index, autopct='%1.1f%%', startangle=200,
                                           colors=sns.color_palette('coolwarm', len(prep_methods)))

        # Add labels and title
        plt.title('Cocktails methods of preparation')

        # Create custom labels for the legend that include category and number of cocktails
        legend_labels = [f'{count} cocktails' for count in prep_methods]

        # Add the legend
        plt.legend(wedges, legend_labels, title="Number of Cocktails", loc="upper right", bbox_to_anchor=(1.1, 1))

        # Show the plot
        plt.show()

    def plot_cocktail_glasses(self):
        # Cocktails Glasses
        top_categories = self.cocktails['glass'].value_counts()

        # Create a bar plot using seaborn
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x=top_categories.values / len(self.cocktails) * 100, y=top_categories.index,
                         palette='coolwarm',
                         hue=top_categories.index)

        # Add labels and title
        plt.xlabel('Cocktails(%)')
        plt.ylabel('Glass')
        plt.title('Cocktails Glasses')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f%%')

        # Show the plot
        plt.show()

    def plot_cocktail_instruction_lengths(self, n_cocktails):
        # Top N hardest to prepare cocktails
        hardest_cocktails = self.cocktails.sort_values(ascending=False, by='instruction_length').head(n_cocktails)

        # Create a bar plot using seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=hardest_cocktails['instruction_length'], y=hardest_cocktails['name'], palette='coolwarm',
                    hue=hardest_cocktails['name'])

        # Add labels and title
        plt.ylabel('Cocktails')
        plt.xlabel('Instruction length')
        plt.title(f'Top {n_cocktails} Cocktails by instruction length')

        # Show the plot
        plt.show()

    def plot_cocktails_with_largest_amount_of_ingredients(self, n_cocktails):
        # Top N cocktails with largest amount of ingredients
        top_n = 30
        hardest_cocktails = self.cocktails.sort_values(ascending=False, by='num_ingredients').head(top_n)

        # Create a bar plot using seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=hardest_cocktails['num_ingredients'], y=hardest_cocktails['name'], palette='coolwarm',
                    hue=hardest_cocktails['name'])

        # Add labels and title
        plt.ylabel('Cocktails')
        plt.xlabel('Num of ingredients')
        plt.title(f'Top {top_n} cocktails by ingredients number')

        # Show the plot
        plt.show()

    def plot_cocktails_rank_by_abv(self, n_cocktails, strongest=True):
        # Cocktails ABV rank
        cocktails = self.cocktails.sort_values(ascending=not strongest, by='abv').head(n_cocktails)

        # Create a bar plot using seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=cocktails['abv'], y=cocktails['name'], palette='coolwarm',
                    hue=cocktails['name'])

        # Add labels and title
        plt.ylabel('Cocktails')
        plt.xlabel('ABV(%)')
        if strongest:
            plt.title(f'Top {n_cocktails} Strongest Cocktails')
        else:
            plt.title(f'Top {n_cocktails} Weakest Cocktails')

        # Show the plot
        plt.show()

    def plot_cocktails_strength_distribution(self):
        # Cocktails strength distribution
        # Get the strengths distribution
        strengths = self.cocktails['strength'].value_counts()

        # Create a figure with two subplots
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

        # Bar Plot
        sns.barplot(y=strengths.values, x=strengths.index, hue=strengths.values, ax=axs[0], legend=False)
        axs[0].set_ylabel('Number of Cocktails')
        axs[0].set_xlabel('Strength')
        axs[0].set_title('Cocktails Strength Distribution')

        # Add value labels on top of each bar
        for i, v in enumerate(strengths.values):
            axs[0].text(i, v, str(v), ha='center', va='bottom')

        strengths = self.cocktails.query('strength != "Unknown"')['strength'].value_counts()

        # Pie Chart
        wedges, texts, autotexts = axs[1].pie(strengths, labels=strengths.index, autopct='%1.1f%%', startangle=195,
                                              colors=sns.color_palette('coolwarm', len(strengths)))

        axs[1].legend(wedges, ['>30%', '20-30%', '10-20%', '<10%'], title="ABV for strength categories", loc="best")

        axs[1].axis('equal')  # Equal aspect ratio ensures that pie chart is circular
        axs[1].set_title('Cocktails Strength Distribution (Without Unknowns)')

        # Show the plots
        plt.tight_layout()  # Adjusts the layout to prevent overlap
        plt.show()

    # Ingredients
    def plot_ingredient_types_distribution(self):
        # Ingredient types distribution
        ingredient_counts = self.ingredients['generalized_type'].value_counts()

        # Create a bar plot using seaborn
        plt.figure(figsize=(10, 6))
        plt.pie(ingredient_counts, labels=ingredient_counts.index, autopct='%1.1f%%', startangle=180,
                colors=sns.color_palette('coolwarm', len(ingredient_counts)))

        # Add labels and title
        plt.title('Ingredient types distribution')
        plt.show()

    def plot_most_common_ingredients(self, n_ingredients):
        # Top N most common ingredients in cocktails
        ingredient_counts = self.cocktails_and_ingredients['ingredient_name'].value_counts()

        top_ingredients = ingredient_counts.head(n_ingredients)

        # Create a bar plot using seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_ingredients.values / len(self.cocktails) * 100, y=top_ingredients.index, palette='coolwarm',
                    hue=top_ingredients.index)

        # Add labels and title
        plt.xlabel('Cocktails(%)')
        plt.ylabel('Ingredient')
        plt.title(f'Top {n_ingredients} Most Common Ingredients')

        # Show the plot
        plt.show()

    def plot_ingredients_co_occurrences(self):
        # Which ingredients tend to appear together in the same cocktails (Ingredient type and ingredients)
        result_df = self.cocktails_and_ingredients.set_index('ingredient_id').join(
            self.ingredients[['generalized_type', 'name', 'type']], how='left')
        most_frequent_types = result_df['type'].value_counts().index[:7]

        fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10))
        axes = axes.flatten()

        for i, ingr_type in enumerate(most_frequent_types):
            cocktails_with_type = result_df[result_df['type'] == ingr_type]['cocktail_name'].unique()
            cocktails_with_type_df = result_df[result_df['cocktail_name'].isin(cocktails_with_type)]
            co_occurring_ingredients = cocktails_with_type_df[cocktails_with_type_df['type'] != ingr_type]
            co_occurrence_counts = co_occurring_ingredients['name'].value_counts().head(10).sort_values(ascending=True)

            axes[i].barh(co_occurrence_counts.index, co_occurrence_counts.values, color='lightblue')
            axes[i].set_title(f'Co-occurrences with {ingr_type}')
            axes[i].set_ylabel('Ingredient Name')
            axes[i].set_xlabel('Count')
            axes[i].tick_params(axis='y', rotation=0)

        fig.delaxes(axes[7])

        plt.tight_layout()
        plt.show()

    def plot_ingredients_by_mean_used_volume(self, n_ingredients, alcoholic=False):
        if alcoholic:
            merged_df = pd.merge(self.ingredients, self.cocktails_and_ingredients, left_on='id',
                                 right_on='ingredient_id',
                                 how='inner')
            ingredients_and_volumes = merged_df.query('generalized_type == "Alcoholic"').groupby('ingredient_name')[
                'volume_oz'].mean().sort_values(ascending=False)
        else:
            # Average volume of main ingredients used in cocktails
            ingredients_and_volumes = self.cocktails_and_ingredients.groupby('ingredient_name')[
                'volume_oz'].mean().sort_values(
                ascending=False)

        top_ingredients = ingredients_and_volumes.head(n_ingredients)

        # Create a bar plot using seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_ingredients.values, y=top_ingredients.index, palette='coolwarm', hue=top_ingredients.index)

        # Add labels and title
        plt.xlabel('Volume Oz')
        plt.ylabel('Ingredient')
        if alcoholic:
            plt.title(f'Top {n_ingredients} Alcoholic Ingredients by Mean Used Volume')
        else:
            plt.title(f'Top {n_ingredients} Ingredients by Mean Used Volume')

        # Show the plot
        plt.show()

    # Cocktails and ingredients
    def plot_ingredients_frequency_in_every_glass(self):
        # Which glass types are used with ingredients types

        # Function to get ingredients for a given cocktail name
        def get_ingredients(cocktail_name):
            # Join dataframes to get the necessary information
            result_df = self.cocktails_and_ingredients.set_index('ingredient_id').join(
                self.ingredients[['generalized_type', 'name', 'type']], how='left')

            # Filter for the current cocktail
            group = result_df[result_df['cocktail_name'] == cocktail_name]

            ingrs = []

            for index, row in group.iterrows():
                # Only consider Alcoholic and Non-Alcoholic ingredients
                if pd.notna(row['generalized_type']):
                    if row['generalized_type'] in ('Alcoholic', 'Non-Alcoholic') and row['volume_oz'] is not None:
                        ingrs.append(row['type'])  # Collect ingredient names

            return ingrs

        # Initialize a list to hold ingredient and glass type pairs
        ingredients_list = []

        # Collect ingredients for each cocktail along with their glass types
        for index, row in self.cocktails.iterrows():
            cocktail_name = row['name']
            glass_type = row['glass']

            # Get ingredients for the cocktail
            ingrs = get_ingredients(cocktail_name)

            # Create a list of (ingredient, glass type) pairs
            for ingredient in ingrs:
                ingredients_list.append({'ingredient': ingredient, 'glass': glass_type})

        # Create a DataFrame from the ingredients list
        df = pd.DataFrame(ingredients_list)

        # Count occurrences of each ingredient for each glass type
        pivot_table = df.pivot_table(index='ingredient', columns='glass', aggfunc='size', fill_value=0)

        # Create the heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, cmap='Blues', fmt='g')

        # Add titles and labels
        plt.title('Number of Times Each Ingredient Type Appears in every Glass')
        plt.xlabel('Glass Type')
        plt.ylabel('Ingredient')

        # Show the chart
        plt.show()

    def most_common_ingredients_by_tags(self):
        # Most used ingredients for IBA, ConremporaryClassic and Classic cocktails
        cocktails_and_tags = self.cocktails.explode('tags')
        result_df = self.cocktails_and_ingredients.set_index('cocktail_name').join(
            cocktails_and_tags.set_index('name')[['tags']], how='left')

        iba_ingrs = result_df[result_df['tags'] == 'IBA']['ingredient_name'].value_counts().head(5)
        conclassic_ingrs = result_df[result_df['tags'] == 'ContemporaryClassic']['ingredient_name'].value_counts().head(
            5)
        classic_ingrs = result_df[result_df['tags'] == 'Classic']['ingredient_name'].value_counts().head(5)

        # Create subplots: 1 row and 3 columns
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Plot for IBA ingredients
        axes[0].bar(iba_ingrs.index, iba_ingrs.values, color='skyblue')
        axes[0].set_title('Most Used Ingredients - IBA')
        axes[0].set_xlabel('Ingredient')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)

        # Plot for ContemporaryClassic ingredients
        axes[1].bar(conclassic_ingrs.index, conclassic_ingrs.values, color='lightcoral')
        axes[1].set_title('Most Used Ingredients - ContemporaryClassic')
        axes[1].set_xlabel('Ingredient')
        axes[1].set_ylabel('Count')
        axes[1].tick_params(axis='x', rotation=45)

        # Plot for Classic ingredients
        axes[2].bar(classic_ingrs.index, classic_ingrs.values, color='lightgreen')
        axes[2].set_title('Most Used Ingredients - Classic')
        axes[2].set_xlabel('Ingredient')
        axes[2].set_ylabel('Count')
        axes[2].tick_params(axis='x', rotation=45)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Show the plots
        plt.show()

    def plot_abv_disribution_by_num_of_ingredients(self):
        # ABV of cocktails distribution by number of ingredients
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=self.cocktails, x='num_ingredients', y='abv')
        plt.xlabel('Number of Ingredients')
        plt.ylabel('ABV')
        plt.title('ABV Distribution by Number of Ingredients')
        plt.grid(True)
        plt.show()
