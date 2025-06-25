import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, RoutingControl, Result

# load secrets from .env file
load_dotenv()
onto_admin = os.getenv("ONTO_ADMIN")
onto_admin_password = os.getenv("ONTO_ADMIN_PASSWORD")
onto_url = os.getenv("ONTO_URL")

# Define and check connection of DKG
uri = onto_url
user = onto_admin # your username
password = onto_admin_password # your password
db_name = "neo4j"
driver = GraphDatabase.driver(uri, auth=(user, password))
driver.verify_connectivity()

# Split dataframe into chunks
def split_dataframe(dataframe, chunk_size = 5000): 
    chunks = list()
    num_chunks = len(dataframe) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(dataframe[i*chunk_size:(i+1)*chunk_size])
    return chunks

# Update nodes in Neo4j With chunks
def onto_nodes(dataframe, label):
    with driver.session() as session:
        # Cypher query to create nodes with properties if they don't exist. Update properties if the node exists.
        node_query = (
                f"unwind $rows as row MERGE (n:{label} {{id:row.id}}) ON CREATE SET n = row ON MATCH SET n = row"
            )
        for chunk in split_dataframe(dataframe):
            session.run(node_query, rows = chunk.to_dict('records'))

# Update RelationType edges in Neo4j With chunks
def onto_relations(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
            f"unwind $rows as row "
                f"MATCH (n:AssetType), (m:AssetType) "
                f"WHERE n.name = row.source_asset_type_name AND m.name = row.target_asset_type_name "
                f"MERGE (n)-[r:RelationType]->(m) "
                f"SET r = row "
                f"REMOVE r.source_asset_type_name, r.target_asset_type_name"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))

# Update other edges in Neo4j With chunks
def is_source_of(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
            f"unwind $rows as row "
                f"MATCH (n:MetadataSource), (m:AssetArea) "
                f"WHERE n.name = row.metadata_source_name AND m.name = row.name "
                f"MERGE (n)-[r:IS_SOURCE_OF]->(m)"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))

def in_area(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
            f"unwind $rows as row "
                f"MATCH (n:AssetType), (m:AssetArea) "
                f"WHERE n.name = row.name AND m.name = row.asset_area_name "
                f"MERGE (n)-[r:IN_AREA]->(m)"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))

def assign_attribute(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
            f"unwind $rows as row "
                f"MATCH (n:AssetType), (m:AttributeType) "
                f"WHERE m.name = row.name AND n.name = row.asset_type_name "
                f"MERGE (m)-[r:IS_ASSIGNED_TO]->(n)"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))

def assign_area(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
            f"unwind $rows as row "
                f"MATCH (n:AssetType), (m:AssetAreaType) "
                f"WHERE m.name = row.name AND n.name = row.asset_area_type_name "
                f"MERGE (n)-[r:IS_ASSIGNED_TO]->(m)"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))

def instance_of(dataframe):
    with driver.session() as session:
        # Cypher query to create edges with properties if they don't exist. Update properties if the edge exists.
        edge_query = (
            f"unwind $rows as row "
                f"MATCH (n:AssetArea), (m:AssetAreaType) "
                f"WHERE n.name = row.name AND m.name = row.type_name "
                f"MERGE (n)-[r:IS_INSTANCE_OF]->(m)"
                    )
        for chunk in split_dataframe(dataframe):
            session.run(edge_query, rows = chunk.to_dict('records'))

# Update schema nodes in Neo4j with chunks
def schema_nodes(dataframe, label):
    with driver.session() as session:
        # Cypher query to create nodes with properties if they don't exist. Update properties if the node exists.
        node_query = (
                f"UNWIND $rows as row MERGE (n:{label}) ON CREATE SET n = row ON MATCH SET n = row"
            )
        for chunk in split_dataframe(dataframe):
            session.run(node_query, rows = chunk.to_dict('records'))