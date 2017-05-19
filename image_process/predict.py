from __future__ import print_function
import tensorflow as tf, sys

# Pass 3 params : test_data_set_directory, retrained_graph, retrained_label

retrain_graph = "retrained_graph.pb"  # pass retrained_graph
retrain_label = "retrained_labels.txt"  # pass retrained_label

label_lines = [line.rstrip() for line
               in tf.gfile.GFile(retrain_label)]

# Unpersists graph from file
with tf.gfile.FastGFile(retrain_graph, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

def predict(image_path):
    result_image = {}
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
            result_image[human_string] = score

    return result_image

if __name__ == "__main__":
    print(sys.argv)
    file = sys.argv[1]
    result = predict(file)
    print(result)
