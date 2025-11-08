#from search import search

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, StreamingResponse
import uvicorn
from io import BytesIO
from pathlib import Path
import os
from blast import *

app = FastAPI()

# Use current directory for templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getconfig")
async def getconfig(request: Request):
    return json.dumps(load_config())

@app.get("/download")
async def download_endpoint(request: Request, type: int, folderid: str):
    if type == 1:
        csv_list = os.listdir(folderid)
        csv_paths = []
        for csv in csv_list:
            if csv[-3:] == "csv":
                csv_paths.append(f'{folderid}/{csv}')
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in csv_paths:
                if os.path.exists(file_path):
                    zipf.write(file_path, arcname=os.path.basename(file_path))
    
        zip_buffer.seek(0)
    
        # Return as streaming ZIP response
        return StreamingResponse(
            zip_buffer,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename={folderid}_csv_bundle.zip"}
        )
        print("download req for CSV")
    elif type == 2:
        return FileResponse(
            f'{folderid}/BLAST_Full_Report.pdf',
            media_type='application/pdf',
            filename=f'{folderid}_full_report.pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{folderid}_full_report.pdf"'
            }
        )
    elif type == 3:
        return FileResponse(
            f'{folderid}/anomaly_output.pdf',
            media_type='application/pdf',
            filename=f'{folderid}_anomaly_report.pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{folderid}_anomaly_report.pdf"'
            }
        )
    elif type == 4:
        return FileResponse(
            f'{folderid}/inputs.fasta',
            media_type='chemical/seq-na-fasta',
            filename=f'{folderid}_inputs.fasta',
            headers={
                'Content-Disposition': f'attachment; filename="{folderid}_inputs.fasta"'
            }
        )

@app.get("/preview")
async def download_endpoint(request: Request, type: int, folderid: str):
    if type == 2:
        return FileResponse(
            f'{folderid}/BLAST_Full_Report.pdf',
            media_type='application/pdf',
            filename=f'{folderid}_full_report.pdf',
            headers = {
                'Content-Disposition': f'inline; filename="{folderid}_anomaly_report.pdf"',
                'Content-Type': 'application/pdf'
            }
        )
    elif type == 3:
        return FileResponse(
            f'{folderid}/anomaly_output.pdf',
            media_type='application/pdf',
            filename=f'{folderid}_anomaly_report.pdf',
            headers = {
                'Content-Disposition': f'inline; filename="{folderid}_anomaly_report.pdf"',
                'Content-Type': 'application/pdf'
            }
        )



@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            asyncio.create_task(run_blast_job(data, websocket))

        except Exception as e:
            await websocket.close()
            break


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


#jsonobj = search("Etheostoma olmstedi isolate EolmZR cytochrome b (cytb) gene,")
#pprint.pprint(jsonobj)
