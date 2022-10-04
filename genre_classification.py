import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn import svm


def preprocess_data():
    country = pd.read_csv('genre_datasets/country.csv')
    country['tag'] = [0 for i in range(1000)]
    country_train = country.iloc[:900]
    country_test = country.iloc[900:]

    pop = pd.read_csv('genre_datasets/pop.csv')
    pop['tag'] = [1 for i in range(1000)]
    pop_train = pop.iloc[:900]
    pop_test = pop.iloc[900:]

    rap = pd.read_csv('genre_datasets/rap.csv')
    rap['tag'] = [2 for i in range(1000)]
    rap_train = rap.iloc[:900]
    rap_test = rap.iloc[900:]

    rock = pd.read_csv('genre_datasets/rock.csv')
    rock['tag'] = [3 for i in range(1000)]
    rock_train = rock.iloc[:900]
    rock_test = rock.iloc[900:]

    data_train = pd.concat(
        [country_train, pop_train, rap_train, rock_train]
    )
    data_train = data_train.drop(
        columns=['key', 'loudness', 'mode', 'tempo', 'id', 'duration_ms', 'time_signature', 'type', 'uri',
                 'analysis_url',
                 'track_href']
    )

    data_test = pd.concat(
        [country_test, pop_test, rap_test, rock_test]
    )
    data_test = data_test.drop(
        columns=['key', 'loudness', 'mode', 'tempo', 'id', 'duration_ms', 'time_signature', 'type', 'uri',
                 'analysis_url',
                 'track_href']
    )

    return data_train, data_test


def mlp_classifier(data_train, data_test):
    X_train = data_train.drop('tag', axis=1).values
    y_train = data_train['tag'].values

    X_test = data_test.drop('tag', axis=1).values
    y_test = data_test['tag'].values

    clf = MLPClassifier(solver='lbfgs', alpha=.0001, hidden_layer_sizes=(10, 5), activation='logistic', max_iter=1000)
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    return score


def svm_classifier(data_train, data_test):
    X_train = data_train.drop('tag', axis=1).values
    y_train = data_train['tag'].values

    X_test = data_test.drop('tag', axis=1).values
    y_test = data_test['tag'].values

    clf = svm.SVC(C=.55, kernel="rbf")
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    return score


data_train, data_test = preprocess_data()
print(f"MLP score: {mlp_classifier(data_train, data_test)}")
print(f"SVM score: {svm_classifier(data_train, data_test)}")
