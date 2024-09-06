import os
import json
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from flask import Flask, jsonify, session, request
from flask_cors import CORS
import requests, string, random
from scipy import io
from create_training_model import model_training
from sklearn.metrics.pairwise import cosine_similarity
from scipy import io
import numpy as np
import logging, shutil, pickle

app = Flask(__name__)
cors = CORS(app)

query_matrix = io.mmread('sparse_matrix.mtx')
with open('tfidf_recomender.pkl', 'rb') as f:
    tfidf = pickle.load(f)


def clean_string(o):
    return str(o).replace(" ", "_").replace("\n", "_")

def preprocess_input(data):
    acc_list = []
    for d in data['Project Data']:
        for i in data['Project Data'][d]:
            if d not in ['Add Participants',' Select Typicals ']:
                print(data['Project Data'][d][i])
                acc_list.append(f"{clean_string(d)}__{clean_string(data['Project Data'][d][i])}")

    return acc_list


@app.route('/train_model', methods=['POST'])
def train_model():
    json_directory = r'C:\Users\z004scne\Desktop\Collabrative filtering\JSON_FROM_DOCX'
    return model_training(json_directory)

@app.route('/recommend', methods=['POST'])
def recommend():
    json_file = '2. TocLst_20201204100549_1.json'
    with open(json_file, 'r') as file:
        data = json.load(file)

    with open('acc.json', 'r') as file:
        acc = json.load(file)
    # print(data)
    preprocessed_inp = preprocess_input(data)
    print("procee---->",preprocessed_inp)
    # for d in data['Project Data']:
    #     for i in data['Project Data'][d]:
    #         if d not in ['Add Participants',' Select Typicals ']:
    #             print(data['Project Data'][d][i])
                # sims = cosine_similarity(query_matrix, tfidf.transform([str(data['Project Data'][d][i])])).max(axis=0)
                # print("sims -- ",sims)
                # idx = np.argsort(sims)[::-1]
                # print("idx--->",idx)
    rec_list = []
    for acc1 in preprocessed_inp:
        question_matrix = tfidf.transform([acc1])
        print("query_matrix---->",query_matrix.shape)
        print("question_matrix---->",question_matrix.shape)
        rank_values = query_matrix @ question_matrix.T
        print("rank_values -- ",rank_values)
        rank_values = np.array(rank_values.todense()).squeeze()
        print("rank_values ---- ",rank_values)
        top_5 = np.argsort(rank_values)[-5:]
        print("top_5 -- ",top_5)
        print(type(top_5[0]))
        print(f"--------------{acc1}----------")
        resp = {"recommendation": [acc[i] for i in list(top_5)]}
        print(resp)
        rec_list.append({"key":acc1.split("__")[0],
                         "value":acc1.split("__")[1],
                         "recommendation":[acc[i].split("__")[1] for i in list(top_5)]})
    return rec_list
        # print(d)
    return 'sus'


if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')