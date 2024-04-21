from flask import Flask, request, render_template

app = Flask(__name__)

HOME_PAGE = '''
<!doctype html>
<html>
<head>
    <title>BMI and BMR Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        input[type=text], input[type=submit], select {
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            width: 200px;
        }
        input[type=submit] {
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
        input[type=submit]:hover {
            background-color: #0056b3;
        }
        h1 {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BMI and BMR Calculator</h1>
        <form action="/calculate" method="post">
            Height (in centimeters): <br><input type="text" name="height"><br>
            Weight (in kilograms): <br><input type="text" name="weight"><br>
            Age: <br><input type="text" name="age"><br>
            Gender: <br><input type="radio" name="gender" value="male" checked> Male
                    <input type="radio" name="gender" value="female"> Female<br>
            Activity Level:
            <select name="activity">
                <option value="1.2">Sedentary: little or no exercise</option>
                <option value="1.375">Lightly active: light exercise/sports 1-3 days/week</option>
                <option value="1.55">Moderately active: moderate exercise/sports 3-5 days/week</option>
                <option value="1.725">Very active: hard exercise/sports 6-7 days a week</option>
                <option value="1.9">Super active: very hard exercise/physical job & exercise 2x/day</option>
            </select><br>
            <input type="submit" value="Calculate BMI and BMR">
        </form>
    </div>
</body>
</html>
'''

RESULT_PAGE = '''
<!doctype html>
<html>
<head>
    <title>BMI and BMR Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
        }
        a:hover {
            background-color: #0056b3;
        }
        h1, h2 {
            color: #333;
        }
        .results {
            font-size: 1.2em;
            margin: 20px 0;
            padding: 10px;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .results p {
            margin: 10px 0;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BMI and BMR Results</h1>
        <div class="results">
            <p>Your BMI is: <strong>{{ bmi }}</strong></p>
            <p>Category: <strong>{{ category }}</strong></p>
            <p>Your BMR is: <strong>{{ bmr }} calories/day</strong></p>
            <p>Your TDEE is: <strong>{{ tdee }} calories/day</strong></p>
        </div>
        <table>
            <tr>
                <th>Goal</th>
                <th>Calories/day</th>
            </tr>
            <tr>
                <td>Maintain weight</td>
                <td>{{ tdee }}</td>
            </tr>
            <tr>
                <td>Mild weight loss <br> 0.5 lb/week</td>
                <td>{{ tdee|safe|int - 250 }}</td>
            </tr>
            <tr>
                <td>Weight loss <br> 1 lb/week</td>
                <td>{{ tdee|safe|int - 500 }}</td>
            </tr>
            <tr>
                <td>Extreme weight loss <br> 2 lb/week</td>
                <td>{{ tdee|safe|int - 1000 }}</td>
            </tr>
        </table>
        <a href="/">Try again</a>
    </div>
</body>
</html>
'''

@app.route('/bmi_bmr_calc')
def bmi_bmr_calc():
    return render_template("bmi_bmr_calc.html")

@app.route('/bmi_bmr_results', methods=['POST'])
def bmi_bmr_results():
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity_factor = float(request.form['activity'])

    bmi = 10000 * (weight / (height * height))
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * activity_factor  # Total Daily Energy Expenditure

    category = classify_bmi(bmi)
    return render_template("bmi_bmr_results.html", bmi="{:.2f}".format(bmi), category=category, bmr="{:.2f}".format(bmr), tdee="{:.2f}".format(tdee))

def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

if __name__ == '__main__':
    app.run(debug=True)
