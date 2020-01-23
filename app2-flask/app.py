import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

class DynamicPricingModel:
    # parameters
    prices = [1.99, 2.49, 2.99, 3.49, 3.99, 4.49]
    alpha_0 = 30.00     # parameter of the prior distribution
    beta_0 = 1.00       # parameter of the prior distribution
    p_theta = []
    price_index_offered = 0

    def __init__(self):
        for p in self.prices:
            self.p_theta.append({'price': p, 'alpha': self.alpha_0, 'beta': self.beta_0})
    
    def sample_demands_from_model(self, p_theta):
        return list(map(lambda v: 
                np.random.gamma(v['alpha'], 1/v['beta']), self.p_theta))
    
    def optimal_price(self):
        demands = self.sample_demands_from_model(self.p_theta)

        print("demands:", ["%.2f"%demand for demand in demands])

        price_index = np.argmax(np.multiply(self.prices, demands))
        self.price_index_offered = price_index
        return price_index, self.prices[price_index]

    def update(self, demand_t):
        demand_t = int(demand_t)
        v = self.p_theta[self.price_index_offered]
        v['alpha'] = v['alpha'] + demand_t
        v['beta'] = v['beta'] + 1

model = DynamicPricingModel()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    try:
        int_features = [float(x) for x in request.form.values()]
        observed_demand = int_features[0]
        model.update(observed_demand)
        t, optimal_price = model.optimal_price()
        
    except:
        t, optimal_price = model.optimal_price()

    return render_template('index.html', prediction_text='Optimal price $ {}'.format(optimal_price))



if __name__ == "__main__":
    app.run(debug=True)