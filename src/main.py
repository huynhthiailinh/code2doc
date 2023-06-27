from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()


class ExecuteRequest(BaseModel):
    language: str = 'java'
    source_code: str = ''


@app.post("/summarize")
async def execute_command(request: ExecuteRequest):
    command = f"../scripts/generate.sh 0 code2jdoc sample.code {request.language} \"{request.source_code}\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    logs = []
    while True:
        output = process.stdout.readline().decode().strip()
        if output == "" and process.poll() is not None:
            break
        logs.append(output)

    return {"summary": logs[-1][2:-2]}
