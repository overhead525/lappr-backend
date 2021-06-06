from datetime import datetime
from typing import Dict, Tuple

Username = str
Amount = float
DiffObject = Dict[Username, Amount]

Currency = str
AmountOwned = float
AmountChanged = float
PortfolioID = str
UpdatedAt = datetime
Portfolio = Dict[Currency, AmountOwned]
PortfolioDiff = Dict[Currency, AmountChanged]
PortfolioObject = Tuple[PortfolioID, Portfolio, UpdatedAt, Username]

TransactionID = str
Timestamp = datetime
OrderType = str
PaidWith = str
OrderAmount = float
From = DiffObject
To = DiffObject
TransactionObject = Tuple[TransactionID, Timestamp, OrderType, Currency, PaidWith, OrderAmount, From, To]

Role = str
JoinedDate = datetime
GroupMemberRow = Tuple[Role, Username, JoinedDate]


class User:
    role: str
    username: str
    joined_date: datetime

    def __init__(self, role: str, username: str, joined_date: str):
        role = role
        username = username
        joined_date = datetime.fromisoformat(joined_date)
