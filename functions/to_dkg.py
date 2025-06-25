import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, RoutingControl, Result

# load secrets from .env file
load_dotenv()
dkg_admin = os.getenv("DKG_ADMIN")
dkg_admin_password = os.getenv("DKG_ADMIN_PASSWORD")
dkg_url = os.getenv("DKG_URL")

# Define and check connection of DKG
url = dkg_url
user = dkg_admin # your username
password = dkg_admin_password # your password
db_name = "neo4j" # or your db name
driver = GraphDatabase.driver(url, auth=(user, password))
driver.verify_connectivity()

# Split dataframe into chunks
def split_dataframe(dataframe, chunk_size = 5000): 
    chunks = list()
    num_chunks = len(dataframe) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(dataframe[i*chunk_size:(i+1)*chunk_size])
    return chunks

# Update nodes in Neo4j with chunks
def update_nodes(dataframe, label):
    with driver.session() as session:
        # Cypher query to create nodes with properties if they don't exist. Update properties if the node exists.
        node_query = (
                f"UNWIND $rows as row MERGE (n:{label} {{id:row.id}}) ON CREATE SET n = row ON MATCH SET n = row"
            )
        for chunk in split_dataframe(dataframe):
            session.run(node_query, rows = chunk.to_dict('records'))

# Update RELATION edges in Neo4j with chunks
def update_relations(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
                f"UNWIND $rows as row "
                f"MATCH (n:Asset), (m:Asset) "
                f"WHERE n.id = row.source_asset_id AND m.id = row.target_asset_id "
                f"MERGE (n)-[r:RELATION]->(m) "
                f"SET r = row "
                f"REMOVE r.source_asset_id, r.target_asset_id"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))                
