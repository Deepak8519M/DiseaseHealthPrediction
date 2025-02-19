from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import pickle
import pandas as pd
import bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)
 

# --------------------- Load Pickle Files ---------------------

# Heart Model
with open('models/model_heart.pkl', 'rb') as model_file:
    model_heart = pickle.load(model_file)
with open('models/scaler_heart.pkl', 'rb') as scaler_file:
    scaler_heart = pickle.load(scaler_file)
with open('models/encoder_heart.pkl', 'rb') as encoder_file:
    encoder_heart = pickle.load(encoder_file)

# Diabetes Model
with open('models/model_diabetes.pkl', 'rb') as model_file:
    model_diabetes = pickle.load(model_file)
with open('models/scaler_diabetes.pkl', 'rb') as scaler_file:
    scaler_diabetes = pickle.load(scaler_file)

# Brain Model
with open('models/model_brain1.pkl', 'rb') as model_file:
    model_brain = pickle.load(model_file)
with open('models/encoder_brain.pkl', 'rb') as encoder_file:
    encoder_brain = pickle.load(encoder_file)

# --------------------- Helper Function ---------------------
def preprocess_data(data, numeric_cols, categorical_cols=None, scaler=None, encoder=None):
    """
    Preprocess the input data:
    - Scale numeric features
    - Encode categorical features (if encoder is provided)
    """
    input_df = pd.DataFrame([data])

    # Scale numeric columns
    if scaler and numeric_cols:
        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

    # Encode categorical columns if encoder exists
    if encoder and categorical_cols:
        encoded_categorical = encoder.transform(input_df[categorical_cols])
        encoded_categorical = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(categorical_cols))
        return pd.concat([input_df[numeric_cols], encoded_categorical], axis=1)

    return input_df[numeric_cols]

# --------------------- WTForms for Login/Register ---------------------
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# --------------------- Routes for Pages ---------------------
@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password.", "danger")
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return render_template('dashboard.html', user=user)
    flash("You need to log in to access the dashboard.", "warning")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/brain')
def brain():
    return render_template('brain.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')

# --------------------- Heart Disease Prediction ---------------------
@app.route('/predict_heart', methods=['POST'])
def predict():
    try:
        # Collect data from the form
        data = {
            "Age": float(request.form["Age"]),
            "Sex": request.form["Sex"],
            "ChestPainType": request.form["ChestPainType"],
            "RestingBP": float(request.form["RestingBP"]),
            "Cholesterol": float(request.form["Cholesterol"]),
            "FastingBS": float(request.form["FastingBS"]),
            "RestingECG": request.form["RestingECG"],
            "MaxHR": float(request.form["MaxHR"]),
            "ExerciseAngina": request.form["ExerciseAngina"],
            "Oldpeak": float(request.form["Oldpeak"]),
            "ST_Slope": request.form["ST_Slope"],
        }

        # Preprocess input data
        numeric_cols = ["Age", "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak"]
        categorical_cols = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
        input_preprocessed = preprocess_data(data, numeric_cols, categorical_cols, scaler_heart, encoder_heart)

        probabilities = model_heart.predict_proba(input_preprocessed)
    
    # Get the probability of being at risk (assuming class 1 represents 'at risk')
        risk_probability = probabilities[0][1] * 100  # Convert to percentage

        output = f"{risk_probability:.2f}% chance of being at risk of a heart attack"

        # Provide tips based on the risk range
        if 0 <= risk_probability <= 30:
            advice = (
                "Tips: Maintain a balanced diet low in saturated fats and salt. "
                "Engage in regular exercise, like walking or jogging, for 30 minutes daily. "
                "Avoid smoking and excessive alcohol."
            )
        elif 31 <= risk_probability <= 60:
            advice = (
                "Tips: Monitor blood pressure and cholesterol levels regularly. "
                "Include heart-friendly foods like nuts, fish, and whole grains in your diet. "
                "Practice stress-reducing activities like yoga or meditation."
            )
        elif 61 <= risk_probability <= 100:
            advice = (
                "Tips: Schedule regular check-ups with a cardiologist. "
                "Take prescribed medications consistently and as advised. "
                "Avoid heavy physical exertion; opt for mild exercises like stretches."
            )
        else:
            advice = "Invalid risk percentage. Please check the input values."

        return render_template(
        "result.html", 
        prediction_text1=f"The person has {output}.", 
        prediction_text2=advice
    )
    except Exception as e:
        return render_template("result.html", prediction_text=f"An error occurred: {str(e)}")

# --------------------- Diabetes Prediction ---------------------
@app.route("/predict_diabetes", methods=["POST"])
def predict_diabetes():
    try:
        # Collect data from the form
        data = {
            "Pregnancies": float(request.form["Pregnancies"]),
            "Glucose": float(request.form["Glucose"]),
            "BloodPressure": float(request.form["BloodPressure"]),
            "SkinThickness": float(request.form["SkinThickness"]),
            "Insulin": float(request.form["Insulin"]),
            "BMI": float(request.form["BMI"]),
            "DiabetesPedigreeFunction": float(request.form["DiabetesPedigreeFunction"]),
            "Age": float(request.form["Age"]),
        }

        # Preprocess input data
        numeric_cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
        input_preprocessed = preprocess_data(data, numeric_cols, scaler=scaler_diabetes)

        probabilities = model_diabetes.predict_proba(input_preprocessed)
    
        risk_probability = probabilities[0][1] * 100  # Convert to percentage

        output = f"{risk_probability:.2f}% chance of being at risk of diabetes"

        if 0 <= risk_probability <= 30:
            advice = (
                "Tips: Maintain a healthy diet rich in fruits, vegetables, and whole grains. "
                "Engage in at least 30 minutes of moderate physical activity daily. "
                "Keep a healthy weight and avoid sugary drinks and processed foods."
            )
        elif 31 <= risk_probability <= 60:
            advice = (
                "Tips: Regularly monitor your blood sugar levels and consult a doctor for guidance. "
                "Include foods with a low glycemic index in your diet and avoid overeating. "
                "Practice stress management techniques, such as yoga or mindfulness."
            )
        elif 61 <= risk_probability <= 100:
            advice = (
                "Tips: Work closely with a healthcare provider to develop a personalized management plan. "
                "Take prescribed medications or insulin as directed. "
                "Avoid skipping meals and maintain a strict, diabetes-friendly diet."
            )
        else:
            advice = "Invalid risk percentage. Please check the input values."

        # Return the results with two prediction texts
        return render_template(
            "result.html",
            prediction_text1=f"The person has {output}.",
            prediction_text2=advice
        )
    except Exception as e:
        return render_template("result.html", prediction_text=f"An error occurred: {str(e)}")

# --------------------- Brain Disease Prediction ---------------------
@app.route("/predict_brain", methods=["POST"])
def predict_brain():
    try:
        # Collect data from the form (ensure consistent naming)
        data = {
            "gender": request.form["Gender"],  # Match case and underscore
            "age": float(request.form["Age"]),
            "hypertension": int(request.form["Hypertension"] == 'yes'),  # Convert 'yes'/'no' to 1/0
            "heart_disease": int(request.form["HeartDisease"] == 'yes'),  # Same for 'HeartDisease'
            "ever_married": request.form["EverMarried"],  # Adjusted name
            "work_type": request.form["WorkType"],  # Adjusted name
            "Residence_type": request.form["ResidenceType"],  # Adjusted name
            "avg_glucose_level": float(request.form["GlucoseLevel"]),
            "bmi": float(request.form["BMI"]),
            "smoking_status": request.form["SmokingStatus"],  # Adjusted name
        }

        # Preprocess input data
        numeric_cols = ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi"]
        categorical_cols = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
        input_preprocessed = preprocess_data(data, numeric_cols, categorical_cols, encoder=encoder_brain)

        probabilities = model_brain.predict_proba(input_preprocessed)
    
        risk_probability = probabilities[0][1] * 100  # Convert to percentage

        output = f"{risk_probability:.2f}% chance of being at risk of brain disease"

        if 0 <= risk_probability <= 30:
            advice = (
                "Tips: Engage in regular physical and mental exercises, such as walking or solving puzzles. "
                "Maintain a diet rich in omega-3 fatty acids, fruits, and vegetables. "
                "Avoid smoking and excessive alcohol consumption."
            )
        elif 31 <= risk_probability <= 60:
            advice = (
                "Tips: Schedule regular check-ups with a neurologist to monitor brain health. "
                "Practice mindfulness or meditation to reduce stress. "
                "Limit screen time and ensure proper sleep hygiene."
            )
        elif 61 <= risk_probability <= 100:
            advice = (
                "Tips: Consult a healthcare provider for a detailed evaluation and follow recommended treatments. "
                "Avoid high-stress environments and focus on a balanced lifestyle. "
                "Incorporate brain-boosting activities, such as learning a new skill or language."
            )
        else:
            advice = "Invalid risk percentage. Please check the input values."
    
        # Return the results with two prediction texts
        return render_template(
            "result.html",
            prediction_text1=f"The person has {output}.",
            prediction_text2=advice
        )
    except Exception as e:
        return render_template("result.html", prediction_text=f"An error occurred: {str(e)}")
    
# --------------------- Run Flask App ---------------------
if __name__ == '__main__':
    app.run(debug=True)
