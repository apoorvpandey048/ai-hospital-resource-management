"""Patient admission prediction using scikit-learn (moved and renamed)

Includes dataset creation, training, and a predict interface.
"""
from typing import Tuple
import numpy as np

# sklearn is optional at import time; allow the module to be imported even when
# scikit-learn is not installed. Raise clear error if user calls training/predict
# functions without sklearn.
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    _SKLEARN_AVAILABLE = True
except Exception:  # pragma: no cover - environment dependent
    LogisticRegression = None
    train_test_split = None
    accuracy_score = None
    _SKLEARN_AVAILABLE = False


def make_sample_dataset(n=200):
    # features: age, temp, sbp, pain
    rng = np.random.RandomState(0)
    age = rng.randint(20, 90, size=n)
    temp = rng.normal(37, 1.5, size=n)
    sbp = rng.normal(120, 15, size=n)
    pain = rng.randint(0, 10, size=n)
    # label: admission if temp>38 or pain>7 or age>75
    y = ((temp > 38) | (pain > 7) | (age > 75)).astype(int)
    X = np.vstack([age, temp, sbp, pain]).T
    return X, y


class AdmissionPredictor:
    def __init__(self):
        if not _SKLEARN_AVAILABLE:
            self.model = None
        else:
            self.model = LogisticRegression(max_iter=200)

    def train(self, X, y):
        if not _SKLEARN_AVAILABLE:
            raise RuntimeError("scikit-learn is required to train the admission predictor. Install scikit-learn and try again.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        return acc

    def predict(self, x):
        if not _SKLEARN_AVAILABLE:
            raise RuntimeError("scikit-learn is required to run predictions. Install scikit-learn and try again.")
        return int(self.model.predict([x])[0])


if __name__ == '__main__':
    X, y = make_sample_dataset()
    ap = AdmissionPredictor()
    acc = ap.train(X, y)
    print('trained, test acc=', acc)
    print('sample pred:', ap.predict([30, 39.0, 115, 9]))
