from joblib import load

file = load("./content/elon_data.pkl")

elon_topic = [
    "doge send money",
    "owners tesla note",
    "el",
    "situation sticky",
    "flying object booster starship",
    "pressure compressor air",
    "got a",
    "heroes hero",
    "tesla",
    "20 raptor outer engine",
    "feud twitter",
    "ramp energy model tesla 3 sustainable",
    "methods manufacturing improvements",
    "yeah",
    "interesting tech",
    "sure",
    "m impressive",
    "le ahem interesting",
    "yes",
]


cluster = file[1]
vector = file[0][0]
tweets = file[0][1]

print(cluster, vector)
