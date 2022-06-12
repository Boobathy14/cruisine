from flask import Flask, render_template, request
import pandas as pd
import pickle
import os


app = Flask(__name__)
model = pickle.load(open('xgb.pkl','rb'))

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        vote = int(request.form['vote'])
        cost = float(request.form['cost'])
        type_food = int(request.form['type_food'])
        rateing = int(request.form['rateing'])
        table_booking = request.form['table_booking']
        city = request.form['city']
        o_order = request.form['O_order']
        date_month = request.form['date']
        order_month = int(pd.to_datetime(date_month,format="%Y-%m-%dT%H:%M").day)
        order_day = int(pd.to_datetime(date_month, format="%Y-%m-%dT%H:%M").month)
        
        print(o_order,table_booking, rateing,vote,cost,type_food, city,	order_day,order_month)
        prediction = model.predict([[o_order,table_booking, rateing,vote,cost,type_food, city,	order_day,order_month]])
        
        output = round(prediction[0],2)
        output = int(output)

        if output < 0:
            return render_template('home.html', prediction_text = "Neither of the Food is in Demand")
        else:
            dict = {1:'North Indian',2: 'Chinese' ,3:'Cafe',4: 'South Indian',5: 'Pizza',6:'Italian' ,7:'Bakery',
 8:'Biryani' ,9:'Street Food',10: 'Burger',11:'Fast Food',12: 'Ice Cream', 13: 'Healthy Food',14: 'Asian',15:'Desserts' ,16:'Goan' ,17:'Continental' ,
18:'Seafood' ,19:'Beverages' ,20:'Mithai',21:'Sandwich', 22: 'Mangalorean' ,23:'Rolls',24: 'Andhra',25:'Thai', 26: 'Salad',27: 'Bengali',
28:'Arabian',29 :'BBQ', 30:'Vietnamese', 31:'Juices' ,32:'Mexican',33: 'Tibetan',34: 'Tea' ,35: 'Momos',36:'Mughlai' ,37: 'Hyderabadi' ,38:'Finger Food'
,39:'Kebab' , 40: 'American special', 41: 'Kerala special',42:'Oriya',43: 'Maharashtrian', 44:'Bohri' ,45:'African',46:'Rajasthani',47:'Turkish', 48:'Tamil',
 49:'Roast Chicken' ,50: 'Gujarati',51:'South American',52: 'Konkan',53: 'Drinks Only',54:'Awadhi',55:'European',56:'Lebanese',57:'Japanese',58:'Modern Indian',59:'Bihari',
 60: 'Australian',61:'Mediterranean',62: 'Chettinad',63:'Steak',64:'Spanish',65:'Portuguese',66:'Parsi',67:'Nepalese',68:'Burmese',69:'North Eastern',70:'Lucknowi',71:'Korean',
 72:'Malaysian',73:'Sushi',74:'Kashmiri',75: 'French',76:'Assamese',77:'Coffee',78:'Charcoal Chicken',79:'Bar Food',80:'Singaporean',81:'Middle Eastern',82:'Naga',83:'Belgian',84:'Indonesian',85:'Russian',86:'Iranian',87:'German',88:'British'}

            return render_template('home.html', prediction_text = "{} dish are the most in demand".format(dict.get(output)))
    return render_template("home.html")


port = int(os.getenv("PORT"))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
