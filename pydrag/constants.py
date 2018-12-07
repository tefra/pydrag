from enum import Enum


class Period(Enum):
    overall = "overall"
    week = "7day"
    month = "1month"
    quarter = "3month"
    semester = "6month"
    year = "12month"
