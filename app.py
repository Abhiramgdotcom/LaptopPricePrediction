from flask import Flask,render_template,request
import math
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
with open("laptop_price_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load column names
with open("model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
    # Get form data
        company = request.form["company"]
        typename = request.form["typename"]
        ram = int(request.form["ram"])
        weight = float(request.form["weight"])

        inches = float(request.form["inches"])
        resolution = request.form["resolution"]

        touchscreen = int(request.form["touchscreen"])
        ips = int(request.form["ips"])

        cpu_brand = request.form["cpu_brand"]
        cpu_family = request.form["cpu_family"]

        ssd = int(request.form["ssd"])
        hdd = int(request.form["hdd"])
        hybrid = int(request.form["hybrid"])
        flash = int(request.form["flash"])

        gpu_brand = request.form["gpu_brand"]
        opsys = request.form["opsys"]

    # Calculate PPI
        x_res, y_res = map(int, resolution.split("x"))
        ppi = math.sqrt(x_res**2 + y_res**2) / inches

        input_data = {col: 0 for col in model_columns}
        input_data["Ram"] = ram
        input_data["Weight"] = weight
        input_data["TouchScreen"] = touchscreen
        input_data["IPS"] = ips
        input_data["PPI"] = ppi
        input_data["SSD"] = ssd
        input_data["HDD"] = hdd
        input_data["Hybrid"] = hybrid
        input_data["Flash"] = flash

        if f"Company_{company}" in input_data:
            input_data[f"Company_{company}"] = 1

        if f"TypeName_{typename}" in input_data:
            input_data[f"TypeName_{typename}"] = 1

        if f"Cpu_Brand_{cpu_brand}" in input_data:  
            input_data[f"Cpu_Brand_{cpu_brand}"] = 1

        if f"Cpu_Family_{cpu_family}" in input_data:
            input_data[f"Cpu_Family_{cpu_family}"] = 1

        if f"Gpu_Brand_{gpu_brand}" in input_data:
            input_data[f"Gpu_Brand_{gpu_brand}"] = 1

        if f"OpSys_{opsys}" in input_data:
            input_data[f"OpSys_{opsys}"] = 1

        import pandas as pd

        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]


        return render_template(
        "index.html",
        prediction=round(prediction, 2),
        form=request.form
        )
    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error: {e}",
            form=request.form
        )
    

if __name__ == "__main__":
    app.run(debug=True)