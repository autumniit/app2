# parameters
prices = [1.99, 2.49, 2.99, 3.49, 3.99, 4.49]
alpha_0 = 30.00     # parameter of the prior distribution
beta_0 = 1.00       # parameter of the prior distribution

# parameters of the true (unknown) demand model
true_slop = 50
true_intercept = -7

# prior distribution for each price
p_theta = []
for p in prices:
    p_theta.append({'price': p, 'alpha': alpha_0, 'beta': beta_0})

def sample_actual_demand(price): 
    demand = true_slop + true_intercept * price
    return np.random.poisson(demand, 1)[0]

# sample mean demands for each price level
def sample_demands_from_model(p_theta):
    return list(map(lambda v: 
           np.random.gamma(v['alpha'], 1/v['beta']), p_theta))

# return price that maximizes the revenue
def optimal_price(prices, demands):
    price_index = np.argmax(np.multiply(prices, demands))
    return price_index, prices[price_index]

# simulation loop        
for t in range(0, T):
    print("Iteration", t)
    demands = sample_demands_from_model(p_theta)
    print("demands:", ["%.2f"%demand for demand in demands])
    price_index_t, price_t = optimal_price(prices, demands)
    print("optimal price:", price_t)
    
    # offer the selected price and observe demand
    demand_t = sample_actual_demand(price_t)
        
    # update model parameters
    v = p_theta[price_index_t]
    v['alpha'] = v['alpha'] + demand_t
    v['beta'] = v['beta'] + 1