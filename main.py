# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import control
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PIDRequest(BaseModel):
    kp: float
    ki: float
    kd: float
    g: float = 9.8  # default value for gravity

@app.post("/pid-step-response")
async def calculate_pid_response(request: PIDRequest):
    try:
        # Extract parameters
        kp, ki, kd, g = request.kp, request.ki, request.kd, request.g
        
        # Create transfer function
        numerator = [g * kd, g * kp, g * ki]
        denominator = [1, g * kd, g * kp, g * ki]
        
        # Calculate step response
        system = control.TransferFunction(numerator, denominator)
        time, response = control.step_response(system)
        
        return JSONResponse(content={
            "time": time.tolist(),
            "response": response.tolist(),
            "status": "success"
        })
        
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=400
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)