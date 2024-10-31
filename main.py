import pandas as pd
from sklearn.manifold import TSNE
import plotly.express as px

import preprocessor
from clusterer import Clusterer

cocktails, ingredients, cocktails_and_ingredients = preprocessor.preprocess()

clr = Clusterer(cocktails, ingredients, cocktails_and_ingredients)

cocktails_matrix = clr.generate_cocktails_and_ingredients_matrix_with_volumes()
cocktails_matrix = clr.transform_matrix(cocktails_matrix)
cocktails_and_main_ingr_type = clr.generate_table_with_cocktails_and_their_main_ingr_type()

cocktails_and_main_ingr_type.reset_index(inplace=True)

print(cocktails_and_main_ingr_type.index)

# Create a color mapping for primary alcohol types
color_map = {
    'Brandy': 'blue',
    'Liqueur': 'orange',
    'Gin': 'green',
    'Whiskey': 'red',
    'Fortified Wine': 'purple',
    'Rum': 'brown',
    'Whisky': 'pink',
    'Vodka': 'gray',
    'Spirit': 'cyan',
    'Wine': 'lime',
    'Bitter': 'olive'
}

tsne = TSNE(random_state=42)
cocktails_coords = tsne.fit_transform(cocktails_matrix)

cocktail_df = pd.DataFrame(cocktails_coords, columns=['x', 'y'])
cocktail_df['cocktail_name'] = cocktails_matrix.index
cocktail_df['labels'] = cocktails_and_main_ingr_type['primary_alcohol_type']  # Add cluster labels

# Create the interactive scatter plot with colors
fig = px.scatter(cocktail_df, x='x', y='y',
                 text='cocktail_name',
                 color='labels',
                 title="AAA",
                 color_discrete_map=color_map,
                 width=1200,  # Set the width of the figure
                 height=800)  # Set the height of the figure  # Set discrete colors

fig.update_traces(textposition='top center')  # Adjust text position
fig.show()

print(cocktail_df.index)
