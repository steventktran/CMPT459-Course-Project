import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, make_scorer, plot_confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt  
import xgboost
from sklearn.ensemble import RandomForestClassifier
from sklearn import neighbors
import pickle

data = pd.read_csv("data/cases_train_processed.csv")

encoder = LabelEncoder()
data = data.apply(encoder.fit_transform)

x = data.iloc[:, data.columns != "outcome"] #input
y = data.iloc[:, data.columns == "outcome"] #output
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, random_state = 0, shuffle = False, stratify = None)

def xgboost_model(x_train, y_train):
	model = xgboost.XGBClassifier(use_label_encoder = False, eval_metric="mlogloss") #default is max_depth = 6
	model.fit(x_train, y_train.values.ravel())
	with open("models/xgb_classifier.pkl", "wb") as file:
		pickle.dump(model, file)
	return model

def knn_model(x_train, y_train):
	model = neighbors.KNeighborsClassifier(100, weights='distance')
	model.fit(x_train, y_train.values.ravel())
	with open("models/knn_classifier.pkl", "wb") as file:
		pickle.dump(model, file)
	return model

def randomforests_model(x_train, y_train):
    model = RandomForestClassifier(n_estimators=25)
    model.fit(x_train, y_train.values.ravel())
    with open("models/rf_classifier.pkl", "wb") as file:
	    pickle.dump(model, file)
    return model

def accuracy(model, x, y):
	y_predict = model.predict(x)
	accuracy = accuracy_score(y, y_predict)
	return accuracy

def report(model, x, y):
	y_predict = model.predict(x)
	outcomes = ['recovered', 'hospitalized', 'nonhospitalized', 'deceased']
	report = classification_report(y, y_predict, target_names=outcomes, digits=4)
	return report

def confusion_matrix_plot(model, x, y, title):
	outcomes = ['recovered', 'hospitalized', 'nonhospitalized', 'deceased']
	matrix = plot_confusion_matrix(model, x, y, display_labels=outcomes, xticks_rotation=15)
	matrix.ax_.set_title(title)
	plt.tight_layout()
	plt.show()

def cross_validation(model, x, y):
	scoring = {'AUC': 'roc_auc', 'Accuracy': make_scorer(accuracy_score)}
	gs = GridSearchCV(model, param_grid={'min_samples_split': range(2, 403, 10)},
                  scoring=scoring, refit='AUC', return_train_score=True)
	gs.fit(x, y)
	return gs.cv_results_

# saved_xgboost = xgboost_model(x_train, y_train)
# saved_knn = knn_model(x_train, y_train)
# saved_rf = randomforests_model(x_train, y_train)

loaded_xgboost = pickle.load(open("models/xgb_classifier.pkl", "rb"))
loaded_knn = pickle.load(open("models/knn_classifier.pkl", "rb"))
loaded_rf = pickle.load(open("models/rf_classifier.pkl", "rb"))

# print("XGBoost Training Accuracy: ", accuracy(loaded_xgboost, x_train, y_train))
# print("XGBoost Validation Accuracy: ", accuracy(loaded_xgboost, x_test, y_test))
# print("XGBoost Training Classification Report:\n", report(loaded_xgboost, x_train, y_train))
# print("XGBoost Validation Classification Report:\n", report(loaded_xgboost, x_test, y_test))
# confusion_matrix_plot(loaded_xgboost, x_test, y_test, 'XGBoost Confusion Matrix')

# print("K-Nearest Neighbours Training Accuracy: ", accuracy(loaded_knn, x_train, y_train))
# print("K-Nearest Neighbours Validation Accuracy: ", accuracy(loaded_knn, x_test, y_test))
# print("K-Nearest Neighbours Training Classification Report:\n", report(loaded_knn, x_train, y_train))
# print("K-Nearest Neighbours Validation Classification Report:\n", report(loaded_knn, x_test, y_test))
# confusion_matrix_plot(loaded_rf, x_test, y_test, 'Random Forests Confusion Matrix')

# print("Random Forests Training Accuracy: ", accuracy(loaded_rf, x_train, y_train))
# print("Random Forests Validation Accuracy: ", accuracy(loaded_rf, x_test, y_test))
# print("Random Forests Training Classification Report:\n", report(loaded_rf, x_train, y_train))
# print("Random Forests Validation Classification Report:\n", report(loaded_rf, x_test, y_test))
# confusion_matrix_plot(loaded_knn, x_test, y_test, 'K-Nearest Neighbours Confusion Matrix')

# print(cross_validation(loaded_xgboost, x_train, y_train))
# print(cross_validation(loaded_knn, x_train, y_train))
# print(cross_validation(loaded_rf, x_train, y_train))