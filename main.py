import streamlit as st
from bs4 import BeautifulSoup
import requests
from streamlit_gsheets import GSheetsConnection
import pandas as pd

if st.button("Clear Cache"):
    st.cache_data.clear()
    
conn = st.connection('gsheets', type=GSheetsConnection)

tab1, tab2, tab3 = st.tabs(["Levels", "Entities", "Objects"])

# Function to clean and extract unique tags
def get_unique_tags(df, tag_column='Tags'):
    unique_tags = set()
    for tags in df[tag_column].dropna():
        for tag in tags.split(','):
            cleaned_tag = tag.strip().strip("[]'\"")
            unique_tags.add(cleaned_tag)
    return sorted(unique_tags)

# Function to apply filters
def apply_filters(df, selected_tags, rating_range, tag_filter_type='OR', tag_column='Tags'):
    if selected_tags:
        if tag_filter_type == 'AND':
            df = df[df[tag_column].apply(lambda x: all(tag in x for tag in selected_tags) if pd.notna(x) else False)]
        elif tag_filter_type == 'OR':
            df = df[df[tag_column].apply(lambda x: any(tag in x for tag in selected_tags) if pd.notna(x) else False)]
    
    df = df[(df['Rating'] >= rating_range[0]) & (df['Rating'] <= rating_range[1])]
    
    return df

with tab1:
    df1 = conn.read(worksheet='Backrooms_db')
    df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
    df1 = df1[df1['Level'].notna()]

    # Class filter with default "All Classes"
    all_classes = ['All Classes'] + list(df1['Class'].dropna().unique())
    selected_class = st.selectbox("Select Class", options=all_classes, index=0)

    # Tags filter
    unique_tags = get_unique_tags(df1)
    selected_tags = st.multiselect("Select Tags", options=unique_tags)

    # Tag filter type
    tag_filter_type = st.radio("Tag Filter Type", ['AND', 'OR'])

    # Rating slider
    min_rating, max_rating = df1['Rating'].min(), df1['Rating'].max()
    rating_range = st.slider("Select Rating Range", min_rating, max_rating, (min_rating, max_rating))

    # Apply filters
    if selected_class != 'All Classes':
        df1 = df1[df1['Class'] == selected_class]

    df1 = apply_filters(df1, selected_tags, rating_range, tag_filter_type)
    
    st.dataframe(df1)

with tab2:
    df2 = conn.read(worksheet='Backrooms_entities_db')
    df2 = df2.loc[:, ~df2.columns.str.contains('^Unnamed')]
    df2 = df2[df2['Level'].notna()]

    # Tags filter
    unique_tags = get_unique_tags(df2)
    selected_tags = st.multiselect("Select Tags", options=unique_tags, key='tags2')

    # Tag filter type
    tag_filter_type = st.radio("Tag Filter Type", ['AND', 'OR'], key='tag_filter_type2')

    # Rating slider
    min_rating, max_rating = df2['Rating'].min(), df2['Rating'].max()
    rating_range = st.slider("Select Rating Range", min_rating, max_rating, (min_rating, max_rating), key='rating2')

    # Apply filters
    df2 = apply_filters(df2, selected_tags, rating_range, tag_filter_type)
    
    st.dataframe(df2)
    
with tab3:
    df3 = conn.read(worksheet='Backrooms_objects_db')
    df3 = df3.loc[:, ~df3.columns.str.contains('^Unnamed')]
    df3 = df3[df3['Level'].notna()]

    # Tags filter
    unique_tags = get_unique_tags(df3)
    selected_tags = st.multiselect("Select Tags", options=unique_tags, key='tags3')

    # Tag filter type
    tag_filter_type = st.radio("Tag Filter Type", ['AND', 'OR'], key='tag_filter_type3')

    # Rating slider
    min_rating, max_rating = df3['Rating'].min(), df3['Rating'].max()
    rating_range = st.slider("Select Rating Range", min_rating, max_rating, (min_rating, max_rating), key='rating3')

    # Apply filters
    df3 = apply_filters(df3, selected_tags, rating_range, tag_filter_type)
    
    st.dataframe(df3)
