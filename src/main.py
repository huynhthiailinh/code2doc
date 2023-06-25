from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

import sys

sys.path.append(".")
sys.path.append("..")

app = FastAPI()


class ExecuteRequest(BaseModel):
    language: str = 'java'
    source_code: str = ''


@app.post("/summarize")
async def execute_command(request: ExecuteRequest):
    request.source_code = '''private int findPLV(int M_PriceList_ID) {
  Timestamp priceDate = null;
  String dateStr = Env.getContext(Env.getCtx(), p_WindowNo, _STR);

  if (dateStr != null && dateStr.length() > _NUM)
    priceDate = Env.getContextAsDate(Env.getCtx(), p_WindowNo, _STR);
  else {
    dateStr = Env.getContext(Env.getCtx(), p_WindowNo, _STR);
    if (dateStr != null && dateStr.length() > _NUM)
      priceDate = Env.getContextAsDate(Env.getCtx(), p_WindowNo, _STR);
  }
  
  if (priceDate == null)
    priceDate = new Timestamp(System.currentTimeMillis());

  log.config(_STR + M_PriceList_ID + _STR + priceDate);
  int retValue = _NUM;
  String sql = _STR + _STR + _STR + _STR + _STR + _STR;

  try {PreparedStatement pstmt = DB.prepareStatement(sql, null);
    pstmt.setInt(_NUM, M_PriceList_ID);
    ResultSet rs = pstmt.executeQuery();

    while (rs.next() && retValue == _NUM) {
      Timestamp plDate = rs.getTimestamp(_NUM);
      
      if (!priceDate.before(plDate))
        retValue = rs.getInt(_NUM);
    }

    rs.close();
    pstmt.close();
  } catch (SQLException e) {
    log.log(Level.SEVERE, sql, e);
  }
  
  Env.setContext(Env.getCtx(), p_WindowNo, _STR, retValue);

  return retValue;
}'''

    command = f"../scripts/generate.sh 0 code2jdoc sample.code {request.language} \"{request.source_code}\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    logs = []
    while True:
        output = process.stdout.readline().decode().strip()
        if output == "" and process.poll() is not None:
            break
        logs.append(output)

    return {"summary": logs[-1][2:-2]}
