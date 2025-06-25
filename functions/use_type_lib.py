import pandas as pd
from functions import asset_uuid, attr_uuid, rel_uuid, display_name

def get_asset_info(df, type_name, ms_name, asset_types, date):
    ''' Populate the Asset information depending on the type and metadata source '''
    df['display_name'] = df['name'].apply(display_name)
    df['at_ms'] = type_name + '-' + ms_name
    df['type_id'] = df['at_ms'].map(asset_types.set_index('at_ms')['id'])
    df['type_name'] = type_name
    df['metadata_source_name'] = ms_name
    df['metadata_source_id'] = df['at_ms'].map(asset_types.set_index('at_ms')['metadata_source_id'])
    df['asset_area_id'] = df['at_ms'].map(asset_types.set_index('at_ms')['asset_area_id'])
    df['asset_area_name'] = df['at_ms'].map(asset_types.set_index('at_ms')['asset_area_name'])
    df['id'] = df.apply(asset_uuid, axis=1)
    df['id'] = df['id'].apply(str)
    df['ingestion_time'] = date
    return df

def transform_attr(df_asset, columns_to_transpose, attribute_types):
    ''' Transform the attributes '''
    attr_df = pd.melt(df_asset, id_vars=['id', 'created_on','created_by','last_modified_by','last_modified_on', 'ingestion_time'], 
                      value_vars=columns_to_transpose, var_name='type_name', value_name='value')
    attr_df.rename(columns={'id':'asset_id'}, inplace=True)
    attr_df['id'] = attr_df.apply(attr_uuid, axis=1)
    attr_df['id'] = attr_df['id'].apply(str)
    attr_df['type_id'] = attr_df['type_name'].map(attribute_types.set_index('name')['id'])
    attr_df['data_type'] = attr_df['type_name'].map(attribute_types.set_index('name')['data_type'])
    attr_df['type_display_name'] = attr_df['type_name'].map(attribute_types.set_index('name')['display_name'])
    attr_df = attr_df.dropna(subset=['value'])
    return attr_df

def transform_rel(df_source, df_target, target_asset_col_name, source_asset_type, target_asset_type, relation_types, date):
    ''' Transform the relations '''
    rel_df = pd.DataFrame(df_source[['id', target_asset_col_name, 'created_by', 'created_on', 'last_modified_by', 'last_modified_on']].copy())
    rel_df['concat_string'] = source_asset_type + '-' + target_asset_type
    rel_df['type_id'] = rel_df['concat_string'].map(relation_types.set_index('concat_string')['id'])
    rel_df['type_name'] = rel_df['concat_string'].map(relation_types.set_index('concat_string')['name'])
    rel_df['type_display_name'] = rel_df['concat_string'].map(relation_types.set_index('concat_string')['display_name'])
    rel_df['target_asset_id'] = rel_df[target_asset_col_name].map(df_target.set_index('name')['id'])
    rel_df.rename(columns={'id': 'source_asset_id'}, inplace=True)
    rel_df['id'] = rel_df.apply(lambda row: rel_uuid(row), axis=1)
    rel_df['id'] = rel_df['id'].astype(str)
    rel_df.drop(columns=['concat_string', target_asset_col_name], inplace=True)
    rel_df['ingestion_time'] = date
    return rel_df

def transform_rel_rev(df_source, df_target, source_asset_col_name, source_asset_type, target_asset_type, relation_types, date):
    ''' Transform the relations '''
    rel_df = pd.DataFrame(df_target[['id', source_asset_col_name, 'created_by', 'created_on', 'last_modified_by', 'last_modified_on']].copy())
    rel_df['concat_string'] = source_asset_type + '-' + target_asset_type
    rel_df['type_id'] = rel_df['concat_string'].map(relation_types.set_index('concat_string')['id'])
    rel_df['type_name'] = rel_df['concat_string'].map(relation_types.set_index('concat_string')['name'])
    rel_df['type_display_name'] = rel_df['concat_string'].map(relation_types.set_index('concat_string')['display_name'])
    rel_df['source_asset_id'] = rel_df[source_asset_col_name].map(df_source.set_index('name')['id'])
    rel_df.rename(columns={'id': 'target_asset_id'}, inplace=True)
    rel_df['id'] = rel_df.apply(lambda row: rel_uuid(row), axis=1)
    rel_df['id'] = rel_df['id'].astype(str)
    rel_df.drop(columns=['concat_string', source_asset_col_name], inplace=True)
    rel_df['ingestion_time'] = date
    return rel_df
