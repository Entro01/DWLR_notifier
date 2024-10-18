import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed
from tensorflow.keras.callbacks import EarlyStopping

# Load and preprocess data
df = pd.read_csv('DWLR_Dataset_2023.csv')
water_level = df['Water_Level_m'].values.reshape(-1, 1)

# Normalize the data
scaler = MinMaxScaler()
water_level_scaled = scaler.fit_transform(water_level)

# Create sequences
def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length + 1):
        sequences.append(data[i:i+seq_length])
    return np.array(sequences)

seq_length = 10
X = create_sequences(water_level_scaled, seq_length)

# Define and train the model
model = Sequential([
    LSTM(64, activation='relu', input_shape=(seq_length, 1), return_sequences=True),
    LSTM(32, activation='relu', return_sequences=False),
    RepeatVector(seq_length),
    LSTM(32, activation='relu', return_sequences=True),
    LSTM(64, activation='relu', return_sequences=True),
    TimeDistributed(Dense(1))
])

model.compile(optimizer='adam', loss='mse')

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history = model.fit(
    X, X,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    shuffle=False
)

# Save the model
model.save('lstm_autoencoder.h5')

# Function to detect anomalies
def detect_anomalies(model, data, threshold):
    reconstructed = model.predict(data)
    mse = np.mean(np.power(data - reconstructed, 2), axis=1)
    return mse > threshold

# Example usage
anomalies = detect_anomalies(model, X, threshold=0.1)