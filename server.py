from flask import Flask, Response, request, jsonify
import pandas as pd
import numpy 
from flask_cors import CORS
import os
from help.test import load_csv,save_csv

app = Flask(__name__)
CORS(app)

# # Read the contents of the CSV file into a DataFrame
# df = pd.read_csv("diamonds.csv")

# # Insert a new column at the beginning of the DataFrame with the id values
# df.insert(0, "id", range(1, len(df) + 1))

# # Write the modified DataFrame back to the CSV file
# df.to_csv("diamonds.csv", index=False)
diamonds_df = pd.read_csv("diamonds.csv")

@app.route("/diamonds", methods=["GET"])
def get_diamonds():
    diamonds = load_csv()
    # print(diamonds)
    return diamonds

# @app.route("/diamonds/<int:diamond_id>", methods=['GET'])
# def get_diamond(diamond_id):
#     global diamonds_df
#     diamond = diamonds_df.loc[diamonds_df["id"] == diamond_id].to_dict(orient='records')
#     return diamond

# @app.route("/diamonds/int:id", methods=["GET"])
# def get_diamond(id):
#     diamond = diamonds_df[diamonds_df["id"] == id]
#     return diamond.to_json()

    
@app.route("/max", methods=["GET"])
def max_price():
    global diamonds_df
    ls=[]
    max_price = diamonds_df["price"].max()
    ls.append(int(max_price))
    return ls
    
@app.route("/mean", methods=["GET"])
def mean_price():
    global diamonds_df
    ls=[]
    mean_price = diamonds_df["price"].mean()
    ls.append(int(mean_price))
    return ls

@app.route("/ideal", methods=["GET"])
def ideal_count():
    global diamonds_df
    ls=[]
    ideal_count = diamonds_df[diamonds_df["cut"] == "Ideal"].shape[0]
    ls.append(int(ideal_count))
    return ls

@app.route("/color", methods=["GET"])
def color_count():
    global diamonds_df
    ls=[]
    color_count = len(diamonds_df["color"].unique())
    ls.append(int(color_count))
    return ls

@app.route("/median", methods=["GET"])
def median_carat():
    global diamonds_df
    ls=[]
    premium_carats = diamonds_df[diamonds_df["cut"] == "Premium"]["carat"]
    median_carat = premium_carats.median()
    ls.append(int(median_carat))
    return ls

@app.route("/cut_avg", methods=["GET"])
def cut_carat_avg():
    global diamonds_df
    ls=[]
    cut_carat_avg = diamonds_df.groupby("cut")["carat"].mean()
    ls.append(str(cut_carat_avg))
    return ls

@app.route("/color_avg", methods=["GET"])
def color_price_avg():
    global diamonds_df
    ls=[]
    color_price_avg = diamonds_df.groupby("color")["price"].mean()
    ls.append(str(color_price_avg))
    return ls

# @app.route("/diamonds", methods=["POST"])
# def add_diamond():
#   data = request.get_json()
#   global diamonds_df
#   diamonds_df = diamonds_df.append(data, ignore_index=True)
#   diamonds_df.to_csv("diamonds.csv", index=False)
#   return data


@app.route("/diamonds", methods=['POST'])
def add_diamond():
    global diamonds_df
    data = request.get_json()
    if diamonds_df.empty:
        data["id"] = 1
    else:
        last_row = diamonds_df.tail(1)
        last_id = int(last_row.id.iloc[0])
        data["id"] = last_id + 1
    diamonds_df = pd.concat([diamonds_df, pd.DataFrame([data])], ignore_index=True)
    diamonds_df.dropna(inplace=True)
    diamonds_df.to_csv("diamonds.csv", index=False)
    return data



# @app.route("/diamonds/int:id", methods=["PUT"])
# def update_diamond(id):
#   data = request.get_json()
#   diamonds_df.loc[diamonds_df["id"] == id, "carat"] = data["carat"]
#   diamonds_df.loc[diamonds_df["id"] == id, "color"] = data["color"]
#   diamonds_df.loc[diamonds_df["id"] == id, "cut"] = data["cut"]
#   diamonds_df.to_csv("diamonds.csv", index=False)
#   return data

@app.route("/dia", methods=['PUT'])
def update_diamond():
    diamonds = load_csv()
    data = request.get_json()
    found = False
    # print(id)
    for i,d in enumerate(diamonds):
        print(d["id"])
        if d["id"] ==data["id"]:
            diamonds[i]["price"] = data["price"]
            found = True
            if found : print("found")
            break
    if found is False:
        return { "error": "diamond not found" }
    save_csv(diamonds)
    return diamonds



@app.route("/diam/<id>", methods=['DELETE'])
def delete_diamond(id):
    id = int(id)
    print(id)
    diamonds_df = pd.read_csv('diamonds.csv')
    # print(diamonds_df.info())
    # print(len( diamonds_df.loc[diamonds_df['id'] == id]))
    if len( diamonds_df.loc[diamonds_df['id'] == id]) >0:
        print("innnnnnnnnnnnnnnn")
        # print(diamonds_df.info())
        lst= diamonds_df.index[diamonds_df['id'] == id].tolist()
        if len(lst ) > 0:
            diamonds_df=diamonds_df.drop(diamonds_df.index[[lst[0]]])
        print(diamonds_df.info())
        # diamonds_df.drop(id, inplace=True)
        diamonds_df.to_csv('diamonds.csv', index=False)
        return jsonify({'message': 'diamond deleted successfully'}), 200
    else:
        return jsonify({'message': 'diamond not found'}), 500
# @app.route("/diamonds/<int:id>", methods=['DELETE'])
# def delete_diamond(id):
#     global diamonds_df
#     df = pd.read_csv(diamonds_df)
#     df = df[df.id != id]
#     df.to_csv(diamonds_df, index=False)
#     return jsonify({"message": "Diamond with id {} deleted.".format(id)})

@app.route("/clean")
def killthemall():
    save_csv([])
    return load_csv()



# @app.route("/diamonds/int:id", methods=["DELETE"])
# def delete_diamond(id):
#    diamonds_df.drop(diamonds_df[diamonds_df["id"] == id].index, inplace=True)
#    diamonds_df.to_csv("diamonds.csv", index=False)
#    return {"message": "Diamond with id {} has been deleted.".format(id)}

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)