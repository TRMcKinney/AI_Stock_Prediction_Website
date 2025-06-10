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
