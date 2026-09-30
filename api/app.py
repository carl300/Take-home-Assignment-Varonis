import json
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict, List, Optional
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

RESTAURANTS_TABLE = os.environ.get("RESTAURANTS_TABLE", "restaurants")
REQUEST_LOGS_TABLE = os.environ.get("REQUEST_LOGS_TABLE", "restaurant_request_logs")


def get_table(table_name: str):
    return boto3.resource("dynamodb").Table(table_name)


def parse_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None

    normalized = str(value).strip().lower()

    if normalized in {"true", "yes", "1"}:
        return True

    if normalized in {"false", "no", "0"}:
        return False

    raise ValueError(f"Invalid boolean value: {value}")


def parse_hhmm(value: str) -> int:
    hour, minute = value.split(":")
    return int(hour) * 60 + int(minute)


def is_open_now(open_hour: str, close_hour: str, now: Optional[datetime] = None) -> bool:
    current = now or datetime.now(ZoneInfo("America/New_York"))

    current_minutes = current.hour * 60 + current.minute
    open_minutes = parse_hhmm(open_hour)
    close_minutes = parse_hhmm(close_hour)

    if open_minutes == close_minutes:
        return True

    if open_minutes < close_minutes:
        return open_minutes <= current_minutes <= close_minutes

    return current_minutes >= open_minutes or current_minutes <= close_minutes


def build_filter_expression(params: Dict[str, str]) -> Optional[Any]:
    filters = []

    if params.get("style"):
        filters.append(Attr("style_lower").eq(params["style"].lower()))

    vegetarian = parse_bool(params.get("vegetarian"))
    if vegetarian is not None:
        filters.append(Attr("vegetarian").eq(vegetarian))

    delivery = parse_bool(params.get("delivery"))
    if delivery is not None:
        filters.append(Attr("delivery").eq(delivery))

    if not filters:
        return None

    expression = filters[0]

    for item in filters[1:]:
        expression = expression & item

    return expression


def scan_restaurants(params: Dict[str, str]) -> List[Dict[str, Any]]:
    filter_expression = build_filter_expression(params)

    scan_kwargs: Dict[str, Any] = {}

    if filter_expression is not None:
        scan_kwargs["FilterExpression"] = filter_expression

    items: List[Dict[str, Any]] = []

    while True:
        response = get_table(RESTAURANTS_TABLE).scan(**scan_kwargs)

        items.extend(response.get("Items", []))

        last_key = response.get("LastEvaluatedKey")

        if not last_key:
            break

        scan_kwargs["ExclusiveStartKey"] = last_key

    return items


def select_recommendation(
    restaurants: List[Dict[str, Any]],
    now: Optional[datetime] = None
) -> Optional[Dict[str, Any]]:

    open_restaurants = [
        item
        for item in restaurants
        if is_open_now(item["openHour"], item["closeHour"], now)
    ]

    if not open_restaurants:
        return None

    return sorted(
        open_restaurants,
        key=lambda item: item.get("name", "")
    )[0]


def public_restaurant_view(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "style": item.get("style"),
        "address": item.get("address"),
        "openHour": item.get("openHour"),
        "closeHour": item.get("closeHour"),
        "vegetarian": item.get("vegetarian"),
        "delivery": item.get("delivery"),
    }


def response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Cache-Control": "no-store",
        },
        "body": json.dumps(body),
    }


def log_request(
    request_id: str,
    params: Dict[str, Any],
    status_code: int,
    recommendation: Optional[Dict[str, Any]]
) -> None:

    try:
        get_table(REQUEST_LOGS_TABLE).put_item(
            Item={
                "requestId": request_id,
                "requestTime": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "queryParameters": params,
                "statusCode": status_code,
                "recommendedRestaurantId": recommendation.get("id") if recommendation else None,
            }
        )

    except (ClientError, BotoCoreError) as exc:
        logger.error(
            "failed_to_write_request_log",
            extra={
                "request_id": request_id,
                "error": str(exc)
            }
        )


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    request_id = getattr(context, "aws_request_id", str(uuid4()))

    params = event.get("queryStringParameters") or {}

    try:
        restaurants = scan_restaurants(params)

        recommendation = select_recommendation(restaurants)

        if not recommendation:
            result = response(
                404,
                {
                    "message": "No open restaurant matched the requested criteria"
                }
            )

            log_request(request_id, params, 404, None)

            return result

        public_item = public_restaurant_view(recommendation)

        result = response(
            200,
            {
                "restaurantRecommendation": public_item
            }
        )

        log_request(request_id, params, 200, public_item)

        return result

    except ValueError as exc:
        result = response(
            400,
            {
                "message": str(exc)
            }
        )

        log_request(request_id, params, 400, None)

        return result

    except Exception:
        logger.exception(
            "unhandled_error",
            extra={
                "request_id": request_id
            }
        )

        result = response(
            500,
            {
                "message": "Internal server error"
            }
        )

        log_request(request_id, params, 500, None)

        return result