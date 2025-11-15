import joblib
import pandas as pd
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

pipeline = joblib.load("model/pipeline.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

EXPECTED_COLUMNS = ['Age', 'Sex', 'Height', 'Weight', 'Sport', 'region']

def predict_medal(input_dict):
    df = pd.DataFrame([input_dict])[EXPECTED_COLUMNS]
    pred = pipeline.predict(df)
    return label_encoder.inverse_transform(pred)[0]

ans = predict_medal({
    "Age": 40,
    "Sex": "F",
    "Height": 150,
    "Weight": 45,
    "Sport": "Shooting",
    "region": "India"
})

print(ans)
