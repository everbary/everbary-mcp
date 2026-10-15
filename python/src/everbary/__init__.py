"""Python client for the eVerbary Order API.

    from everbary import Client
    eb = Client("ev_test_...")          # test keys place pretend orders
    order = eb.create_order(
        email="paralegal@firm.com", first_name="Ana", last_name="Ruiz",
        language_from="spanish", language_to="english", pages=1,
        files=["birth-certificate.pdf"], reference="I-130 Gomez",
    )
    print(eb.get_order(order["orderNumber"]))

API reference: https://orders.everbary.com/v1/docs
"""

from .client import Client, EverbaryError, verify_webhook

__all__ = ["Client", "EverbaryError", "verify_webhook"]
__version__ = "1.0.0"
