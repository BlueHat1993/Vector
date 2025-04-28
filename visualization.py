import chromadb
from chromadb.config import Settings
from sklearn.decomposition import PCA
import plotly.express as px
import textwrap

# Get embeddings
chroma = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma.get_collection("fragments_on_machines")  # Get the collection by name
# Get the embeddings and document IDs from the collection
embeddings = collection.get(include=['embeddings'])['embeddings']
docs = collection.get(include=['embeddings'])['ids']
# Get the data (documents) from the collection
data = collection.get(include=['documents'])['documents']

print(docs)

# Reduce the embedding dimensionality
pca = PCA(n_components=3)
vis_dims = pca.fit_transform(embeddings)

# Create an interactive 3D plot with enhanced visuals
fig = px.scatter_3d(
    x=vis_dims[:, 0],
    y=vis_dims[:, 1],
    z=vis_dims[:, 2],
    text=docs,
    hover_data={'Chunk Data': [textwrap.shorten(chunk, width=50, placeholder="...") for chunk in data]},  # Shorten chunk data text
    labels={'x': 'PCA Component 1', 'y': 'PCA Component 2', 'z': 'PCA Component 3'},
    title='Fragments on Machines embeddings',
    color=vis_dims[:, 0],  # Add color based on the first PCA component
    color_continuous_scale=px.colors.sequential.Viridis  # Use a cool color scale
)
# Set dark mode background
fig.update_layout(
    template='plotly_dark'
)

# Update marker size and opacity for better aesthetics
fig.update_traces(marker=dict(size=5, opacity=0.8))

# Save the plot as an HTML file
fig.write_html("fragments_knowledge_graph.html")