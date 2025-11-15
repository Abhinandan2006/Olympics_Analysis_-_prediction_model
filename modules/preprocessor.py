import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer
from category_encoders import TargetEncoder
def preprocess_summer(df, region_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df

def preprocess_winter(df, region_df):
    df = df[df['Season'] == 'Winter']
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df

def preprocess_overall(df, region_df):
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df

def get_preprocessor():
    preprocessor = ColumnTransformer(transformers=[

        # Numerical imputers
        ('age_imputer', SimpleImputer(strategy='median'), ['Age']),
        ('hw_imputer', IterativeImputer(random_state=42), ['Height', 'Weight']),

        # Categorical encoders
        ('sex_encoder', OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), ['Sex']),
        ('sport_encoder', OneHotEncoder(handle_unknown='ignore'), ['Sport']),
        ('region_encoder', TargetEncoder(handle_unknown="value", handle_missing="value"), ['region'])
    ])

    return preprocessor
