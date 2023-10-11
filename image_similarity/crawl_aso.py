import requests
import json
# import datetime
from datetime import datetime
import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime(year, month, day)
# Cấu hình các thông tin cần thiết để gọi API
api_url = 'https://admin2.kido.vn/mooncake-api/api/aso/order/listV2'
params = {"aggregations":"region_id,product_type_id,distributor_id,shop_province_id,area_id,place_id","productIds":[],"jsonQuery":{"match_all":{}}}
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbl9zcCI6MTMsImRpc3RyaWJ1dG9yX2ludmVudG9yeV9pZHMiOlsxMDA0LDEwMDUsMTAwNiwxMDEzLDEwMTQsMTAxNSwxMDE2LDEwMTcsMTEwMSwxMTExLDIyMTJdLCJncm91cF9pZCI6MSwibmFtZSI6IsSQ4bq3bmcgVOG6pW4gVMOgaSIsImRpc3RyaWJ1dG9yX2lkcyI6WzEwMDQsMTAwNSwxMDA2LDEwMTMsMTAxNCwxMDE1LDEwMTYsMTAxNywxMTAxLDExMTEsMjIxMl0sImV4cCI6MTY4NDQwMTYwMCwiaWF0IjoxNjgzNzk2ODAwfQ.9RKyPwzgyits4qm0EY3JEK_U0IwM84CdlP1CYQiOKiQ',
}

# Tạo đối tượng date đại diện cho tháng 1/2022
start_date = datetime(2021, 1, 1)

# Tạo đối tượng date đại diện cho tháng 4/2023
end_date = datetime(2023, 5, 1)

# Lặp qua từng tháng
current_date = start_date
while current_date < end_date:
    # In ra tháng và năm hiện tại
    print(current_date.strftime("%B %Y"))
    date_after_month = add_months(current_date, 1)
    fromTs = round(datetime.timestamp(current_date) * 1000)
    toTs = round(datetime.timestamp(date_after_month) * 1000 - 1)
    params["fromTime"] = fromTs
    params["toTime"] = toTs

# Gọi API và lưu response vào file
    response = requests.post(api_url, json=params, headers=headers)
    if response.status_code == 200:
        with open("aso_{month}-{year}.json".format(month=current_date.month, year=current_date.year), 'w', encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False)
        print('API response saved to file api_response.json', response.status_code )
    else:
        print('Error calling API:', response.status_code, response.reason)

    # Tính toán ngày đầu tiên của tháng tiếp theo
    year = current_date.year + (current_date.month // 12)
    month = current_date.month % 12 + 1
    current_date = datetime(year, month, 1)
