from File import File
from Experiment import Experiment
from Link_Generator import Link_Generator
from MetaData import MetaData
from File_Requester import File_Requester
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import cross_val_score,cross_validate
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.datasets import samples_generator
from sklearn.feature_selection import SelectKBest, VarianceThreshold
from sklearn.feature_selection import f_regression
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


if __name__ == "__main__":
    x = Link_Generator("json")
    kw = ["cancer"]
    x.insert_keywords(kw)
    dic = {"samplecount" : "[200 TO 500]"}
    #dic = {}
    x.insert_criteria(dic)
    x.url_generator("experiments")
    request = File_Requester(x.get_url())
    print(request.get_url())
    request.do_request()
    request.get_request()
    request.do_content()
    print(request.get_content())
    decoder = MetaData(request.get_content(), request.get_url())
    decoder.decode_json()
    print(decoder.get_decoded())
    exp = Experiment(decoder.get_decoded()["experiments"]["experiment"][13])
    print(exp.__dict__)
    print(exp.accession)
    #exp.do_files_url()
    #print(exp.get_files_url())
    #exp.json_files_requester()
    #print(exp.get_json_files_request())
    #exp.json_files_decoder()
    #print(exp.get_decoded_json_files())
    #exp.create_files()
    print(exp.files)
    #exp.download_all_files("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    exp.do_idf_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    print(exp.get_idf_file())
    exp.do_sdrf_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    print(exp.get_sdrf_file())
    exp.do_processed_file("C:/Users/utilizador/Google Drive/drive/Bioinformática/1_ano/2_Semestre/Projeto/Scripts/Downloads")
    #print(exp.get_processed_file())
    print(exp.get_concat_processed())
    print(exp.find_samples())
    #exp.get_concat_processed().to_csv("Expression_Matrix")
    #Model
    x = exp.get_concat_processed().dropna()
    y = exp.get_metada_sdrf(x.columns)["FactorValue [organism part]"]
    X = x.T

    le = LabelEncoder()
    y_num = le.fit_transform(y)
    idxs = np.isin(y_num, [0, 1])

    X = X.loc[idxs,:]
    y_num = y_num[idxs]

    scaler = StandardScaler()
    X_norm = scaler.fit_transform(X)
    score_dict = {}
    precision_dict = {}
    recall_dict = {}
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis()]

    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
             "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
             "Naive Bayes", "QDA"]
    dic = {}
    for name,clf in zip(names,classifiers):
        precision_dict = {}
        recall_dict = {}
        for i in range(20, 1500, 60):
            print(i)
            anova_filter = SelectKBest(f_regression, k=i)
            anova_filter.fit(X_norm, y_num)
            feature_indexes = anova_filter.get_support()

            X_filt = X_norm[:,feature_indexes]

            #clf = svm.SVC(kernel='linear')
            scoring = ['precision_macro', 'recall_macro']
            scores = cross_validate(clf, X_filt, y_num, cv=5,scoring=scoring,return_train_score=False)
            x = scores["test_precision_macro"]
            y = scores["test_recall_macro"]
            precision_dict[i] = sum(x)/float(len(x))
            recall_dict[i] = sum(y)/float(len(y))
        dic[name] = {"recall":recall_dict,"precision":precision_dict}

    df_total = pd.concat(
        [pd.DataFrame(mets).T.append(pd.Series([mod] * len(mets["recall"]), name="Model", index=range(20, 1500, 60))).T
         for mod, mets in dic.items()])
    df_total["K"] = df_total.index.values
    df_total['F1'] = (2 * df_total['precision'] * df_total['recall'])/(df_total['precision'] + df_total['recall'])
    df_final = df_total.groupby(["Model"]).apply(lambda x: x.loc[x['F1'] == max(x['F1']), :])
    df_final.to_csv("Classifiers_Table", sep="\t")
    plt.show()
    sp = df_total.loc[df_total["Model"] == "Neural Net", ['K', 'precision', 'recall']].plot(x='K', y=['recall', 'precision'],title = "Neural Networks")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(9, 4, forward=True)
    fig.add_subplot(sp)
    fig.savefig("Neural_Net")
    plt.show()
