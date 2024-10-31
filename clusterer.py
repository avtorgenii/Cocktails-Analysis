import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

import plotly.express as px
import pandas as pd


class Clusterer:
    def __init__(self, cocktails, ingredients, cocktails_and_ingredients):
        self.cocktails = cocktails
        self.ingredients = ingredients
        self.cocktails_and_ingredients = cocktails_and_ingredients

    def generate_cocktails_and_ingredients_matrix_with_volumes(self):
        volume_df = self.cocktails_and_ingredients[['cocktail_name', 'ingredient_name', 'volume_oz']].fillna(0.01)

        # Create a pivot table to reshape the DataFrame
        cocktail_matrix = volume_df.pivot_table(index='cocktail_name',
                                                columns='ingredient_name',
                                                values='volume_oz',
                                                fill_value=0)
        return cocktail_matrix

    def generate_table_with_cocktails_and_their_main_ingr_type(self):
        # Get main alcohol ingredient for each cocktail
        result_df = self.cocktails_and_ingredients.set_index('cocktail_name').join(
            self.cocktails.set_index('name')[['abv']],
            how='left'
        ).reset_index()  # Reset index to restore 'cocktail_name' as a column

        result_df = self.ingredients[['name', 'type', 'generalized_type']].merge(result_df, left_on='name',
                                                                                 right_on='ingredient_name',
                                                                                 how='inner')

        result_df.dropna(subset=['type'], inplace=True)
        result_df.drop(columns=['name'], inplace=True)

        result_df.sort_values(by='cocktail_name', ascending=True, inplace=True)

        max_volume_type_df = (
            result_df.loc[result_df['generalized_type'] == "Alcoholic"]  # Filter to include only alcoholic ingredients
            .sort_values(by=['cocktail_name', 'volume_oz'], ascending=[True, False])  # Sort by cocktail and volume
            .drop_duplicates(subset=['cocktail_name'], keep='first')
            # Keep the row with the largest volume per cocktail
            [['cocktail_name', 'type']]  # Select only relevant columns
        )

        # Rename column to indicate it's the primary type by volume
        max_volume_type_df.rename(columns={'type': 'primary_alcohol_type'}, inplace=True)

        # Merge this back into the original DataFrame if desired
        result_df = result_df.merge(max_volume_type_df, on='cocktail_name', how='left')

        result_df = result_df[['primary_alcohol_type', 'cocktail_name']]
        result_df.drop_duplicates(inplace=True)
        result_df.reset_index(inplace=True)
        return result_df

    def generate_table_with_cocktails_and_style(self):
        # Create a copy of cocktails table
        cocktails_copy = self.cocktails.copy()

        # Encode Strength(not ABV because we have a lot of missing data for it), glasses and prep_method
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded_features = encoder.fit_transform(cocktails_copy[['glass', 'prep_method', 'strength']])

        encoded_df = pd.DataFrame(
            encoded_features,
            columns=encoder.get_feature_names_out(['glass', 'prep_method', 'strength']),
            index=cocktails_copy.index
        )

        return encoded_df

    def transform_matrix(self, matrix, random_state=42):
        # Initialize the QuantileTransformer
        quantile_transformer = QuantileTransformer(random_state=random_state, n_quantiles=len(matrix))
        transformed_matrix = quantile_transformer.fit_transform(matrix)

        return pd.DataFrame(transformed_matrix, index=matrix.index, columns=matrix.columns)

    def kmeans_clustering(self, transformed_matrix, n_clusters=5, random_state=42):
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        clusters = kmeans.fit_predict(transformed_matrix)

        return clusters

    def plot_pca_decomposition(self, transformed_matrix, labels, color_map, title):
        # Perform PCA for dimensionality reduction
        pca = PCA(n_components=2)
        cocktail_coords = pca.fit_transform(transformed_matrix)

        # Create a DataFrame with PCA results and labels
        cocktail_df = pd.DataFrame(cocktail_coords, columns=['PC1', 'PC2'])
        cocktail_df['cocktail_name'] = transformed_matrix.index
        cocktail_df['labels'] = labels  # Add cluster labels

        # Create the interactive scatter plot with colors
        fig = px.scatter(
            cocktail_df, x='PC1', y='PC2',
            text='cocktail_name',
            color='labels',  # Use cluster labels for color categorization
            title=title,
            color_discrete_map=color_map,  # Apply color map directly
            width=1200,
            height=800
        )

        fig.update_traces(textposition='top center')  # Adjust text position
        fig.show()

    def plot_scree_plot(self, transformed_matrix):
        # Assume cocktail_matrix is your original data (ingredient matrix)
        pca = PCA()
        pca.fit(transformed_matrix)

        # Get the explained variance ratios
        explained_variance = pca.explained_variance_ratio_

        # Create a bar plot for the scree plot
        plt.figure(figsize=(25, 6))
        plt.bar(np.arange(1, len(explained_variance) + 1), explained_variance, color='skyblue', edgecolor='black')
        plt.title('Scree Plot')
        plt.xlabel('Principal Component')
        plt.ylabel('Variance Ratio')
        plt.xticks(np.arange(1, len(explained_variance) + 1))  # Set the x-axis to match component numbers
        plt.grid(True, axis='y')  # Add horizontal grid lines for better readability
        plt.show()

    def plot_tsne_decomposition(self, transformed_matrix, labels, color_map, title, random_state=42):
        tsne = TSNE(random_state=random_state)
        cocktails_coords = tsne.fit_transform(transformed_matrix)

        cocktail_df = pd.DataFrame(cocktails_coords, columns=['x', 'y'])
        cocktail_df['cocktail_name'] = transformed_matrix.index
        cocktail_df['labels'] = labels  # Add cluster labels

        # Create the interactive scatter plot with colors
        fig = px.scatter(cocktail_df, x='x', y='y',
                         text='cocktail_name',
                         color='labels',
                         title=title,
                         color_discrete_map=color_map,
                         width=1200,  # Set the width of the figure
                         height=800)  # Set the height of the figure  # Set discrete colors

        fig.update_traces(textposition='top center')  # Adjust text position
        fig.show()



