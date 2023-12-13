import networkx as nx
import matplotlib.pyplot as plt
import csv

def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return int(float(value))

# Read the graph input file in CSV format
with open('network_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    graph_lines = list(reader)

# Extracting the number of nodes
num_nodes = convert_to_int(graph_lines[0][0])

# Create a graph
G = nx.Graph()

# Add edges to the graph
for line in graph_lines[1:]:
    # Clean up the line by removing non-breaking spaces
    cleaned_line = [item.replace('\xa0', '') for item in line]
    
    # Convert values to integers
    edge_data = list(map(convert_to_int, cleaned_line))
    G.add_edge(edge_data[0], edge_data[1], weight=edge_data[2])

# Read the driver information from another CSV file
with open('driver_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    driver_lines = list(reader)

# Extract the number of drivers
num_drivers = convert_to_int(driver_lines[0][0])

# Create a list to store the driver locations
driver_locations = {}

# Add drivers to their source locations
for i, line in enumerate(driver_lines[1:], start=1):
    source, destination = map(convert_to_int, line)
    driver_locations[i] = (source, destination)

# Draw the graph with drivers
pos = nx.spring_layout(G)  # You can choose a different layout if needed

# Draw the graph
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black')

# Add edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Add drivers to the graph
for driver_id, (source, destination) in driver_locations.items():
    # Label source vertex
    plt.text(pos[source][0], pos[source][1], f'{driver_id}', fontsize=12, ha='right', va='bottom', color='red')

    # Label destination vertex
    plt.text(pos[destination][0], pos[destination][1], f'{driver_id}\'', fontsize=12, ha='right', va='bottom', color='red')

# Show the plot
plt.show()
