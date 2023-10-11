from datetime import datetime
from datetime import timedelta
def compareDatetime(aDateTime = datetime.now(),bDateTime = datetime.now()):
    aDt = aDateTime.replace(second=0,microsecond=0)
    bDt = bDateTime.replace(second=0,microsecond=0)
    return aDt > bDt;