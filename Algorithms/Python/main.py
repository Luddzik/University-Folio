import knn
import gaussian

#code is working for full fold, for testing, and report, it was set for sample size of 5 for each fold because it took too much time to test.
print knn.fullConfusion(1)
print knn.fullConfusion(3)
print knn.fullConfusion(5)

#gaussian code doesn't work completely
#print totalGaussianClassificationDiscriminant('fold1_features')
