import numpy as np
import matplotlib.pyplot as plt
from sklearn import (datasets,tree, svm) # Mission #2 and #3) You need to import some modules if necessary
from matplotlib.lines import Line2D # For the custom legend
from sklearn import metrics #For balanced accuracy

def load_wdbc_data(filename):
    class WDBCData:
        data = []
        target = []
        target_names = ['malignant', 'benign']
        feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']
    wdbc = WDBCData()
    
    # fetch 'wdbc.data' file 
    f=open(filename,'r')
    lines=f.readlines()
    for line in lines:
        values=[]
        for value in line.split(','):
            if value=='M':
                value=0
                values.append(value)
            elif value=='B':
                value=1
                values.append(value)
            else:
                values.append(float(value))
        wdbc.data.append(values)
    f.close()
    
    # delete ID,target class from data and define target
    for i in range(len(wdbc.data)):
        del wdbc.data[i][0]
        wdbc.target.append(wdbc.data[i][0])
        del wdbc.data[i][0]
   
    wdbc.data = np.array(wdbc.data)
    
    return wdbc

if __name__ == '__main__':
    # Load a dataset
    wdbc = datasets.load_breast_cancer()
    #wdbc = load_wdbc_data('data/wdbc.data') # Mission #1) Implement 'load_wdbc_data()'

    # Train a model
    model = svm.SVC()                       # Mission #2) Try at least two different classifiers
    model.fit(wdbc.data, wdbc.target)
    
    # Train anoter model
    model2 =tree.DecisionTreeClassifier(max_depth=2)
    model2.fit(wdbc.data,wdbc.target)
    
    # Test the model
    predict1 = model.predict(wdbc.data)
    n_correct1 = sum(predict1 == wdbc.target)
    accuracy1 = n_correct1 / len(wdbc.data)  
    # Mission #3) Calculate balanced accuracy
    balanced_accuracy1=metrics.balanced_accuracy_score(wdbc.target, predict1)
    
    # Test the model2
    predict2 = model2.predict(wdbc.data)
    n_correct2 = sum(predict2 == wdbc.target)
    accuracy2 = n_correct2 / len(wdbc.data)  
    # Mission #3) Calculate balanced accuracy
    balanced_accuracy2=metrics.balanced_accuracy_score(wdbc.target, predict2)
    
    # Visualize testing results
    cmap = np.array([(1, 0, 0), (0, 1, 0)])
    clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]
    for (x, y) in [(0, 1)]: # Not mandatory, but try [(i, i+1) for i in range(0, 30, 2)]
        plt.figure(1)       
        plt.title(f'svm.SVC ({n_correct1}/{len(wdbc.data)}={accuracy1:.3f})\n balanced accuracy={balanced_accuracy1:.3f}')
        plt.scatter(wdbc.data[:,x], wdbc.data[:,y], c=cmap[wdbc.target], edgecolors=cmap[predict1])
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
        
    
    # Visualize testing results2
    cmap = np.array([(1, 0, 0), (0, 1, 0)])
    clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]
    for (x, y) in [(0, 1)]: # Not mandatory, but try [(i, i+1) for i in range(0, 30, 2)]
        plt.figure(2)
        plt.title(f'tree.DecisionTree(2) ({n_correct2}/{len(wdbc.data)}={accuracy2:.3f})\n balanced accuracy={balanced_accuracy2:.3f}')
        plt.scatter(wdbc.data[:,x], wdbc.data[:,y], c=cmap[wdbc.target], edgecolors=cmap[predict2])
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
        plt.show()   


