import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import pickle
df=pd.read_csv("dataset.csv")
vectorizer=TfidfVectorizer()
x=vectorizer.fit_transform(df['question'])
model={d
    "vectorizer":vectorizer,
    "x":x,
    "answers":df['answer'].tolist(),
    "questions":df['question'].tolist()
}
pickle.dump(model,open("model.pk1","wb"))
print("model trained and saved successfully")

