import * as tf from '@tensorflow/tfjs-node'

const model = tf.loadModel('./model.json');
console.log(model);
