Health Prediction System

Overview

The Health Prediction System is a web application that helps users assess their risk for various health conditions, including heart disease, diabetes, and stroke (brain disease). Using Machine Learning models, the system takes user input, processes it, and provides a health risk assessment along with personalized recommendations.

Features

User Authentication: Register and log in to access health predictions.

Health Predictions:

Heart Disease Risk Prediction

Diabetes Risk Prediction

Stroke (Brain Disease) Risk Prediction

Personalized Health Advice: Users receive tailored health improvement suggestions based on their results.

Secure & Private: User data is protected and used only for predictions.

Tech Stack

Frontend: HTML, CSS, JavaScript, GSAP, TiltJs, LocomotiveJs.

Backend: Flask (Python)

Machine Learning Models: scikit-learn, pandas, NumPy

Database: SQLite (or any preferred database for user management)

Installation

Prerequisites

Ensure you have Python 3.7+ installed.

Clone the Repository

git clone https://github.com/your-username/health-prediction-system.git
cd health-prediction-system

Install Dependencies

pip install -r requirements.txt

Run the Application

python app.py

Open your browser and go to http://127.0.0.1:5000/ to use the application.

Usage Guide

Sign up / Log in to access the system.

Select a prediction model (Heart, Diabetes, or Brain Disease).

Enter your health details.

Click "Predict" to get your health risk assessment.

View recommendations to improve your health.

Machine Learning Models

The system uses trained ML models for health risk prediction:

Heart Disease: Logistic Regression / XGBoost

Diabetes: Decision Tree / Random Forest

Brain Disease (Stroke Prediction): Support Vector Machine (SVM)

Models are saved using pickle and loaded for predictions.

Future Enhancements

Integration with Electronic Health Records (EHR)

Advanced AI Chatbot for medical consultation

More ML models with improved accuracy

Mobile app version

Document Scanning  – Allowing Users to scan medical reports and get AI-driven insights

Contributing

Feel free to fork this repository and make improvements. Pull requests are welcome!

License

This project is licensed under the MIT License.

Contact

For any issues or suggestions, reach out to:

Deepak Mallareddy: (mail-to: mallareddydeepak03@gmail.com)

Enjoy using our Health Prediction System! 🚀

