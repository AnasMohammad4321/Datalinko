from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi import Query  

from utils import convert_all_columns_to_snake_case

from agents.intent import IntentAgent
from agents.ecommerce_assistant import NormalEcommerceAssistantAgent
from agents.memory_agent import ConversationMemoryAgent
from agents.response_formatter import ResponseFormatterAgent
from agents.query_generator import SQLQueryAgent
from agents.infer_schema import SchemaInferenceAgent

import os
import sqlite3
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI()

load_dotenv()

CSV_PATH = '../../data/raw/sample_data.csv'
DB_PATH = 'sales_database.sqlite'

try:
    schema_agent = SchemaInferenceAgent(CSV_PATH)
    schema = schema_agent.infer_schema()

    df_chunks = pd.read_csv(CSV_PATH, chunksize=1000)
    df = pd.concat(chunk for chunk in df_chunks)
    df = convert_all_columns_to_snake_case(df)
    conn = sqlite3.connect(DB_PATH)
    TABLE_NAME = "sales_table"
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False, method="multi")
    conn.close()
except Exception as e:
    print(f"Error during initialization: {e}")
    exit(1)

intent_agent = IntentAgent()
normal_assistant = NormalEcommerceAssistantAgent()
memory_agent = ConversationMemoryAgent()

class ChatRequest(BaseModel):
    query: str

@app.post('/chat')
async def chat(request: ChatRequest):
    user_query = request.query
    if not user_query:
        raise HTTPException(status_code=400, detail="No query provided")

    context = memory_agent.get_context()
    
    try:
        intent_classification = intent_agent.classify_intent(user_query)

        if intent_classification.intent.lower() == 'query':
            sql_agent = SQLQueryAgent(schema, DB_PATH)
            sql_query = sql_agent.generate_sql_query(user_query, TABLE_NAME)
            query_results = sql_agent.execute_query(sql_query)

            response_agent = ResponseFormatterAgent()
            final_response = response_agent.format_response(user_query, query_results)

            memory_agent.add_interaction(user_query, final_response)
            return JSONResponse(content={"intent": intent_classification.intent, "response": final_response, "results": query_results}, status_code=200)
        else:
            general_response = normal_assistant.generate_response(user_query, context)
            memory_agent.add_interaction(user_query, general_response)
            return JSONResponse(content={"intent": intent_classification.intent, "response": general_response}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

try:
    df = pd.read_csv("../../data/raw/data.csv", low_memory=False)
    df["created_at"] = pd.to_datetime(df["created_at"]) 
except Exception as e:
    raise RuntimeError(f"Error loading data: {str(e)}")

@app.get("/get_filters")
def get_order_filters():
    """Return unique order statuses and min/max created_at dates."""
    try:
        if df.empty or "created_at" not in df.columns or "order_status" not in df.columns:
            raise HTTPException(status_code=500, detail="Data is missing required columns")

        order_statuses = df["order_status"].dropna().unique().tolist()  
        start_date = df["created_at"].dropna().min().strftime("%Y-%m-%d")
        end_date = df["created_at"].dropna().max().strftime("%Y-%m-%d")

        return JSONResponse(content={
            "order_statuses": order_statuses,
            "start_date": start_date,
            "end_date": end_date
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_filtered_data")
def get_filtered_data(
    start_date: str,
    end_date: str,
    order_status: str = Query(..., description="Comma-separated order statuses")
):
    """
    API endpoint to return filtered sales data based on date range and order status.
    """
    try:
        start_date = pd.to_datetime(start_date, errors="coerce")
        end_date = pd.to_datetime(end_date, errors="coerce")

        if pd.isna(start_date) or pd.isna(end_date):
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        if start_date > end_date:
            raise HTTPException(status_code=400, detail="start_date cannot be after end_date")

        statuses = order_status.split(",")

        valid_statuses = df["order_status"].dropna().unique().tolist()
        invalid_statuses = [s for s in statuses if s not in valid_statuses]

        if invalid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid order statuses: {', '.join(invalid_statuses)}"
            )

        filtered_df = df.loc[
            (df["created_at"].between(start_date, end_date)) &
            (df["order_status"].isin(statuses))
        ]

        if filtered_df.empty:
            return JSONResponse(
                content={"message": "No data found for the given filters", "data": []},
                status_code=200
            )

        filtered_df["created_at"] = filtered_df["created_at"].astype(str)  

        filtered_data = filtered_df.fillna("").to_dict(orient="records")  
        return JSONResponse(content={"message": "Success", "data": filtered_data}, status_code=200)

    except HTTPException as e:
        print("HTTPException:", e)
        raise  
    except Exception as e:
        print("Exception:", e)
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
