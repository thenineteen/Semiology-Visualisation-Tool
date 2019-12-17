import numpy as np
import matplotlib.pyplot as plt
# from sklearn.svm import LinearSVC



def plot_coefficients_all(classifier, feature_names, save=False, title='Linear-SVC for Temporal-EZ prediction: Feature Ranking'):
    coef = classifier.coef_.ravel()
    coefficients = np.argsort(coef)[0:]
#     coefficients = np.hstack(coefficients)
    
    # create plot
    plt.figure(figsize=(15, 10))
    colors = ['red' if c < 0 else 'blue' for c in coef[coefficients]]
    
    plt.bar(np.arange(len(coef)), coef[coefficients], color=colors)
    
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(0, 1 + len(coef)), feature_names[coefficients], rotation=45, ha='right', fontsize=12)
    plt.ylabel('Coefficients', fontsize=14)
    plt.grid(which='all')
    plt.title(title, fontsize=18)
    
    plt.tight_layout()
    if save:
        plt.savefig('D:\\Ali USB Backup\\1 PhD\\paper 1\\fixed fully\\TEST_Check_name.jpg', format='jpg', dpi=1000)
    
    plt.show()