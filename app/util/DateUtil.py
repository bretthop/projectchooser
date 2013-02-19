FULL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def formatFullDatetime(datetimeObj):
    return formatDatetime(datetimeObj, FULL_DATETIME_FORMAT)

def formatDatetime(datetimeObj, format):
    return datetimeObj.strftime(format)
