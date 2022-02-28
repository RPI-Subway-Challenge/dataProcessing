from knn import KNN

coords = [(-80,40), (-79,41), (-71, 44), (-72,45)]
cv = KNN()

print(cv.random_centers(n_neighbors=2))
