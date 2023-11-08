import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
import numpy as np
import cv2



tf.disable_v2_behavior()

detector = dlib.get_frontal_face_detector() # 앞 얼굴을 찾아주는 디텍터
shape = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')
# img = dlib.load_rgb_image('./image/09.jpg')
#
# plt.figure(figsize=(16,10))
# plt.imshow(img)
# plt.show()
#
# img_result = img.copy()
# dets = detector(img, 1)     # 이미지를 업샘플링하는 횟수, 업샘플링을 사용하면 더 정확한 얼굴 감지가 가능하지만 계산 비용이 늘어날 수 있음
#
# if (len(dets) == 0):
#     print('Not find faces')
#
# else:
#     fig, ax = plt.subplots(1, figsize=(10, 16))
#     for det in dets:
#         x, y, w, h = det.left(), det.top(), det.width(), det.height()
#         rect = patches.Rectangle((x, y), w, h, linewidth=2,
#                         edgecolor='b', facecolor='None')
#         ax.add_patch(rect)
#
# ax.imshow(img_result)
# plt.show()
#
# fig, ax = plt.subplots(1, figsize=(16, 10))
# obj = dlib.full_object_detections()
#
# for detection in dets:
#     s = shape(img, detection)
#     obj.append(s)
#
#     for point in s.parts():
#         circle = patches.Circle((point.x, point.y),
#                     radius=3, edgecolor='b', facecolor='b')
#         ax.add_patch(circle)
#     ax.imshow(img_result)
# plt.show()

def align_faces(img):
    dets = detector(img)
    objs = dlib.full_object_detections()
    for detection in dets:
        s = shape(img, detection)
        objs.append(s)
    # 얼굴을 정렬하는 코드
    faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)  # padding을 0으로 지정하면 얼굴이 잘림, 그래서 여유를 준다.
    return faces

# test_img = dlib.load_rgb_image('./image/02.jpg')
# test_faces = align_faces(test_img)
# fig, axes = plt.subplots(1, len(test_faces)+1, figsize=(10, 8))
# axes[0].imshow(test_img)
# for i, face  in enumerate(test_faces):
#     axes[i+1].imshow(face)
# plt.show()

########################## 모델 불러오는 부분
sess = tf.Session()
init_op = tf.group(tf.global_variables_initializer(),
                   tf.local_variables_initializer())
sess.run(init_op)

saver = tf.train.import_meta_graph('./models/model.meta')
saver.restore(sess, tf.train.latest_checkpoint('./models'))
graph = tf.get_default_graph()
X = graph.get_tensor_by_name('X:0')
Y = graph.get_tensor_by_name('Y:0')
Xs = graph.get_tensor_by_name('generator/xs:0')
############################

def preprocess(img):
    return img / 127.5 -1
def deprocess(img):
    return (img + 1) / 2

img1 = dlib.load_rgb_image('./image/10.jpg')
img1_faces = align_faces(img1)

img2 = dlib.load_rgb_image('./image/makeup/XMY-136.png')
img2_faces = align_faces(img2)

# fig, axes = plt.subplots(1, 2, figsize=(8, 5))
# axes[0].imshow(img1_faces[0])
# axes[1].imshow(img2_faces[0])
# plt.show()

src_img = img1_faces[0]
ref_img = img2_faces[0]

X_img = preprocess(src_img)
X_img = np.expand_dims(X_img, axis=0)

Y_img = preprocess(ref_img)
Y_img = np.expand_dims(Y_img, axis=0)

output = sess.run(Xs, feed_dict={X:X_img, Y:Y_img})
output_img = deprocess(output[0])

fig, axes = plt.subplots(1, 3, figsize=(8, 5))
axes[0].imshow(img1_faces[0])
axes[1].imshow(img2_faces[0])
axes[2].imshow(output_img)
plt.show()