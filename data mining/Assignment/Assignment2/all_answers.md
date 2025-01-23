# Assignment2

## DT

### Question1

In the SDSS.pdf file

### Question2

Number of leaves in the tree: 28

Generalization Error: 127

### Question3

The best value for the max_depth is 2. The max_depth mainly affects the complexity of the model, that is, the number of final leaf nodes. With equal training error, the fewer the final leaf nodes, the smaller the generalization error.（In the SDSS_best.pdf）

### Question4

Use the decision tree in point 3 because, with equal training error, the model in point 3 is simpler and more efficient for classification.

### Question5

The redshift is most relevant when classifying sky objects. In physics, redshift happens when light or other electromagnetic radiation from an object is increased in wavelength, or shifted to the red end of the spectrum.

### Question6

I think pruning can be considered because when classifying STAR, we can stop at the previous step without needing to make another decision to split the STAR into two subsets.

### Question7

Generalization Error before Pruning: 115.0

Generalization Error after Pruning: 114.5
(In the SDSS_best_pruned.pdf)

## NB

### Question1

Multinomial Naive Bayes Average Accuracy: 0.7913 (+/- 0.0426)
Gaussian Naive Bayes Average Accuracy: 0.7363 (+/- 0.0308)

### Qusetion2

Random Classifier Average Accuracy: 0.1113 (+/- 0.0360)

Multinomial Naive Bayes is much better than the Random Classifier.

### Question3

Multinomial Naive Bayes Average Accuracy without removing "stopword": 0.7450 (+/- 0.0384)

We can see that the accuarcy worsens. Here are a few reasons why not removing stopwords might lead to a decrease in the accuracy of a Multinomial Naive Bayes (MNB) model:

- Increased Noise: Stopwords typically do not help with the classification task. Keeping them adds noise to the model, which can affect its performance.

- Expanded Feature Space: The presence of stopwords increases the dimensionality of the feature space, making the model handle more irrelevant features, which can lead to overfitting.

- Imbalanced Word Frequency Distribution: Stopwords appear frequently and can dilute the impact of useful features (i.e., words that help with classification), reducing the model's sensitivity to these useful features.

### Question4

Reasons why Task 1 is easier to classify:

- The differences between categories are significant, and the vocabulary is highly distinctive. The “use of guns”, “hockey”, “Mac hardware” belong to completely different domains, with noticeable differences in content and vocabulary, making it easier for the classifier to distinguish between them.

Reasons why Task 2 is harder to classify:

- The similarities between categories are high, and there is a lot of vocabulary overlap. The  “Mac hardware”, “IBM hardware”, “electronics” all belong to the technical and electronic fields, with similar content and vocabulary, making it difficult for the classifier to differentiate between them.

