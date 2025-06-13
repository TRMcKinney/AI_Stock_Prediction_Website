# AI_Stock_Prediction_Website
Online AI Stock predictor - | https://ai-stock-predictorr.netlify.app/ |

Building on the models developed for the Stock-Price-Prediction repo (https://github.com/TRMcKinney/Stock-Price-Prediction)
Now will incorporate continuous learning based on users past predictions (model persistence)

- Front End (Vue, hosted on Netlify)
- Back End (FastAPI, hosted on Render)
- Database (Supabase - PostgreSQL)


# Notes on Architecture

bulk_load_full_history.py = 

fetch_and_upload.py = 

main.py = 

model.py = 




FetchLogsModal.vue = A pop up window for when you click the 'Fetch Latest Stock Data' button for a terminal with printouts of the process of the print statements of the fetch_and_upload.py


# To Do
- Make data checker into a button for manual checking - the automatic function when fetching new data just doesn't seem to work
- Have a model selector dropdown to select version of the predicting model
      - basic neural network LSTM (the current one) - although needs fine tuning still
      - LSTM with memory
      - LSTM with memory and sentiment analysis module
- Then will need new database table to track predictions and by which model
- Table/visualisation for each models past results and their accuracy
- New card with generic stock data analysis - (Balance Sheet values, total Revenue, Net Income, Operating Costs, Costs of Revenue, Operating Income, (Operating Income / Total Revenue) x 100, Earnings Per Share (EPS), Price-to-Earnings Ratio (P/E), Price to Sales Ratio (P/S), Debt to Equity Ratio, Return on Equity (ROE), Trend Analysis, Support and Resistance Levels, Moving Averages, Relative Strength Index (RSI), Valuation Metrics, Discounted Cash Fow (DCF) Analysis, Enterprise Value (EV/EBITDA), PEG Ratio)
      Another model version (LSTM with memory and sentiment analysis module and stock data analysis)?
