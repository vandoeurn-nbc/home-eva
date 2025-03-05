import pickle

house_model = pickle.load(open('model/house_rf.sav', 'rb'))
condo_model = pickle.load(open('model/condo_rf.sav', 'rb'))
land_model = pickle.load(open('model/land_rf.sav', 'rb'))

def estimate_price(property_type, latitude, longitude, size_value, bedrooms_value, bathrooms_value):
    result = []
    if property_type == 1:
        result = house_model.predict([[latitude, longitude, size_value, bedrooms_value, bathrooms_value]])
    if property_type == 2:
        result = condo_model.predict([[latitude, longitude, size_value]])
    if property_type == 3:
        result = land_model.predict([[latitude, longitude, size_value]])
    # price = '%.0f'%(result[0])
    return '${:,.0f}'.format(result[0])

if __name__ == "__main__":
    print(estimate_price(1, 11.547598, 104.917943, 120, 4, 4))