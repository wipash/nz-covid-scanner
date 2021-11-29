import time
import base64
import re

import cwt
import requests

import exceptions

ENCODING = "utf-8"
DID_URL = "https://nzcp.identity.health.nz/.well-known/did.json"
VALID_ISSUERS = ["did:web:nzcp.identity.health.nz", "did:web:nzcp.identity.health.nz"]
PASS_TYPES = {"PublicCovidPass": ["givenName", "familyName", "dob"]}
SPEC_VERSION = 1
SPEC_VERSION_LONG = "1.0.0"

PROD_KEY = {
    "kty": "EC",
    "kid": "z12Kf7UQ",
    "crv": "P-256",
    "x": "DQCKJusqMsT0u7CjpmhjVGkHln3A3fS-ayeH4Nu52tc",
    "y": "lxgWzsLtVI8fqZmTPPo9nZ-kzGs7w7XO8-rUU68OxmI",
}
TEST_KEY = {
    "kty": "EC",
    "kid": "key-1",
    "crv": "P-256",
    "x": "zRR-XGsCp12Vvbgui4DD6O6cqmhfPuXMhi1OxPl8760",
    "y": "Iv5SU6FuW-TRYh5_GOrJlcV_gpF_GpFQhCOD8LSk3T0",
}


def get_did_from_url():
    try:
        r = requests.get(DID_URL)
        r.raise_for_status()
    except Exception:
        print("Got exception fetching DID")
    return r.json()


def get_verification_keys(did):
    verification_keys = []
    for verification_method in did["verificationMethod"]:
        if verification_method["type"] == "JsonWebKey2020":
            kid = verification_method["id"].split("#")[1]
            verification_method["publicKeyJwk"]["kid"] = kid
            verification_keys.append(
                cwt.COSEKey.from_jwk(verification_method["publicKeyJwk"])
            )
        else:
            raise exceptions.InvalidDidDocument("Verification method is the wrong type")

    # Add test key
    verification_keys.append(cwt.COSEKey.from_jwk(TEST_KEY))
    return verification_keys


def get_default_keys():
    verification_keys = []
    verification_keys.append(cwt.COSEKey.from_jwk(PROD_KEY))
    verification_keys.append(cwt.COSEKey.from_jwk(TEST_KEY))
    return verification_keys


def get_jti(cti):
    val = cti.hex()
    return "urn:uuid:" + "-".join(
        re.findall(r"^(.{8})(.{4})(.{4})(.{4})(.{12})$", val)[0]
    )


def validate_verifiable_claim(vc):
    context = vc.get("@context")
    type = vc.get("type")
    version = vc.get("version")
    subject = vc.get("credentialSubject")
    if context[0] != "https://www.w3.org/2018/credentials/v1":
        raise exceptions.InvalidVerifiableClaim("VC context is invalid")
    elif type[0] != "VerifiableCredential" or type[1] not in PASS_TYPES:
        raise exceptions.InvalidVerifiableClaim("VC type is invalid")
    elif version != SPEC_VERSION_LONG:
        raise exceptions.InvalidVerifiableClaim("VC version is invalid")

    for prop in PASS_TYPES[type[1]]:
        if prop not in subject:
            raise exceptions.InvalidVerifiableClaim(f"VC subject missing {prop}")

    return subject


def decode_qr(qr_bytes, verification_keys):
    raw_string = str(qr_bytes, ENCODING).strip()

    pattern = r"^NZCP:\/(\d+)\/(.+)$"
    match = re.search(pattern, raw_string)
    if match is None:
        raise exceptions.InvalidPayload("Invalid payload")

    version = match.group(1)
    encoded_payload = match.group(2)
    if int(version) != SPEC_VERSION:
        raise exceptions.InvalidPayload("Invalid version")

    unpadded_length = len(encoded_payload) % 8
    if unpadded_length != 0:
        encoded_payload += (8 - unpadded_length) * "="

    try:
        qrcode_payload = base64.b32decode(encoded_payload)
    except Exception as e:
        raise exceptions.InvalidPayload("Invalid base32 payload") from e

    qrcode_cwt = cwt.decode(qrcode_payload, keys=verification_keys, no_verify=True)

    readable = cwt.Claims.new(qrcode_cwt)
    jti = get_jti(readable.get(7))

    claim = {
        "iss": readable.iss,
        "nbf": readable.nbf,
        "exp": readable.exp,
        "jti": jti,
        "vc": readable.to_dict()["vc"],
    }

    if claim["nbf"] > int(time.time()):
        raise exceptions.PassNotActive("Pass not active yet")
    elif claim["exp"] < int(time.time()):
        raise exceptions.PassExpired("Pass expired")

    return claim


if __name__ == "__main__":
    from led import LED
    from scanner import Scanner

    try:
        did = get_did_from_url()
        keys = get_verification_keys(did)
    except:
        print("Couldn't get keys, using built-in defaults")
        keys = get_default_keys()

    scanner = Scanner().scanner
    led = LED()

    print("Ready")
    led.write_text("////")

    while True:
        s = scanner.readline()
        if s:
            try:
                covid_pass = decode_qr(s, keys)
                subject = validate_verifiable_claim(covid_pass["vc"])
                print("-----= Valid Pass =-----")
                print(f'Name: {subject["givenName"]} {subject["familyName"]}')
                print(f'DOB:  {subject["dob"]}')
                print("------------------------")
                led.write_text(" \3\3")
            except Exception as e:
                print(e)
                led.write_text("xxxx")
