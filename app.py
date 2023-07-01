from flask import Flask,request,jsonify
import pickle

 
model=pickle.load(open("Crop.pkl","rb"))

app=Flask(__name__)
@app.route('/')
def home():
    return "hello madhav"

@app.route('/predict',methods=["POST"])
def predict ():
    n = request.form.get('n')
    p = request.form.get("p")
    k = request.form.get("k")
    t = request.form.get("t")
    h = request.form.get("h")
    ph = request.form.get("ph")
    r = request.form.get("r")

    
    result=model.predict([[n,p,k,t,h,ph,r]])[0]
    
    
    return jsonify(str(result))


if __name__ == "__main__":
    app.run(debug=True)