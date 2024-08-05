import secrets
import string
from asyncio import Event
import pandas as pd
from pathlib import Path
from database.db_utils import get_connection


def generate_randon_report_id(length: int) -> str:
    characters = string.ascii_uppercase
    random_str = ''.join(secrets.choice(characters) for _ in range(length))
    return random_str


async def trigger_report_gen(new_report_id: str, status_event: Event) -> None:
    """
    TODO: manipulate DFs to generate report
    trigger report generation and store against new_report_id in the database
     and generate a {new_report_id}.csv file.
    :param: new_report_id, status_event
    :return: None
    """
    # connect to the database
    engine = get_connection()

    store_status_df: pd.DataFrame = pd.read_sql_table('store_status', con=engine)
    time_zone_df: pd.DataFrame = pd.read_sql_table('time_zone', con=engine)
    menu_hours_df: pd.DataFrame = pd.read_sql_table('menu_hours', con=engine)

    # manipulate above DFs to get the desired report in result_df
    report_df: pd.DataFrame()
    # generate csv from result_df
    generate_report_csv(new_report_id, report_df)

    # set coroutine as complete
    status_event.set()


def generate_report_csv(report_id: str, report_df: pd.DataFrame) -> None:
    """
    create a {report_id}.csv file.
    :param: report_id: str, report_df: pd.DataFrame
    :return: None
    """
    filepath = Path(f'./generated_csv/{report_id}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    report_df.to_csv(filepath)
