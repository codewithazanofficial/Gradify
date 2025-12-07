from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle
import numpy as np
user_data = np.array([[9.8, 2, 7, 1, 2.2]])
user_text = 'It hate it.'
def adjust_gpa(user_text, predicted_gpa):
    analyzer = SentimentIntensityAnalyzer()
    ps = analyzer.polarity_scores(user_text)
    return ps['compound'] * 0.4 + predicted_gpa
with open('model_pickel','rb') as f:
    model = pickle.load(f)

gpa = model.predict(user_data)
adjusted_gpa = adjust_gpa(user_text,gpa)
print(gpa)
print(adjusted_gpa)
