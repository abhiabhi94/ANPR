import input_data
import tensorflow as tf
import cv2
import numpy as np

mnist = input_data.read_data_sets("data/MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [ None , 784 ])
y_ = tf.placeholder(tf.float32, [ None, 10 ])

W = tf.Variable(tf.zeros([784 , 10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x,W) + b)

cross_entropy = -tf.reduce_sum(y_*tf.log(y))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)


for i in range(1000):
	batch_xs,batch_ys = mnist.train.next_batch(100)
	sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

##### image preprocessing
# imgResized=[]
# m = []

img = cv2.imread("data/char_9.jpg",0)
# img1 = cv2.imread("data/char_7.jpg",0)
d = np.ndarray(shape=(1,784), buffer=(1 - img/255.0) , dtype=np.float64, order='F')
c = np.ndarray(shape=(1,10), buffer=np.array([0.,0.,0.,0.,0.,0.,1.,0.,0.,0.]) , dtype=np.float64, order='F')
for i in range(100):
	sess.run(train_step, feed_dict={x: d, y_: c})

# cv2.imshow("original",img)
# m.append([img[16:145, 15:144],img[16:145, 174:303],img[16:145, 334:463],img[16:145, 495:624]])
# m1 = img[16:145, 15:144]
# m2 = img[16:145, 174:303]
# m3 = img[16:145, 334:463]
# m4 = img[16:145, 495:624]
# cv2.imshow("Crop1",m1)
# cv2.imshow("Crop2",m2)
# cv2.imshow("Crop3",m3)
# cv2.imshow("Crop4",m4)
# print imgCrop.shape
# imgResized 
# imgResized.append([cv2.resize(m[0][0] , (28,28)),cv2.resize(m[0][1] , (28,28)),cv2.resize(m[0][2] , (28,28)),cv2.resize(m[0][3] , (28,28))])
# imgResized[1] = cv2.resize(m2 , (28,28))
# imgResized[2] = cv2.resize(m3 , (28,28))
# imgResized[3] = cv2.resize(m4 , (28,28))
# cv2.imshow("resize",imgResized)
# print imgResized.shape
# cv2.waitKey(0)

#### accuracy check


# c = np.ndarray(shape=(1,10), buffer=np.array([0.,0.,0.,0.,0.,1.,0.,0.,0.,0.]) , dtype=np.float64, order='F')
# d = np.ndarray(shape=(1,784), buffer=(1 - imgResized[0][0]/255.0) , dtype=np.float64, order='F')
# correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
# print sess.run(tf.argmax(y,1) , feed_dict = {x:d  })
# print y
for i in range(1):
	cv2.imshow("image "+str	(i),img)
	d = np.ndarray(shape=(1,784), buffer=(1 - img/255.0) , dtype=np.float64, order='F')
	print sess.run(tf.argmax(y,1) , feed_dict = {x:d  })
	cv2.waitKey(0)

# print np.ndarray(shape=(1,784), buffer=(1 - img/255.0) , dtype=np.float64, order='F')
# cv2.imshow("image "+str	(i),img)
# cv2.waitKey()
# print img.shape
# d = np.ndarray(shape=(1,784), buffer=(1 - imgResized/255.0) , dtype=np.float64, order='F')
# print d[0]
# print mnist.test.images[0]

# print b.eval(session=sess)