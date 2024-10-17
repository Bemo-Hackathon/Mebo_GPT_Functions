# %%
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# %%
data = pd.read_csv(r'C:\Users\rlope\OneDrive\Área de Trabalho\HACKATHON\Telco_Churn.csv')

data.head()

# %%
data.isna().sum()

# %%
data.nunique()

# %%
columns_binary = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']

columns_label = ['MultipleLines', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

columns_dummy = ['InternetService', 'Contract', 'PaymentMethod']

# %%
for col in columns_binary:
    data[col] = data[col].astype(bool)

label_encoder = LabelEncoder()
for col in columns_label:
    data[col] = label_encoder.fit_transform(data[col])

data = pd.get_dummies(data, columns=columns_dummy, drop_first=True)

# %%
data.replace({True: 1, False: 0}, inplace=True)
data.replace({'Yes': 1, 'No': 0}, inplace=True)

# %%
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')

# %%
data['TotalCharges'].fillna(data['TotalCharges'].median(), inplace=True)  # Ou use median, ou qualquer valor padrão

# %%
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

X = data.drop(['customerID', 'Churn'], axis=1)
y = data['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(random_state=42, class_weight='balanced')

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print('Matriz de Confusão:')
print(confusion_matrix(y_test, y_pred))

print('\nRelatório de Classificação:')
print(classification_report(y_test, y_pred))

print('\nAcurácia:')
print(accuracy_score(y_test, y_pred))

# %%
threshold = 0.3

y_proba = model.predict_proba(X_test)[:, 1]

y_pred_adjusted = (y_proba >= threshold).astype(int)

# %%
from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(y_test, y_pred_adjusted)
print("Matriz de Confusão:\n", cm)

print("Relatório de Classificação:\n", classification_report(y_test, y_pred_adjusted))

# %%
