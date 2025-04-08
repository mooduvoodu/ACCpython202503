from polygon import RESTClient

client = RESTClient("dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq")

aggs = []
for a in client.list_aggs(
    "AAPL",
    1,
    "day",
    "2023-01-09",
    "2023-02-10",
    adjusted="true",
    sort="asc",
    limit=120,
):
    aggs.append(a)

print(aggs)
