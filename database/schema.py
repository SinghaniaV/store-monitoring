from sqlalchemy import Column, INT, BIGINT, VARCHAR, TIME, TIMESTAMP
from sqlalchemy.orm import declarative_base

# inherit from this Base class to create each of the ORM models
Base = declarative_base()


class TimeZone(Base):
    """
    Class for time_zone table
    """
    __tablename__ = 'time_zone'

    id = Column(INT, primary_key=True, autoincrement=True)
    store_id = Column(BIGINT, index=True)
    timezone_str = Column(VARCHAR(50))

    def __init__(self, store_id: INT, timezone_str: VARCHAR):
        self.store_id = store_id
        self.timezone_str = timezone_str

    def __repr__(self):
        return f'({self.store_id}, {self.timezone_str})'


class StoreStatus(Base):
    """
    Class for store_status table
    """
    __tablename__ = 'store_status'

    id = Column(INT, primary_key=True, autoincrement=True)
    store_id = Column(BIGINT, index=True)
    status = Column(VARCHAR(10))
    timestamp_utc = Column(TIMESTAMP)

    def __init__(self, store_id: BIGINT, status: VARCHAR, timestamp_utc: TIMESTAMP):
        self.store_id = store_id
        self.status = status
        self.timestamp_utc = timestamp_utc

    def __repr__(self):
        return f'({self.store_id}, {self.status}, {self.time_stamp_utc})'


class MenuHours(Base):
    """
    Class for menu_hours table
    """
    __tablename__ = 'menu_hours'

    id = Column(INT, primary_key=True, autoincrement=True)
    store_id = Column(BIGINT, index=True)
    day = Column(INT)

    # If data is missing for a store, assuming it is open 24*7
    start_time_local = Column(TIME)
    end_time_local = Column(TIME)

    def __init__(self, store_id: BIGINT, day: INT, start_time_local: TIME, end_time_local: TIME):
        self.store_id = store_id
        self.day = day
        self.start_time_local = start_time_local
        self.end_time_local = end_time_local

    def __repr__(self):
        return f'({self.store_id}, {self.start_time_local}, {self.end_time_local})'

class MenuHoursUTC(Base):
    """
    Class for menu_hours table
    """
    __tablename__ = 'menu_hours_utc'

    id = Column(INT, primary_key=True, autoincrement=True)
    store_id = Column(BIGINT, index=True)
    day = Column(INT)

    # If data is missing for a store, assuming it is open 24*7
    start_time_utc = Column(TIMESTAMP)
    end_time_utc = Column(TIMESTAMP)

    def __init__(self, store_id: BIGINT, day: INT, start_time_utc: TIME, end_time_utc: TIME):
        self.store_id = store_id
        self.day = day
        self.start_time_utc = start_time_utc
        self.end_time_utc = end_time_utc

    def __repr__(self):
        return f'({self.store_id}, {self.start_time_local}, {self.end_time_local})'


class Reports(Base):
    """
    Class for report table.
    we will be storing all the report_ids and corresponding data accordingly.
    if we have to retrieve all the reports generated so far we will return unique entries in report_id column
    """

    __tablename__ = 'reports'

    id = Column(INT, primary_key=True, autoincrement=True)
    report_id = Column(VARCHAR(10), index=True)
    store_id = Column(BIGINT, index=True)
    uptime_last_hour = Column(INT)
    uptime_last_day = Column(INT)
    uptime_last_week = Column(INT)
    downtime_last_hour = Column(INT)
    downtime_last_day = Column(INT)
    downtime_last_week = Column(INT)

    def __init__(self, store_id: BIGINT, uptime_last_hour: INT, uptime_last_day: INT,  uptime_last_week: INT,
                 downtime_last_hour: INT,  downtime_last_day: INT, downtime_last_week: INT):
        self.store_id = store_id
        self.uptime_last_hour = uptime_last_hour
        self.uptime_last_day = uptime_last_day
        self.uptime_last_week = uptime_last_week
        self.downtime_last_hour = downtime_last_hour
        self.downtime_last_day = downtime_last_day
        self.downtime_last_week = downtime_last_week

    def __repr__(self):
        return f'({self.store_id}, {self.uptime_last_hour}, {self.uptime_last_day}, {self.downtime_last_hour}, ' \
               f'{self.downtime_last_week})'
