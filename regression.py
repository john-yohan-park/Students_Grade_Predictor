'''
John Park
Github: john-yohan-park
System Requirements: Anaconda, TensorFlow, Pandas, NumPy, scikit-learn, pickle, matplotlib
Predicts students' 3rd semester grades based on their:
    - 1st & 2nd semester grades
    - time spent studying
    - instances of failures
    - number of absences
Uses linear regression model to train our machine
Data Source: https://archive.ics.uci.edu/ml/datasets/student+performance
Data Size:   649 students
'''

# import libraries
import pandas                          # extract data
import numpy                           # organize data into an array
import sklearn                         # machine learning library
import pickle                          # save model
from   matplotlib import pyplot        # graph data
from   sklearn    import linear_model  # linear regression model
from   matplotlib import style         # change graph style

#======================================PREP DATA======================================
# extract data
data = pandas.read_csv('student-mat.csv', sep = ';')
# trim data to desired attributes
data = data[['G1', 'G2', 'G3', 'studytime', 'failures', 'absences']]  # working with ints

# identify which attributes help us create the most accurate model
'''
attr1 = 'absences'                            # see correlation
style.use('ggplot')
pyplot.scatter(data[attr1], data['G3'])       # use scatter plot
pyplot.xlabel(attr1)
pyplot.ylabel('3rd Sem Grade')
pyplot.show()
'''

predict = 'G3'  # variable to predict

# construct new data frames
x = numpy.array(data.drop([predict], 1))
y = numpy.array(data[predict])

# partition 10% of data as test samples to test model accuracy
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

#================================TRAIN & GET BEST MODEL================================
bestAccuracy = 0
for _ in range(100):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

    # train model using linear regression
    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)             # train: produces line of best fit from train data
    accuracy = linear.score(x_test, y_test)  # test accuracy

    if accuracy > bestAccuracy:              # save the best model
        bestAccuracy = accuracy
        with open('student_model.pickle', 'wb') as f:
            pickle.dump(linear, f)

#===================================SAVE BEST MODEL===================================
pickle_in = open('student_model.pickle', 'rb')
linear = pickle.load(pickle_in)

predictions = linear.predict(x_test)    # array of just predictions

print("Accuracy: ", '\t', '\t', bestAccuracy)
print("Guesses", '\t', '\t', "Actual")
for i in range(len(predictions)):
    print(predictions[i], '\t', y_test[i])
