import requests
import requests.exceptions


DEFAULT_TIMEOUT = 5


def make_service_request(
    method: str,
    url: str,
    *,
    params: dict = None,
    data: dict = None,
    json: dict = None,
    headers: dict = None,
    timeout: int = DEFAULT_TIMEOUT,
    raise_on_error: bool = True,
    fallback_result=None,
):
    headers = headers or {}

    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
        )
        response.raise_for_status()
        return response

    except (requests.exceptions.Timeout, ConnectionError) as e:
        print(f"[Service Request] Connection error to {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(
            f"[Service Request] Failed: {e} | Response: {getattr(e.response, 'text', 'No response')}"
        )

    if raise_on_error:
        raise Exception(f"Failed to request {url}")

    return fallback_result


def make_authenticated_service_request(
    request,
    method: str,
    url: str,
    *,
    params: dict = None,
    data: dict = None,
    json: dict = None,
    extra_headers: dict = None,
    timeout: int = DEFAULT_TIMEOUT,
    raise_on_error: bool = True,
    fallback_result=None,
):
    headers = {}

    access_token = request.COOKIES.get("access")
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    headers["X-Request-Source"] = "frontend-service"

    if extra_headers:
        headers.update(extra_headers)

    return make_service_request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        data=data,
        json=json,
        timeout=timeout,
        raise_on_error=raise_on_error,
        fallback_result=fallback_result,
    )
