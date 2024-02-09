from cmath import exp
import math
import re
from flask import request
import datetime
from app import db
from functools import wraps
from common.error_response import ErrorResponse
import traceback
from common.base_response import BaseResponse
from flask import jsonifyp


def ExperienceConvert(experience: str):
    if experience == "nan":
        return 0
    yearPattern = re.compile("\d TAHUN")
    yearsPattern = re.compile("\d\d TAHUN")
    yearMonthPattern = re.compile("\d TAHUN \d BULAN")
    monthPattern = re.compile("\d BULAN")
    monthPointPattern = re.compile("\d,\d BULAN")
    untilMonthPattern = re.compile("\d-\d BULAN")
    untilYearPattern = re.compile("\d-\d TAHUN")
    yearPointPattern = re.compile("\d,\d TAHUN")
    yearComaPattern = re.compile("\d.\d TAHUN")
    yearSpacePattern = re.compile("\d TAHUN ")
    minYearPattern = re.compile("- \d TAHUN")
    lowerYearPattern = re.compile("<\d TAHUN")
    lowerSpaceYearPattern = re.compile("< \d TAHUN")
    yearUntilShort = re.compile("\d-\d THN")
    yearPatternShort = re.compile("\d THN")
    skalaPattern = re.compile("SKALA: 1 - 10 = \d")

    if experience is None and experience == "":
        return 0
    elif re.fullmatch(yearPattern, experience):
        return int(experience[0]) * 12
    elif re.fullmatch(yearsPattern, experience):
        return int(experience[0]) * 12
    elif re.fullmatch(yearPointPattern, experience):
        experience = experience[0].replace(",", ".")
        return int(experience) * 12
    elif re.fullmatch(yearMonthPattern, experience):
        experience = (
            experience.replace("TAHUN", "").replace(
                "BULAN", "").replace(" ", "")
        )
        year = int(experience[0]) * 12
        month = int(experience[1])
        return year + month
    elif re.fullmatch(monthPattern, experience):
        return int(experience[0])
    elif re.fullmatch(monthPointPattern, experience):
        experience = experience[0].replace(",", ".")
        return math.floor(int(experience))
    elif re.fullmatch(untilYearPattern, experience):
        experience = experience.replace(
            "TAHUN", "").replace("-", "").replace(" ", "")
        return int(experience[0]) * 12
    elif re.fullmatch(untilMonthPattern, experience):
        experience = experience.replace(
            "MONTH", "").replace("-", "").replace(" ", "")
        return int(experience[1]) - 1
    elif re.fullmatch(minYearPattern, experience):
        experience = experience.replace("- ", "")
        return int(experience[0])
    elif re.fullmatch(lowerYearPattern, experience):
        experience = experience.replace("<", "")
        return int(experience[0])
    elif re.fullmatch(lowerSpaceYearPattern, experience):
        experience = experience.replace("< ", "")
        return int(experience[0])
    elif re.fullmatch(yearComaPattern, experience):
        return int(experience[0]) * 12
    elif re.fullmatch(yearSpacePattern, experience):
        return int(experience[0]) * 12
    elif re.fullmatch(yearUntilShort, experience):
        experience = experience.replace(
            "THN", "").replace("-", "").replace(" ", "")
        return (int(experience[1]) - 1) * 12
    elif re.fullmatch(yearPatternShort, experience):
        return int(experience[0]) * 12
    elif experience != experience:
        return 0
    elif IsNaN(experience):
        return 0
    else:
        return 0


def IsNaN(num):
    try:
        if float("-inf") < float(num) < float("inf"):
            return False
        else:
            return True
    except Exception:
        return False


def checkEmail(email):
    try:
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    except Exception:
        return False


def ConvertAssignmentStatus(status):
    requestStatus = None
    if status is not None:
        if status == "requested" or status == "running" or status == "finished":
            requestStatus = status
    return requestStatus


def FormRequestStatusConvert(status: str):
    status = status.replace("%", "").lower()
    result = ""
    if status == "pending":
        result = "0"
    elif status == "on progress":
        result = "1"
    elif status == "rejected":
        result = "2"
    elif status == "cancelled by client":
        result = "3"
    elif status == "assigned":
        result = "4"

    result = "%{}%".format(result)
    print(result)
    return result


def AssignmentCandidateStatusConvert(status: str):
    status = status.replace("%", "").lower()
    result = ""
    result = ""
    if status == "review":
        result = 0
    elif status == "accepted":
        result = 1
    elif status == "rejected":
        result = 2

    result = "%{}%".format(str(result))

    return result


def ResourcesAssignmentStatusConvert(status: str):
    status = status.replace("%", "").lower()
    result = ""
    if status == "proses":
        result = 0
    elif status == "approve":
        result = 1
    elif status == "reject":
        result = 2
    elif status == "on runing":
        result = 3
    elif status == "done":
        result = 4
    elif status == "terminated":
        result = 5

    result = "%{}%".format(str(result))

    return result


def SupportTicketStatusConvert(status: str):
    status = status.replace("%", "").lower()
    result = ""
    if status == "open":
        result = 0
    elif status == "closed":
        result = 1
    result = "%{}%".format(str(result))

    return result



class ErrorResponseException(BaseException):
    def __init__(self, response: ErrorResponse, message: str = ""):
        self.response = response
        super().__init__(message)

def rollback_db():
    try:
        db.rollback()
    except:
        pass
        
def error_catcher(rollback: bool):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ErrorResponseException as e:
                traceback.print_exc()
                if rollback:
                    rollback_db()
                return e.response.serialize()
            except Exception as e:
                traceback.print_exc()
                if rollback:
                    rollback_db()
                return ErrorResponse(str(e), 500).serialize()

        return wrapper

    return decorator

def validate_required_fields(json, required_fields: list[str]):
    for field in required_fields:
        if field not in json:
            raise ErrorResponseException(ErrorResponse(f'Field {field} is required', 500))