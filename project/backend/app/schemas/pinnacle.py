from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

class PinnaclePeriod(BaseModel):
    number: int
    sport_id: int
    description: str
    short_description: str
    spread_description: str
    moneyline_description: str
    total_description: str
    team_1_total_description: str
    team_2_total_description: str
    spread_short_description: str
    moneyline_short_description: str
    total_short_description: str
    team_1_total_short_description: str
    team_2_total_short_description: str

class PinnaclePeriodsResponse(BaseModel):
    periods: List[PinnaclePeriod]

class PinnacleSport(BaseModel):
    id: int
    p_id: int
    name: str
    last_call: int
    last: int
    special_last: Optional[int] = None

class PinnacleSportsResponse(BaseModel):
    sports: List[PinnacleSport]

class PinnacleLeague(BaseModel):
    id: int
    sport_id: int
    name: str
    home_team_type: str
    container: str
    league_specials_count: int
    event_specials_count: int
    event_count: int
    has_offerings: bool
    homeTeamType: str

class PinnacleLeaguesResponse(BaseModel):
    leagues: List[PinnacleLeague]

# class PinnacleSpecialMarket(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None
#     event_count: int

# class PinnacleSpecialMarketsResponse(BaseModel):
#     specials: List[PinnacleSpecialMarket]

########################################### SCHEMAS FOR MARKETS ###############################################
class MoneyLine(BaseModel):
    home: Optional[float]
    draw: Optional[float]
    away: Optional[float]

class SpreadLine(BaseModel):
    hdp: float
    alt_line_id: Optional[int]
    home: float
    away: float
    max: int

class TotalLine(BaseModel):
    points: float
    alt_line_id: Optional[int]
    over: float
    under: float
    max: int

class TeamTotalLine(BaseModel):
    points: float
    over: float
    under: float

class TeamTotal(BaseModel):
    home: TeamTotalLine
    away: TeamTotalLine

class PeriodMeta(BaseModel):
    number: int
    max_money_line: int
    max_spread: int
    max_total: int
    max_team_total: int
    open_money_line: bool
    open_spreads: bool
    open_totals: bool
    open_team_total: bool

class Period(BaseModel):
    line_id: int
    number: int
    description: str
    cutoff: str
    period_status: int
    money_line: Optional[MoneyLine]
    spreads: Optional[Dict[str, SpreadLine]] = None
    totals: Optional[Dict[str, TotalLine]] = None
    team_total: Optional[TeamTotal] = None
    meta: Optional[PeriodMeta] = None

class Event(BaseModel):
    event_id: int
    sport_id: int
    league_id: int
    league_name: str
    starts: str
    last: int
    home: str
    away: str
    event_type: str
    live_status_id: int
    parent_id: Optional[int]
    resulting_unit: str
    is_actual: bool
    home_team_type: str
    is_have_odds: bool
    is_have_periods: bool
    is_have_open_markets: bool
    periods: Dict[str, Period]

class PinnacleMarket(BaseModel):
    sport_id: int
    sport_name: str
    last: int
    last_call: int
    events: List[Event]

class PinnacleMarketsResponse(BaseModel):
    markets: List[PinnacleMarket]

########################################### SCHEMAS FOR EVENT DETAILS ###############################################

class PinnacleMoneyLine(BaseModel):
    home: Optional[float]
    draw: Optional[float]
    away: Optional[float]


class PinnacleSpread(BaseModel):
    hdp: float
    alt_line_id: Optional[int]
    home: float
    away: float
    max: int


class PinnacleTotal(BaseModel):
    points: float
    alt_line_id: Optional[int]
    over: float
    under: float
    max: int


class PinnacleTeamTotal(BaseModel):
    points: float
    over: float
    under: float


class PinnacleTeamTotals(BaseModel):
    home: Optional[PinnacleTeamTotal]
    away: Optional[PinnacleTeamTotal]


class PinnaclePeriodMeta(BaseModel):
    number: int
    max_money_line: int
    max_spread: int
    max_total: int
    max_team_total: int
    open_money_line: bool
    open_spreads: bool
    open_totals: bool
    open_team_total: bool


class PinnaclePeriod(BaseModel):
    line_id: int
    number: int
    description: str
    cutoff: str
    period_status: int
    money_line: Optional[PinnacleMoneyLine]
    spreads: Optional[Dict[str, PinnacleSpread]]
    totals: Optional[Dict[str, PinnacleTotal]]
    team_total: Optional[PinnacleTeamTotals]
    meta: Optional[PinnaclePeriodMeta]
    history: Optional[Dict[str, Any]]  # raw dict because it's very nested


class PinnacleEventDetail(BaseModel):
    event_id: int
    sport_id: int
    league_id: int
    league_name: str
    starts: str
    last: int
    home: str
    away: str
    event_type: str
    live_status_id: int
    parent_id: Optional[int]
    resulting_unit: str
    is_actual: bool
    home_team_type: str
    is_have_odds: bool
    is_have_periods: bool
    is_have_open_markets: bool
    periods: Optional[Dict[str, PinnaclePeriod]]


class PinnacleEventDetailsResponse(BaseModel):
    events: List[PinnacleEventDetail]

########################################### SCHEMAS FOR ARCHIEVE EVENTS ###############################################

class PinnacleCancellationReason(BaseModel):
    code: Optional[str]
    details: Optional[Dict[str, "PinnaclePeriodResult"]] = None  # recursive details

class PinnaclePeriodResult(BaseModel):
    number: int
    status: int
    settlement_id: int
    settled_at: str
    team_1_score: int
    team_2_score: int
    cancellation_reason: Optional[PinnacleCancellationReason] = None

PinnacleCancellationReason.model_rebuild()  # rebuild for recursive type

class PinnacleArchiveEvent(BaseModel):
    event_id: int
    sport_id: int
    league_id: int
    league_name: str
    starts: str
    last: int
    home: str
    away: str
    event_type: str
    live_status_id: int
    parent_id: Optional[int]
    resulting_unit: str
    is_actual: bool
    home_team_type: str
    is_have_odds: bool
    is_have_periods: bool
    is_have_open_markets: bool
    period_results: Optional[List[PinnaclePeriodResult]] = None

class PinnacleArchiveEventsResponse(BaseModel):
    sport_id: Optional[int] = None
    sport_name: Optional[str] = None
    events: List[PinnacleArchiveEvent]
