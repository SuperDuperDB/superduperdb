import numpy
from sklearn.svm import SVC


def test_pipeline(random_arrays, int64):
    X = numpy.random.randn(100, 32)
    y = (numpy.random.rand(100) > 0.5).astype(int)
    est = SVC()
    est.fit(X, y)
    random_arrays.create_model('test_sklearn', est)
    pl = random_arrays.models['test_sklearn']
    print(pl)
    random_arrays.create_watcher('test_sklearn', key='x')
