
import * as tf from '@tensorflow/tfjs';


function makePrediction(companyName) {
	const model = await tf.loadLayersModel(‘./stock-predictor/modelBin/${companyName}/model.json’);
	return model.predict(X);
}
