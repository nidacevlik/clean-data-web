from fastapi import FastAPI, UploadFile, Form, File
import pandas as pd
import numpy as np
import io
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

app = FastAPI()

def clean_missing_values(df, method="mean"):
    """Eksik değerleri belirlenen yönteme göre temizler"""
    if method == "mean":
        return df.fillna(df.mean())
    elif method == "median":
        return df.fillna(df.median())
    elif method == "knn":
        imputer = KNNImputer(n_neighbors=3)
        return pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    return df

def detect_outliers(df, method="zscore"):
    """Aykırı değerleri belirler ve seçilen yönteme göre temizler"""
    if method == "zscore":
        z_scores = np.abs((df - df.mean()) / df.std())
        df[z_scores > 3] = np.nan  # 3 Standart sapma dışındaki değerleri NaN yap
    elif method == "iqr":
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        df[((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))] = np.nan
    return df

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    missing_value_method: str = Form("mean"),
    outlier_method: str = Form("zscore")
):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Sadece sayısal sütunları işleyelim
    df_numeric = df.select_dtypes(include=["number"])

    # Eksik değerleri temizle
    df_numeric = clean_missing_values(df_numeric, missing_value_method)

    # Aykırı değerleri belirle ve temizle
    df_numeric = detect_outliers(df_numeric, outlier_method)

    return {"cleaned_data": df_numeric.to_dict(orient="records")}
