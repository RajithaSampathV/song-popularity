# 🎵 Song Popularity Prediction System

A machine learning–based system that predicts the **popularity score (0–100)** of a song by analyzing its **audio characteristics and metadata**.  
The project demonstrates a complete **end-to-end workflow**, from data preprocessing and model training to deployment through an interactive web interface.

---

## 🚀 Project Overview

With the rapid growth of music streaming platforms, predicting which songs will become popular has become increasingly complex. This project addresses that challenge by building a structured system that:

- Extracts meaningful **audio features** from song files  
- Trains and evaluates **machine learning regression models**  
- Integrates the trained model with a **modern web frontend**  
- Provides real-time popularity predictions to users  

The system is intended for **singers, music producers, composers, and content creators** to gain early insights into a song’s potential performance.

---

## 🎧 System Walkthrough

This project includes a detailed end-to-end walkthrough explaining how the system works behind the scenes.

### Covered Pipeline:
- Dataset preparation and cleaning  
- Audio preprocessing  
- Feature extraction using **MFCCs, chroma, and spectral features**  
- Model training, selection, and evaluation  
- Integration of the trained ML model with the frontend  

The walkthrough demonstrates how **audio analytics and machine learning** are combined into a practical, real-world prediction system.

---

## 🧠 Key Features

- 🎧 Upload `.mp3` song files  
- 🔍 Automated audio feature extraction using **Librosa**  
- 📊 Data preprocessing and normalization  
- 🤖 Multiple regression models trained and evaluated  
- 🏆 Best-performing model selected based on RMSE, MAE, and R²  
- 🌐 Interactive web interface for real-time predictions  

---

## 🛠️ Technologies & Tools Used

### **Machine Learning & Data Processing**
- Python  
- NumPy & Pandas  
- Librosa (audio feature extraction)  
- Scikit-learn / TensorFlow  
- Joblib  

### **Analysis & Visualization**
- Matplotlib  
- Seaborn  

### **Frontend & Backend**
- Next.js (frontend interface)  
- API routes / backend integration for serving predictions  

### **Other Tools**
- Google Colab (model training & experimentation)  
- Git & GitHub (version control)

---

## 🔬 Methodology Summary

1. **Dataset Preparation**
   - Spotify Tracks dataset containing audio and metadata features  

2. **Data Preprocessing**
   - Handling missing values and duplicates  
   - Encoding categorical features  
   - Scaling numerical attributes  

3. **Feature Engineering**
   - Extraction of MFCCs, chroma features, and spectral features  
   - Correlation and ANOVA-based feature selection  

4. **Model Training & Evaluation**
   - Linear Regression  
   - Ridge Regression  
   - Random Forest Regressor  
   - Gradient Boosting Regressor  
   - Neural Network models  
   - Evaluation using RMSE, MAE, and R²  

5. **Model Selection**
   - Best-performing model selected and saved for deployment  

6. **Deployment**
   - Model integrated with a web interface  
   - Real-time predictions served via backend APIs  

---

## 🌐 Live Demo & Resources

- 🔗 **Live Demo:** https://lnkd.in/ekYMiVqf  
- 📦 **GitHub Repository:** https://lnkd.in/eSKibJQC  
- 📊 **Dataset:** https://lnkd.in/ebiqXe8S  
- 📓 **Google Colab (Preprocessing & Training):** https://lnkd.in/e-HcFWYb  

---

## 👥 Team Members

- Rajitha Sampath Viduranga  
- Dinura Sanmith  
- Monil Ariyarathna  
- Chithira Jayarathna  

---

## 📌 Conclusion

This project demonstrates how machine learning and audio signal processing can be combined to build a practical system for estimating song popularity. The modular design allows for future enhancements such as social media signals, lyric sentiment analysis, and advanced deep learning models.
