# Function to generate asset UUID
import uuid
def asset_uuid(row):
    namespace_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, row['type_name'])  
    asset_source_id = str(row['asset_source_id'])
    return uuid.uuid5(namespace_uuid, asset_source_id)

# Function to generate attribute UUID
def attr_uuid(row):
    namespace_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, row['type_name'])  
    asset_id = str(row['asset_id'])
    return uuid.uuid5(namespace_uuid, asset_id)

# Function to generate relation UUID
def rel_uuid(row):
    namespace_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, row['type_name'])  
    asset_comp = str(row['source_asset_id']) + str(row['target_asset_id'])
    return uuid.uuid5(namespace_uuid, asset_comp)

# Function to create display name in title case from name
def display_name(name):
    # Check if the name contains underscore
    if '_' in name:
        # Split the name by underscore
        words = name.split('_')
    else:
        # Split the name by space
        words = name.split(' ')
    
    # Capitalize each word
    words = [word.title() for word in words]
    
    # Join the words with space
    display_name = ' '.join(words)
    
    return display_name
