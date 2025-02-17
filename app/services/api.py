from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

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
        print("filtered_data:", filtered_data)
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
