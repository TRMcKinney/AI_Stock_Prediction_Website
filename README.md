# AI_Stock_Prediction_Website
Online AI Stock predictor

Building on the models developed for the Stock-Price-Prediction repo (https://github.com/TRMcKinney/Stock-Price-Prediction)
Now will incorporate continuous learning based on users past predictions (model persistence)

- Front End (Vue, hosted on Netlify)
- Back End (FastAPI, hosted on Render)
- Database (Supabase - PostgreSQL)


Workflow :- 
At ~00:05 each day:
 - Fetch the latest Apple (AAPL) stock data
 - Save it to a table in Supabase

Immediately after:
 - Retrain the model on the full historical data now in Supabase
 - Save the model to disk (or cloud storage)

For the rest of the day:
 - When a user clicks "Predict", the backend loads that model and predicts the price in 10 days from now

Repeat this cycle daily
