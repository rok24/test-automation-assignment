import re
from typing import Literal
from pydantic import BaseModel, field_validator, ConfigDict, Field, model_validator


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class RequestModel(BaseModel):
    transaction_id: str = Field(..., min_length=1)  # Required,non-emptystring

POSTCODE_REGEX = r"[A-Za-z][A-Ha-hK-Yk-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2}"


class Postcode(BaseModel):
    postcode: str

    @field_validator("postcode", mode="after")
    def check_postcode(cls, v):
        v_striped = v.strip().upper()
        if not re.match(POSTCODE_REGEX, v_striped):
            raise ValueError("please provide a valid UK postcode as a string!")
        return v_striped


class QuoteRequest(RequestModel, Postcode):
    requested_data_rate_mbps: int
    requested_access_rate_mbps: int
    contract_length: int
    quote_id: str = Field(..., min_length=1)  # Required,non-emptystring

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaction_id": "728167dc-b6c7-49ef-af68-ac9c5aec70ec",
                    "quote_id": "quote_id_example",
                    "requested_data_rate_mbps": 100,
                    "requested_access_rate_mbps": 100,
                    "postcode": "SO43 7PB",
                    "contract_length": 12,
                }
            ]
        }
    }


class CircuitModel(BaseModel):
    exchange_type: str | None = None
    service_type: Literal["EAD LA", "EAD", "EAD ER"]
    serving_exchange_code: str = Field(description="1141 code")
    serving_exchange_mdf_id: str
    serving_exchange_name: str
    serving_exchange_postcode: str
    lead_time_days: int
    radial_distance_metres: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "serving_exchange_code": "SMBA",
                    "serving_exchange_mdf_id": "SMBA",
                    "serving_exchange_name": "some_exchange_name",
                    "serving_exchange_postcode": "W1A 1AA",
                    "lead_time_days": 30,
                    "radial_distance_metres": 1200,
                    "service_type": "EAD",
                    "exchange_type": "T1",
                },
                {
                    "serving_exchange_code": "SMBT",
                    "serving_exchange_mdf_id": "SMBT",
                    "serving_exchange_name": "some_exchange_name",
                    "serving_exchange_postcode": "W1A 1AA",
                    "lead_time_days": 45,
                    "radial_distance_metres": 600,
                    "service_type": "EAD",
                    "exchange_type": "T1.1",
                },
            ]
        }
    }

class QuoteResponse(BaseModel):
    # we want to limit this based on requested param "limit"
    postcode: str
    preferred_exchange: CircuitModel
    exchange_options: list[CircuitModel]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "postcode": "SO43 7PB",
                    "preferred_exchange": {
                        "serving_exchange_code": "STLYNST",
                        "serving_exchange_mdf_id": "STLYNST",
                        "serving_exchange_name": "some_exchange_name",
                        "serving_exchange_postcode": "W1A 1AA",
                        "lead_time_days": 45,
                        "radial_distance_metres": 600,
                        "service_type": "EAD",
                    },
                    "exchange_options": [
                        {
                            "serving_exchange_code": "STLYNST",
                            "serving_exchange_mdf_id": "STLYNST",
                            "serving_exchange_name": "some_exchange_name",
                            "serving_exchange_postcode": "W1A 1AA",
                            "lead_time_days": 45,
                            "radial_distance_metres": 600,
                            "service_type": "EAD",
                        },
                        {
                            "serving_exchange_code": "STCADNM",
                            "serving_exchange_mdf_id": "STCADNM",
                            "serving_exchange_name": "some_exchange_name",
                            "serving_exchange_postcode": "W1A 1AA",
                            "lead_time_days": 45,
                            "radial_distance_metres": 800,
                            "service_type": "EAD",
                        },
                        {
                            "serving_exchange_code": "STBROCK",
                            "serving_exchange_mdf_id": "STBROCK",
                            "serving_exchange_name": "some_exchange_name",
                            "serving_exchange_postcode": "W1A 1AA",
                            "lead_time_days": 45,
                            "radial_distance_metres": 900,
                            "service_type": "EAD",
                        },
                    ],
                }
            ]
        }
    }


class Partner(BaseModel):
    id: str  # need this in case names change
    name: str  # need this for human readability


class Service(BaseModel):
    serving_exchange_mdf_id: str
    serving_exchange_code: str = Field(description="1141 code")
    requested_data_rate_mbps: int
    requested_access_rate_mbps: int
    service_type: Literal["EAD LA", "EAD", "EAD ER"]
    exchange_type: str = None

    @model_validator(mode="after")
    def check_rates(self):
        if self.requested_data_rate_mbps > self.requested_access_rate_mbps:
            raise ValueError("Data rate cannot exceed access rate, please provide valid rates.")
        return self

class OrderRequest(RequestModel):
    order_type: Literal["NEW", "MODIFY", "CEASE"]
    linked_asset_id: str = Field(default=None, description="Linked asset reference for an RO2 order")
    interface_type: str  # might not need
    # might not need partner deets
    contract_term_months: int
    partner: Partner
    service: Service
    order_id: str
    asset_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "service": {
                        "serving_exchange_code": "SMBA",
                        "serving_exchange_mdf_id": "SMBA",
                        "requested_data_rate_mbps": 1000,
                        "requested_access_rate_mbps": 1000,
                        "service_type": "EAD",
                        "exchange_type": "T1.1",
                    },
                    "transaction_id": "728167dc-b6c7-49ef-af68-ac9c5aec70ec",
                    "order_type": "NEW",
                    "interface_type": "100BASE-TX/RJ45/TP",
                    "partner": {"id": "partner_id", "name": "Partner A"},
                    "order_id": "order_id_example",
                    "asset_id": "SKY-TPA1-002",
                    "linked_asset_id": "SKY-TPA1-001",
                    "contract_term_months": 12,
                }
            ]
        }
    }

class OrderResponse(BaseModel):
    lead_time_days: int
