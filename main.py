from asyncio import Event, create_task
from fastapi import FastAPI
from starlette.responses import FileResponse, Response
import os
import json
from crud import trigger_report_gen, generate_randon_report_id

app = FastAPI()
status_event = Event()


@app.get('/trigger_report')
async def trigger_report() -> str:
    global status_event

    # generating a report_id with length 5
    new_report_id = generate_randon_report_id(length=5)

    # creating an asynchronous task from a coroutine.
    # why not threading? - "threading is for working in parallel, async is for waiting in parallel"
    create_task(trigger_report_gen(new_report_id=new_report_id, status_event=status_event))
    return f'generating report with report_id {new_report_id}'


@app.get('/get_report/{report_id}')
def get_report(report_id: str):
    global status_event

    # if the trigger_report event is running respond with 'Running'.
    while not status_event.is_set():
        return Response(content=json.dumps({'message': 'Running'}), status_code=422)

    # if the csv file is not present in the directory that means trigger_report event has finished its task
    # but csv file not generated hence, maybe invalid report_id, so, respond with an error.
    if not os.path.exists(f'./generated_csv/{report_id}.csv'):
        return Response(content=json.dumps({'message': 'Report not found'}), status_code=404)

    # if csv file is present in the directory that means trigger_report event has finished its task
    # and a {report_id}.csv file is generated, return it.
    return FileResponse(f'./generated_csv/{report_id}.csv', media_type='application/octet-stream',
                        filename=f'{report_id}.csv')
