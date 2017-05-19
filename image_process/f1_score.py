from __future__ import print_function
import tensorflow as tf, sys, os, time
from sklearn.metrics import classification_report

# Pass 3 params : test_data_set_directory, retrained_graph, retrained_label
test_data = []
actual_label = []
predict_label = []
i = 0

print(sys.argv)
test_data_dir_paths = sys.argv[1]  # pass test_data_set_directory
retrain_graph = sys.argv[2].encode(sys.getfilesystemencoding())  # pass retrained_graph
retrain_label = sys.argv[3].encode(sys.getfilesystemencoding())  # pass retrained_label
label_set = {}

for root, dirs, files in os.walk(test_data_dir_paths):
    for index in range(len(dirs)):
        label_set[index] = dirs[index]

for index_label, label in label_set.items():
    path = os.path.join(test_data_dir_paths, label)
    files = os.listdir(path)
    for file in files:
        if file.endswith(".JPG") or file.endswith(".jpg"):
            test_data.append(os.path.join(path, file))
            actual_label.append(index_label)

label_lines = [line.rstrip() for line
               in tf.gfile.GFile(retrain_label)]

# Unpersists graph from file
with tf.gfile.FastGFile(retrain_graph, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

print("Results : \n", file=open("logs.txt", "w+"))
for image_path in test_data:
    i += 1
    print(str(i) + " : " + image_path)
    print(str(i) + " : " + image_path, file=open("logs.txt", "a"))
    # image_path = "C:\\Users\\as\Desktop\plant_test_set\\bacla\\20170204_171228.jpg"

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        print(predictions)
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
            print('%s (score = %.5f)' % (human_string, score), file=open("logs.txt", "a"))

        for index_label, label in label_set.items():
            if (label_lines[top_k[0]] == label):
                predict_label.append(index_label)
                break
    time.sleep(0.05)
print(actual_label)
print(predict_label)
target_names = list(label_set.values())
print(classification_report(actual_label, predict_label, target_names=target_names))
print(classification_report(actual_label, predict_label, target_names=target_names), file=open("result.txt", "w+"))
