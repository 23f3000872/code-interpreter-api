from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import StringIO
import sys
import traceback
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str


@app.post("/code-interpreter")
def code_interpreter(req: CodeRequest):
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(req.code)

        output = sys.stdout.getvalue()

        return {
            "error": [],
            "result": output
        }

    except Exception:
        tb = traceback.format_exc()

        match = re.findall(r'File "<string>", line (\d+)', tb)

        error_lines = [int(x) for x in match]

        return {
            "error": error_lines,
            "result": tb
        }

    finally:
        sys.stdout = old_stdout


@app.get("/")
def root():
    return {"message": "Code Interpreter API Running"}