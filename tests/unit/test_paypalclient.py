from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment
import pytest

from paypalv2 import paypalclient


def test_default_settings_are_set_as_expected():
    # GIVEN the settings

    # WHEN

    # THEN
    pytest.fail('not completed!')


def test_paypal_environment_set_to_live_sets_the_environment_to_live_environment(mocker):
    # GIVEN we are in a live environment
    mocker.patch.object(paypalclient, 'PAYPAL_ENVIRONMENT', 'live')

    # WHEN instantiating a paypal client
    pc = paypalclient.PayPalClient()

    # THEN the environment is live
    assert isinstance(pc.environment, LiveEnvironment)


def test_paypal_environment_not_set_to_live_sets_the_environment_to_sandbox_environment(mocker):
    # GIVEN we are in a test environment
    mocker.patch.object(paypalclient, 'PAYPAL_ENVIRONMENT', 'sandbox')

    # WHEN instantiating a paypal client
    pc = paypalclient.PayPalClient()

    # THEN the environment is test/sandbox
    assert isinstance(pc.environment, SandboxEnvironment)
