import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Plotter:
    """
    A class to generate various plots related to cocktails, ingredients, and their properties.
    """

    def __init__(self, cocktails, ingredients, cocktails_and_ingredients):
        self.cocktails = cocktails
        self.ingredients = ingredients
        self.cocktails_and_ingredients = cocktails_and_ingredients

    # Cocktails
    def plot_cocktail_categories(self):
        """
        Plots a pie chart of cocktail categories with the distribution of each category.
        """
        top_categories = self.cocktails['category'].value_counts()

        plt.figure(figsize=(12, 6))

        wedges, texts, autotexts = plt.pie(top_categories, labels=top_categories.index, autopct='%1.1f%%',
                                           startangle=180, colors=sns.color_palette('coolwarm', len(top_categories)))

        plt.title('Cocktails Categories')

        legend_labels = [f'{count} cocktails' for count in top_categories]

        plt.legend(wedges, legend_labels, title="Number of Cocktails", loc="upper right", bbox_to_anchor=(1.1, 1))

        plt.show()

    def plot_cocktails_preparation_methods(self):
        """
        Plots a pie chart showing the distribution of different preparation methods used for cocktails.
        """

        prep_methods = self.cocktails['prep_method'].value_counts()

        plt.figure(figsize=(12, 6))

        wedges, texts, autotexts = plt.pie(prep_methods, labels=prep_methods.index, autopct='%1.1f%%', startangle=200,
                                           colors=sns.color_palette('coolwarm', len(prep_methods)))

        plt.title('Cocktails methods of preparation')

        legend_labels = [f'{count} cocktails' for count in prep_methods]

        plt.legend(wedges, legend_labels, title="Number of Cocktails", loc="upper right", bbox_to_anchor=(1.1, 1))

        plt.show()

    def plot_cocktail_glasses(self):
        """
        Plots a horizontal bar chart showing the percentage of cocktails served in different types of glasses.
        """

        top_categories = self.cocktails['glass'].value_counts()

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x=top_categories.values / len(self.cocktails) * 100, y=top_categories.index,
                         palette='coolwarm',
                         hue=top_categories.index)

        plt.xlabel('Cocktails(%)')
        plt.ylabel('Glass')
        plt.title('Cocktails Glasses')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f%%')

        plt.show()

    def plot_cocktail_instruction_lengths(self, n_cocktails):
        """
         Plots a bar chart showing the top N cocktails with the longest instruction lengths.

         :param n_cocktails: Number of cocktails to include in the plot.
         """

        hardest_cocktails = self.cocktails.sort_values(ascending=False, by='instruction_length').head(n_cocktails)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=hardest_cocktails['instruction_length'], y=hardest_cocktails['name'], palette='coolwarm',
                    hue=hardest_cocktails['name'])

        plt.ylabel('Cocktails')
        plt.xlabel('Instruction length')
        plt.title(f'Top {n_cocktails} Cocktails by instruction length')

        plt.show()

    def plot_cocktails_with_largest_amount_of_ingredients(self, n_cocktails):
        """
         Plots a bar chart showing the top N cocktails with the largest number of ingredients.

         :param n_cocktails: Number of cocktails to include in the plot.
         """
        top_n = 30
        hardest_cocktails = self.cocktails.sort_values(ascending=False, by='num_ingredients').head(top_n)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=hardest_cocktails['num_ingredients'], y=hardest_cocktails['name'], palette='coolwarm',
                    hue=hardest_cocktails['name'])

        plt.ylabel('Cocktails')
        plt.xlabel('Num of ingredients')
        plt.title(f'Top {top_n} cocktails by ingredients number')

        plt.show()

    def plot_cocktails_rank_by_abv(self, n_cocktails, strongest=True):
        """
        Plots a bar chart showing the top N cocktails by ABV, either strongest or weakest.

        :param n_cocktails: Number of cocktails to include in the plot.
        :param strongest: If True, plots the strongest cocktails; if False, plots the weakest.
        """
        cocktails = self.cocktails.sort_values(ascending=not strongest, by='abv').head(n_cocktails)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=cocktails['abv'], y=cocktails['name'], palette='coolwarm',
                    hue=cocktails['name'])

        plt.ylabel('Cocktails')
        plt.xlabel('ABV(%)')
        if strongest:
            plt.title(f'Top {n_cocktails} Strongest Cocktails')
        else:
            plt.title(f'Top {n_cocktails} Weakest Cocktails')

        plt.show()

    def plot_cocktails_strength_distribution(self):
        """
         Plots a bar chart and a pie chart showing the distribution of cocktails by strength category.
         """

        strengths = self.cocktails['strength'].value_counts()

        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        sns.barplot(y=strengths.values, x=strengths.index, hue=strengths.values, ax=axs[0], legend=False)
        axs[0].set_ylabel('Number of Cocktails')
        axs[0].set_xlabel('Strength')
        axs[0].set_title('Cocktails Strength Distribution')

        for i, v in enumerate(strengths.values):
            axs[0].text(i, v, str(v), ha='center', va='bottom')

        strengths = self.cocktails.query('strength != "Unknown"')['strength'].value_counts()

        wedges, texts, autotexts = axs[1].pie(strengths, labels=strengths.index, autopct='%1.1f%%', startangle=195,
                                              colors=sns.color_palette('coolwarm', len(strengths)))

        axs[1].legend(wedges, ['>30%', '20-30%', '10-20%', '<10%'], title="ABV for strength categories", loc="best")

        axs[1].axis('equal')
        axs[1].set_title('Cocktails Strength Distribution (Without Unknowns)')

        plt.tight_layout()
        plt.show()

    # Ingredients
    def plot_ingredient_types_distribution(self):
        """
        Plots a pie chart showing the distribution of different types of ingredients.
        """

        ingredient_counts = self.ingredients['generalized_type'].value_counts()

        plt.figure(figsize=(10, 6))
        plt.pie(ingredient_counts, labels=ingredient_counts.index, autopct='%1.1f%%', startangle=180,
                colors=sns.color_palette('coolwarm', len(ingredient_counts)))

        plt.title('Ingredient types distribution')
        plt.show()

    def plot_most_common_ingredients(self, n_ingredients):
        """
         Plots a bar chart showing the top N most common ingredients used in cocktails.

         :param n_ingredients: Number of ingredients to include in the plot.
         """

        ingredient_counts = self.cocktails_and_ingredients['ingredient_name'].value_counts()

        top_ingredients = ingredient_counts.head(n_ingredients)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_ingredients.values / len(self.cocktails) * 100, y=top_ingredients.index, palette='coolwarm',
                    hue=top_ingredients.index)

        plt.xlabel('Cocktails(%)')
        plt.ylabel('Ingredient')
        plt.title(f'Top {n_ingredients} Most Common Ingredients')

        plt.show()

    def plot_ingredients_co_occurrences(self):
        """
        Plots bar charts showing the most common co-occurring ingredients for different ingredient types.
        """
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
        """
        Plots a bar chart of the top N ingredients by mean used volume, optionally filtered by alcoholic ingredients.

        :param n_ingredients: Number of ingredients to include in the plot.
        :param alcoholic: If True, only includes alcoholic ingredients; otherwise includes all ingredients.
        """
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

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_ingredients.values, y=top_ingredients.index, palette='coolwarm', hue=top_ingredients.index)

        plt.xlabel('Volume Oz')
        plt.ylabel('Ingredient')
        if alcoholic:
            plt.title(f'Top {n_ingredients} Alcoholic Ingredients by Mean Used Volume')
        else:
            plt.title(f'Top {n_ingredients} Ingredients by Mean Used Volume')

        plt.show()

    # Cocktails and ingredients
    def plot_ingredients_frequency_in_every_glass(self):
        """
         Plots a heatmap showing the frequency of each ingredient type in different types of glasses.
         """
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

        ingredients_list = []

        for index, row in self.cocktails.iterrows():
            cocktail_name = row['name']
            glass_type = row['glass']

            ingrs = get_ingredients(cocktail_name)

            for ingredient in ingrs:
                ingredients_list.append({'ingredient': ingredient, 'glass': glass_type})

        df = pd.DataFrame(ingredients_list)

        pivot_table = df.pivot_table(index='ingredient', columns='glass', aggfunc='size', fill_value=0)

        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, cmap='Blues', fmt='g')

        plt.title('Number of Times Each Ingredient Type Appears in every Glass')
        plt.xlabel('Glass Type')
        plt.ylabel('Ingredient')

        plt.show()

    def most_common_ingredients_by_tags(self):
        """
         Plots bar charts for the most common ingredients in different cocktail categories (IBA, ContemporaryClassic, Classic).
         """
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

        plt.tight_layout()

        plt.show()

    def plot_abv_disribution_by_num_of_ingredients(self):
        """
        Plots a boxplot showing the distribution of cocktail ABV by the number of ingredients.
        """
        # ABV of cocktails distribution by number of ingredients
        plt.figure(figsize=(8, 4))
        sns.boxplot(data=self.cocktails, x='num_ingredients', y='abv')
        plt.xlabel('Number of Ingredients')
        plt.ylabel('ABV')
        plt.title('ABV Distribution by Number of Ingredients')
        plt.grid(True)
        plt.show()
