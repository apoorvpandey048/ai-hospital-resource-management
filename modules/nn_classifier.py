"""Simple neural network classifier using sklearn's MLPClassifier (moved)

Demo for disease classification from simple features.
"""
import numpy as np

# sklearn optional import to keep module importable in lightweight environments
try:
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    _SKLEARN_AVAILABLE = True
except Exception:  # pragma: no cover - environment dependent
    MLPClassifier = None
    train_test_split = None
    accuracy_score = None
    _SKLEARN_AVAILABLE = False


def make_sample_data(n=200):
    rng = np.random.RandomState(1)
    # features: fever (0/1), cough (0/1), wbc
    fever = rng.binomial(1, 0.2, size=n)
    cough = rng.binomial(1, 0.3, size=n)
    wbc = rng.normal(7, 2, size=n)
    X = np.vstack([fever, cough, wbc]).T
    # label: disease A if fever and high wbc
    y = ((fever == 1) & (wbc > 9)).astype(int)
    return X, y


class NNClassifier:
    def __init__(self):
        if not _SKLEARN_AVAILABLE:
            self.model = None
        else:
            self.model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=500, random_state=2)

    def train(self, X, y):
        if not _SKLEARN_AVAILABLE:
            raise RuntimeError("scikit-learn is required to train the NNClassifier. Install scikit-learn and try again.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        return accuracy_score(y_test, preds)

    def predict(self, x):
        if not _SKLEARN_AVAILABLE:
            raise RuntimeError("scikit-learn is required to run predictions. Install scikit-learn and try again.")
        return int(self.model.predict([x])[0])


if __name__ == '__main__':
    X, y = make_sample_data()
    m = NNClassifier()
    acc = m.train(X, y)
    print('nn acc=', acc)
    print('sample pred:', m.predict([1, 1, 11.0]))
