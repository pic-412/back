from drf_spectacular.utils import OpenApiExample

ErrorBadRequestSchema = OpenApiExample(
    name="400(bad_request)",
    summary="[Default Bad Request]",
    value={
        "error": "잘못된 요청입니다."
    },
    status_codes=["400"],
    response_only=True,
)

ErrorBadRequestSchema1 = OpenApiExample(
    name="400(bad_request)",
    summary="[Default Bad Request1111]",
    value={
        "error": "잘못된 요청입니다."
    },
    status_codes=["400"],
    response_only=True,
)

# 여기에 에러 예시 다 적기

