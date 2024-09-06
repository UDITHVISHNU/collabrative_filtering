import os
import json
from scipy import io
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_string(o):
    return str(o).replace(" ", "_").replace("\n", "_")

def prepare_acc_dict(json_contents):
    acc_dict = dict()
    for content in json_contents:
        for js in content:
            for k in content[js]:
                if k not in ['Add Participants',' Select Typicals ']:
                    if k in acc_dict:
                        # acc_dict[k].append(list(set(str(content[js][k]['value']))))
                        acc_list = acc_dict[k]
                        acc_list.append(str(content[js][k]['value']))
                        acc_dict[k] = acc_list
                    else:
                        acc_dict.update({k:[content[js][k]['value']]})

        for acc in acc_dict:
                new_list = []
                for o in acc_dict[acc]:
                    if o not in new_list:
                        if o != "":
                            new_list.append(o)
                acc_dict[acc] = new_list

    return acc_dict

def prepare_sparse_matrix(json_contents):
    acc = []
    for content in json_contents:
        for js in content:
            for k in content[js]:
                if k not in ['Add Participants',' Select Typicals ']:
                    acc.append(f"{clean_string(k)}__{clean_string(str(content[js][k]['value']))}")

    with open('acc.json','w') as f:
        json.dump(acc, f, indent=4)
    return acc

def model_training(directory):
    json_contents = []
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    print('filtered_files are:', json_files)
    # for file in filtered_files:
    for json_file in json_files:
        try:
            with open(os.path.join(directory, json_file), 'r') as file:
                data = json.load(file)
                json_contents.append(data)
        except Exception as E:
            continue

    acc = prepare_sparse_matrix(json_contents)
    acc_dict = prepare_acc_dict(json_contents)
    tfidf = TfidfVectorizer()
    query_matrix = tfidf.fit_transform(acc)
    print('query_matrix created')
    io.mmwrite('sparse_matrix.mtx', query_matrix)
    with open('tfidf_recomender.pkl','wb') as f:
        pickle.dump(tfidf,f)
    print('Sparse matrix created')

    with open('acc_dict.json','w') as f:
        json.dump(acc_dict, f, indent=4)
    print('created acc_dict json file')

    return 'training completed'