import numpy as np
import pickle

# T = 100

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

pickle.dump(model, open('model.pkl','wb'))

# for t in range(0, T):
#     print("Iteration", t)
#     optimal_price_index, optimal_price = model.optimal_price()
#     print("optimal price: ", optimal_price)
#     model.update(input("Demand of "  + str(optimal_price) + ": "))