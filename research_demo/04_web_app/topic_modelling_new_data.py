import streamlit as st

st.set_page_config(page_title='Demo: Topic Modeling Of News')

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# loading preprocessing pipeline and models
import joblib

# from scikit-learn
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

# from wordcloud
from wordcloud import WordCloud

# from pyLDAvis
import pyLDAvis.lda_model

ROOT_PATH = Path('research_demo/04_web_app')

def load_data() -> pd.DataFrame:
    """ Loads the dataset with news data for topic modeling """
    pred = pd.read_csv(ROOT_PATH / '00_pred_raw.csv', index_col=None)
    pred.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
    return pred

def execute_preprocessing_pipe(pred) -> pd.DataFrame:
    """ Loads the preprocessing pipeline and processes the news dataframe """
    with st.status("Load preprocessing pipeline and transform data..", expanded=True) as status:
        topic_pipe = joblib.load(ROOT_PATH / 'topic_pipe_nosplit.joblib')
        pred_preprocessed =  topic_pipe.transform(pred)
        status.update(label="Preprocessing completed!", state="complete", expanded=False)
        return pred_preprocessed

def run_demo(model_name, model,cv, feature):
    """ Runs the demo with the selected model and input feature"""

    # Load the dataset with news data for topic modeling
    st.subheader("Loading raw data")
    pred = pd.read_csv(ROOT_PATH / '00_pred_raw.csv')
    pred.drop(columns=['Unnamed: 0'], axis=1, inplace=True)

    # show dataframe
    st.dataframe(pred)

    # execute preprocessing pipeline
    st.subheader("Preprocessing data")
    pred_preprocessed = execute_preprocessing_pipe(pred)

    # show preprocessed data
    st.dataframe(pred_preprocessed)

    # predicting topics with LDA model
    st.subheader(f'Predict {model_name} on feature {feature}')

    # create DTM from given feature
    dtm = cv.transform(pred_preprocessed[feature])

    # show most important words of topics found
    for index, topic in enumerate(model.components_):
        st.write(f'Die TOP-15 Wörter für das Thema #{index}')
        st.write([cv.get_feature_names_out()[i] for i in topic.argsort()[-15:]])

    # predict topics on corpus
    topic_results = model.transform(dtm)
    pred_preprocessed['topic'] = topic_results.argmax(axis=1)

    # show dataset with topics
    st.dataframe(pred_preprocessed)


def main():
    """ A simple demo app for Topic Modeling of News headlines"""

    # show title
    st.title("Demo: Topic Modeling with Latent Dirichlet Allocation On News Headlines")

    # show menu
    menu = ["Run the demo", "Evaluation / Visualization"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Run the demo":

        # show options for model selection
        features_choice = st.sidebar.radio("Select input features", ("title", "title, description and text"))
        topics = ["4 topics", "6 topics", "7 topics", "8 topics"]
        topics_choice = st.sidebar.selectbox("Select number of topics", topics)

        feature = None
        cv = None
        if features_choice == "title":
            feature = 'title_cleaned'
            cv = joblib.load(ROOT_PATH / 'models/cv.jl')
        elif features_choice == "title, description and text":
            feature = 'title_description_text_cleaned'
            cv = joblib.load(ROOT_PATH / 'models/cv_combined.jl')

        lda_model = None
        model_map_title = {'4 topics' : 'lda_model_4_topics.jl',
                           '6 topics' : 'lda_model_6_topics.jl',
                           '7 topics' : 'lda_model_7_topics.jl',
                           '8 topics' : 'lda_model_8_topics.jl'}
        model_map_combined = {'4 topics' : 'lda_model_4_topics_combined.jl',
                           '6 topics' : 'lda_model_6_topics_combined.jl',
                           '7 topics' : 'lda_model_7_topics_combined.jl',
                           '8 topics' : 'lda_model_8_topics_combined.jl'}

        model_path = None
        if feature == 'title_cleaned':
            model_path = ROOT_PATH / 'models' / model_map_title[topics_choice]
        elif feature == 'title_description_text_cleaned':
            model_path = ROOT_PATH / 'models' / model_map_combined[topics_choice]
        lda_model = joblib.load(model_path)


        st.write("This application shows the processing pipeline for predicting topics of news data from a trained "
                "model using Latent Dirichlet Allocation (LDA). ")
        st.write("For more info on this project check "
                "[project website](http://portfolio.manuelarink.de/2023/10/20/topic-modelling-of-news-with-latent-dirichlet-allocation/).")
        st.info("To use this demo: On the sidebar left, select the input features from which the model was trained. "
                "You can choose to use just the headline title or a combination of the headline title, "
                "description and text. "
                "Select the number of topics that you want to extract using LDA. "
                "Press the button to start the demo. Please note that data processing may take some time. "
                "Use the table slider to view all columns.")


        if st.button("Start demo", key='start_demo'):
            run_demo(topics_choice, lda_model, cv, feature)


    elif choice == "Evaluation / Visualization":
        st.subheader("Evaluation and Visualization of the results of LDA")
        st.info('Work on this is still in progress - please visit later.')



if __name__ == '__main__':
    main()