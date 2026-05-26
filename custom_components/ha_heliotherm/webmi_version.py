"""Read the Heliotherm RCG firmware version via the WebMI endpoint.

Intended usage from the hub:

    from .webmi_version import detect_firmware_version

    async def detect_firmware_version(self) -> str | None:
        return await detect_firmware_version(self._hass, self._client.comm_params.host)

The implementation mirrors the WebMI browser flow:
1. /webMI/?info -> encryption parameters
2. /webMI/?createsession -> sessionid
3. /webMI/?createsubscription -> subscriptionid
4. /webMI/?read -> mcg/data/version
"""

from __future__ import annotations

import hashlib
import logging
import random
import string
from typing import Any

try:
    from homeassistant.core import HomeAssistant
except ImportError:
    HomeAssistant = None

try:
    from homeassistant.helpers.aiohttp_client import async_get_clientsession
except ImportError:
    import aiohttp
    def async_get_clientsession(hass):
        return aiohttp.ClientSession()

_LOGGER = logging.getLogger(__name__)

_WEBMI_PATH = "/webMI/"
_VERSION_ADDRESS = "mcg/data/version"
_SECRET_CHARS = string.ascii_letters + string.digits + "/"


class WebMIError(RuntimeError):
    """Raised when the WebMI version lookup fails."""


def _make_secret(length: int = 64) -> str:
    return "".join(random.choice(_SECRET_CHARS) for _ in range(length))


def _webmi_digest(session_id: str, secret: str, cnonce: int) -> str:
    raw = f"{session_id}:{secret}:{cnonce}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()


def _webmi_header(session_id: str, secret: str, cnonce: int) -> str:
    digest = _webmi_digest(session_id, secret, cnonce)
    return f'sessionid="{session_id}", cnonce="{cnonce}", digest="{digest}"'


def _rsa_encrypt_secret(secret: str, exponent_hex: str, modulus_hex: str) -> str:
    exponent = int(exponent_hex, 16)
    modulus = int(modulus_hex, 16)
    key_len_bytes = (modulus.bit_length() + 7) // 8

    message = secret.encode("utf-8")

    if key_len_bytes < len(message) + 11:
        raise WebMIError("Message is too long for RSA encryption")

    padding_len = key_len_bytes - len(message) - 3
    padding = bytes(random.randint(1, 255) for _ in range(padding_len))

    block = b"\x00\x02" + padding + b"\x00" + message

    cipher_int = pow(int.from_bytes(block, "big"), exponent, modulus)

    result = hex(cipher_int)[2:]
    if len(result) % 2:
        result = "0" + result

    # cipher = result.upper()
    # print("key_len_bytes", key_len_bytes)
    # print("cipher hex len", len(cipher))
    # print(cipher)

    return result.upper()

def _result_value(payload: dict[str, Any]) -> str | None:
    result = payload.get("result")

    if isinstance(result, list) and result:
        result = result[0]

    if isinstance(result, dict):
        value = result.get("value")
        return None if value is None else str(value)

    if isinstance(result, str):
        return result

    value = payload.get("value")
    return None if value is None else str(value)


async def _detect_firmware_version_with_session(session, base_url: str, timeout: int = 10) -> str | None:
    try:
        # 1) Read WebMI info / public key.
        async with session.post(f"{base_url}?info", timeout=timeout) as response:
            info = await response.json(content_type=None)

        exponent = info.get("encryptionexponent")
        modulus = info.get("encryptionmodulus")
        if not exponent or not modulus:
            raise WebMIError("WebMI info response does not contain RSA parameters")

        # 2) Create session.
        secret = _make_secret()
        cipher = _rsa_encrypt_secret(secret, exponent, modulus)

        async with session.post(
            f"{base_url}?createsession",
            data={"cipher": cipher},
            timeout=timeout,
        ) as response:
            create_session = await response.json(content_type=None)

        session_id = create_session.get("sessionid")
        if not session_id:
            raise WebMIError(f"WebMI createsession failed: {create_session!r}")

        # 3) Create main subscription. This matches the browser sequence.
        cnonce = 1
        async with session.post(
            f"{base_url}?createsubscription",
            headers={"X-WebMI": _webmi_header(session_id, secret, cnonce)},
            data={"Persistent": "true"},
            timeout=timeout,
        ) as response:
            create_subscription = await response.json(content_type=None)

        if "subscriptionid" not in create_subscription:
            raise WebMIError(f"WebMI createsubscription failed: {create_subscription!r}")

        # 4) Read firmware version.
        cnonce += 1
        async with session.post(
            f"{base_url}?read",
            headers={"X-WebMI": _webmi_header(session_id, secret, cnonce)},
            data={"address[]": _VERSION_ADDRESS},
            timeout=timeout,
        ) as response:
            version_response = await response.json(content_type=None)

        if version_response.get("error"):
            raise WebMIError(f"WebMI read failed: {version_response!r}")

        return _result_value(version_response)

    except Exception as err:  # noqa: BLE001 - caller should continue with configured fallback
        _LOGGER.warning("Could not detect Heliotherm firmware version via WebMI: %s", err)
        return None


async def detect_firmware_version(
    hass: HomeAssistant,
    host: str,
    port: int = 80,
    timeout: int = 10,
) -> str | None:
    """Return the RCG firmware version, e.g. '2.2.0.1', or None on failure."""
    base_url = f"http://{host}:{port}{_WEBMI_PATH}"
    if hass is None:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            return await _detect_firmware_version_with_session(session, base_url, timeout)
    else:
        session = async_get_clientsession(hass)
        return await _detect_firmware_version_with_session(session, base_url, timeout)
