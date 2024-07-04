#!/usr/bin/env python3
import logging
import logging.handlers
import os

from dotenv import load_dotenv


def config_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s[%(process)d] - [%(name)s:%(lineno)d] :: (%(funcName)s) %(levelname)s - %(message)s",
        handlers=[logging.handlers.SysLogHandler(address="/dev/log", facility="user")],
    )
    return logging.getLogger(__name__)


def main():
    try:
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()
            fp_username = os.environ.get("FORDPASS_USERNAME")
            fp_region = os.environ.get("FORDPASS_REGION")
            if (fp_username or fp_region) is None:
                _LOGGER.warning(
                    f"if either fp_username:[{fp_username}] or fp_region:[{fp_region}] is None, stop"
                )
                return 1
            return 0
        else:
            _LOGGER.warning("unable to load .env")
            print("unable to load .env")
            return 1

    except Exception as e:
        _LOGGER.error(f"Error condition: {e}")
        return 1  # Indicate error


if __name__ == "__main__":
    _LOGGER = config_logging()
    exit_code = main()
    if exit_code == 0:
        _LOGGER.info("Completed successfully.")
        print("Completed Successfully.")
    else:
        _LOGGER.warning("Failed to complete.")
        print("Failed to complete.")
