"""Constants for the FordPass integration."""

VIN = "vin"

MANUFACTURER = "Ford Motor Company"

VEHICLE = "Ford Vehicle"

REGION = "region"

REGION_OPTIONS = ["Netherlands", "UK&Europe", "Australia", "USA", "Canada"]
DEFAULT_REGION = "USA"

REGIONS = {
    "UK&Europe": {
        "region": "1E8C7794-FF5F-49BC-9596-A1E0C86C5B19",
        "locale": "EN-IE",
        "locale_short": "IE",
        "locale_url": "https://login.ford.ie",
    },
    "Australia": {
        "region": "5C80A6BB-CF0D-4A30-BDBF-FC804B5C1A98",
        "locale": "EN-AU",
        "locale_short": "AUS",
        "locale_url": "https://login.ford.com.au",
    },
    "USA": {
        "region": "71A3AD0A-CF46-4CCF-B473-FC7FE5BC4592",
        "locale": "en-US",
        "locale_short": "USA",
        "locale_url": "https://login.ford.com",
    },
    "Canada": {
        "region": "71A3AD0A-CF46-4CCF-B473-FC7FE5BC4592",
        "locale": "en-CA",
        "locale_short": "CAN",
        "locale_url": "https://login.ford.com",
    },
}
