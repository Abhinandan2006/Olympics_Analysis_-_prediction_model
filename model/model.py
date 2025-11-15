import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, confusion_matrix
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from modules import preprocessor

df = pd.read_csv('../data/athlete_events.csv')
region_df = pd.read_csv('../data/noc_regions.csv')
df = df.merge(region_df, on='NOC', how='left')

df.drop_duplicates(inplace=True)
df.drop(columns=['ID', 'Name', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Event', 'notes'], inplace=True)
df = df.dropna(subset=['region'])

df['Medal'].fillna("No Medal", inplace=True)
le_medal = LabelEncoder()
df['Medal'] = le_medal.fit_transform(df['Medal'])

df = df.dropna(subset=['Age', 'Height', 'Weight'])

Q1 = df['Age'].quantile(0.25)
Q3 = df['Age'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['Age'] >= Q1 - 1.5 * IQR) & (df['Age'] <= Q3 + 1.5 * IQR)]

z_score_height = np.abs(stats.zscore(df['Height']))
df = df[z_score_height <= 3]

Q1 = df['Weight'].quantile(0.25)
Q3 = df['Weight'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['Weight'] >= Q1 - 1.5 * IQR) & (df['Weight'] <= Q3 + 1.5 * IQR)]

df = df.reset_index(drop=True)

X_train, X_test, y_train, y_test = train_test_split(
    df.drop(columns=['Medal']),
    df['Medal'],
    test_size=0.2,
    random_state=42,
    stratify=df['Medal']
)

X_train = X_train.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
X_test = X_test.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

preprocessor = preprocessor.get_preprocessor()

X_train_prep = preprocessor.fit_transform(X_train, y_train)
X_test_prep = preprocessor.transform(X_test)

smote = SMOTE(
    sampling_strategy="not majority",
    random_state=42
)
X_train_res, y_train_res = smote.fit_resample(X_train_prep, y_train)

weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train_res),
    y=y_train_res
)

model = LGBMClassifier(
    n_estimators=500,
    learning_rate=0.03,
    num_leaves=64,
    random_state=42,
    class_weight={0: weights[0], 1: weights[1], 2: weights[2], 3: weights[3]},
    n_jobs=-1
)

model.fit(X_train_res, y_train_res)

y_pred = model.predict(X_test_prep)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

final_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', model)
])

joblib.dump(final_pipeline, '../model/pipeline.pkl')
joblib.dump(le_medal, '../model/label_encoder.pkl')

print("\nTraining complete. Pipeline saved.")
