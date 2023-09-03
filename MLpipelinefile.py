import pandas as pd
import numpy as np
import random
import networkx as nx
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from node2vec import Node2Vec
#this bit is for the sql database to work 
import sqlite3

with open(r"C:\Users\User\Documents\Excel Practice\OneDrive\Documents\LinkPredictionProject\fb-pages-food\fb-pages-food.nodes", encoding="utf-8") as nodes: 
    fb_nodes = nodes.read().splitlines() 
    number_of_nodes = len(fb_nodes)
with open(r"C:\Users\User\Documents\Excel Practice\OneDrive\Documents\LinkPredictionProject\fb-pages-food\fb-pages-food.edges") as edges:
    fb_links = edges.read().splitlines() 
    number_of_edges = len(fb_links)

node_list_1 = []
node_list_2 = []

for i in tqdm(fb_links):
  node_list_1.append(i.split(',')[0])
  node_list_2.append(i.split(',')[1])

fb_df = pd.DataFrame({'node_1': node_list_1, 'node_2': node_list_2})

G = nx.from_pandas_edgelist(fb_df, "node_1", "node_2", create_using=nx.Graph())

node_list = node_list_1 + node_list_2

node_list = list(dict.fromkeys(node_list))

adj_G = nx.to_numpy_matrix(G, nodelist = node_list)
all_unconnected_pairs = []

offset = 0
for i in tqdm(range(adj_G.shape[0])):
  for j in range(offset,adj_G.shape[1]):
    if i != j:
      if nx.shortest_path_length(G, str(i), str(j)) <=2:
        if adj_G[i,j] == 0:
          all_unconnected_pairs.append([node_list[i],node_list[j]])

  offset = offset + 1

node_1_unlinked = [i[0] for i in all_unconnected_pairs]
node_2_unlinked = [i[1] for i in all_unconnected_pairs]

data = pd.DataFrame({'node_1':node_1_unlinked, 
                     'node_2':node_2_unlinked})

data['link'] = 0

initial_node_count = len(G.nodes)

fb_df_temp = fb_df.copy()

omissible_links_index = []

for i in tqdm(fb_df.index.values):
  
  G_temp = nx.from_pandas_edgelist(fb_df_temp.drop(index = i), "node_1", "node_2", create_using=nx.Graph())
  
  if (nx.number_connected_components(G_temp) == 1) and (len(G_temp.nodes) == initial_node_count):
    omissible_links_index.append(i)
    fb_df_temp = fb_df_temp.drop(index = i)

fb_df_ghost = fb_df.loc[omissible_links_index]

fb_df_ghost['link'] = 1
data = pd.concat([fb_df_ghost[['node_1', 'node_2', 'link']],data], ignore_index=True)


distribution = data['link'].value_counts()

fb_df_partial = fb_df.drop(index=fb_df_ghost.index.values)

G_data = nx.from_pandas_edgelist(fb_df_partial, "node_1", "node_2", create_using=nx.Graph())

node2vec = Node2Vec(G_data, dimensions=100, walk_length=16, num_walks=50)

n2w_model = node2vec.fit(window=7, min_count=1)

x = []

#retrieving the node embeddings from the node mubers 
for i, j in zip(data['node_1'], data['node_2']):
        vector_i = n2w_model.wv[str(i)]
        vector_j = n2w_model.wv[str(j)]
        x.append(vector_i + vector_j)
    

xtrain, xtest, ytrain, ytest = train_test_split(np.array(x), data['link'], 
                                                test_size = 0.3, 
                                                random_state = 35)

lr = LogisticRegression(max_iter=100000,class_weight="balanced")

lr.fit(xtrain, ytrain)
#we have to somehow make the predictions array tell us which node pairing the probabilities
#correspond to. This code is my addition to this code! new stuff 
predictions = lr.predict_proba(xtest)
print(predictions)
#this is my attempt at retrieving node numbers from their embeddings in node2vec


# Create an array to store both node pairings and probabilities
result_df = pd.DataFrame(columns=['node_1', 'node_2', 'probability'])

# Assuming you have already trained your logistic regression model and obtained predictions
# predictions = lr.predict_proba(xtest)

# Create an array to store both node pairings and probabilities
node_pairings_and_probs = []

# Iterate through the test set and predictions to associate them. I came up with replacing 
#"xtest[:,0]", and "xtest[:,1]" with "data['node_1']", and "data['node_2']", and it works to show the 
#actual node numbers!!!
for (node_1, node_2), probs in zip(zip(data['node_1'], data['node_2']), predictions):
    node_pairings_and_probs.append((node_1, node_2, probs[1]))  # Using probs[1] for the probability of having a link

# Create a DataFrame from the array
result_df = pd.DataFrame(node_pairings_and_probs, columns=['node_1', 'node_2', 'probability'])

# Now, result_df contains the node pairings along with their probabiliti

    #node_pairings_and_probs.append((node_1, node_2, probs[1]))  # Using probs[1] for the probability of having a link

# Create a DataFrame from the array


# Now, result_df contains the node pairings along with their probabilities
print(result_df)


#this code works, but it gives the vector encoding of the nodes instead of the nodes themselves!!!
#print(xtest)
#xtest is the array where all the random walks are stored!!! crazy 
result_list = [(row['node_1'], row['probability']) for _, row in result_df.iterrows()]
#trying it as a list instead of a data frame 
#this actually works!!!! insane stuff!!!

#this gives the node numbers as the output instead of the embeddings! hopefully will get there 
#anyway

# Assuming you have the result_df DataFrame

#gonna try this in SQL instead and import it into python!!!! cool 
conn = sqlite3.connect('linkprediction.db')
cursor = conn.cursor()
result_df.to_sql('result_table', conn, if_exists='replace', index=False)

# Execute the SQL query on the SQLite table
query = '''
    SELECT *
    FROM result_table
    WHERE node_1 = 4 OR node_2 = 4
    ORDER BY probability DESC;
'''

# Fetch the query result into a new DataFrame
filtered_df = pd.read_sql_query(query, conn)

# Commit the changes (if any)
conn.commit()
conn.close()

print(filtered_df.head(5))
#this works!! now you just need to create the data scraper 