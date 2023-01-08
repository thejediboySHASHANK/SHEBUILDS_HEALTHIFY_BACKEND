import requests
import configparser
from flask import Flask,request, url_for, redirect, render_template, jsonify
import pickle
import numpy as np

app = Flask(__name__)

model=pickle.load(open('final_model-1.pkl','rb'))
model2=pickle.load(open('model2.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template("forest.html")

@app.route("/prediction", methods=["GET"])
def prediction () : 
    prediction = model.predict(request.json)

    return prediction


@app.route ("/predictSteps", methods=["POST", "GET"])
def predictsteps () :
    features2 = [int(x) for x in request.form.values()]
    final2 = [np.array(features2)]
    print (features2)
    print (final2)
    prediction2 = model2.predict(final2)

    output_steps = '{}'.format(prediction2[0][0], 2)

    return render_template('steps.html',pred_steps='Steps required is  : {}'.format(output_steps), bhai="kuch karna hain iska ab?")
    




@app.route('/predict',methods=['POST','GET'])
def predict():
    # features = [1 if x == 'M' else 0 if x == 'F' else int(x) if x.isdigit() else  x for x in request.form.values()]

    features = []
    for x in request.form.values() :
        if x == 'M' : 
            value = 1
        elif x == 'F' : 
            value = 0       
        else : 
            try : 
                value = int(x)
            except ValueError : 
                try : 
                    value = float(x)
                except ValueError : 
                    value = x

        features.append(value)
    

    final=[np.array(features)]
    print(features)
    print(final)
    prediction=model.predict(final)
    print (prediction)

    # return jsonify({'prediction' : prediction})
    
    output1='{0:.{1}f}'.format(prediction[0][0], 2)
    output2='{0:.{1}f}'.format(prediction[0][1], 2)
    output3='{0:.{1}f}'.format(prediction[0][2], 2)
    # output4='{0:.{1}f}'.format(prediction[0][3], 2)

    return render_template('index.html',
    pred1='BMI is : {}'.format(output1), 
    pred2='BMR is {}' .format(output2), 
    pred3='Required Daily Calories are {}' .format(output3), 
    pred_mild = float(output3) * 0.88,
    pred_loss = float(output3) * 0.77,
    pred_extreme = float(output3) * 0.53,
    bhai="kuch karna hain iska ab?")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
