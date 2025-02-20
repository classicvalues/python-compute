# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import mock

import grpc
from grpc.experimental import aio
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.compute_v1.services.backend_services import BackendServicesClient
from google.cloud.compute_v1.services.backend_services import pagers
from google.cloud.compute_v1.services.backend_services import transports
from google.cloud.compute_v1.types import compute
from google.oauth2 import service_account
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert BackendServicesClient._get_default_mtls_endpoint(None) is None
    assert (
        BackendServicesClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BackendServicesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BackendServicesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BackendServicesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BackendServicesClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize("client_class", [BackendServicesClient,])
def test_backend_services_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [(transports.BackendServicesRestTransport, "rest"),],
)
def test_backend_services_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class", [BackendServicesClient,])
def test_backend_services_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


def test_backend_services_client_get_transport_class():
    transport = BackendServicesClient.get_transport_class()
    available_transports = [
        transports.BackendServicesRestTransport,
    ]
    assert transport in available_transports

    transport = BackendServicesClient.get_transport_class("rest")
    assert transport == transports.BackendServicesRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(BackendServicesClient, transports.BackendServicesRestTransport, "rest"),],
)
@mock.patch.object(
    BackendServicesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BackendServicesClient),
)
def test_backend_services_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BackendServicesClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BackendServicesClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            BackendServicesClient,
            transports.BackendServicesRestTransport,
            "rest",
            "true",
        ),
        (
            BackendServicesClient,
            transports.BackendServicesRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    BackendServicesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BackendServicesClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_backend_services_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize("client_class", [BackendServicesClient])
@mock.patch.object(
    BackendServicesClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BackendServicesClient),
)
def test_backend_services_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(BackendServicesClient, transports.BackendServicesRestTransport, "rest"),],
)
def test_backend_services_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(BackendServicesClient, transports.BackendServicesRestTransport, "rest"),],
)
def test_backend_services_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "request_type", [compute.AddSignedUrlKeyBackendServiceRequest, dict,]
)
def test_add_signed_url_key_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["signed_url_key_resource"] = {
        "key_name": "key_name_value",
        "key_value": "key_value_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_signed_url_key_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_add_signed_url_key_unary_rest_required_fields(
    request_type=compute.AddSignedUrlKeyBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).add_signed_url_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).add_signed_url_key._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.add_signed_url_key_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_add_signed_url_key_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.add_signed_url_key._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(("backendService", "project", "signedUrlKeyResource",))
    )


def test_add_signed_url_key_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.AddSignedUrlKeyBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["signed_url_key_resource"] = {
        "key_name": "key_name_value",
        "key_value": "key_value_value",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_signed_url_key_unary(request)


def test_add_signed_url_key_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service="backend_service_value",
            signed_url_key_resource=compute.SignedUrlKey(key_name="key_name_value"),
        )
        mock_args.update(sample_request)
        client.add_signed_url_key_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}/addSignedUrlKey"
            % client.transport._host,
            args[1],
        )


def test_add_signed_url_key_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_signed_url_key_unary(
            compute.AddSignedUrlKeyBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
            signed_url_key_resource=compute.SignedUrlKey(key_name="key_name_value"),
        )


def test_add_signed_url_key_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.AggregatedListBackendServicesRequest, dict,]
)
def test_aggregated_list_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendServiceAggregatedList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendServiceAggregatedList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.aggregated_list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AggregatedListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]


def test_aggregated_list_rest_required_fields(
    request_type=compute.AggregatedListBackendServicesRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).aggregated_list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).aggregated_list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "max_results",
            "include_all_scopes",
            "filter",
            "order_by",
            "page_token",
            "return_partial_success",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.BackendServiceAggregatedList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.BackendServiceAggregatedList.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.aggregated_list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_aggregated_list_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.aggregated_list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "maxResults",
                "includeAllScopes",
                "filter",
                "orderBy",
                "pageToken",
                "returnPartialSuccess",
            )
        )
        & set(("project",))
    )


def test_aggregated_list_rest_bad_request(
    transport: str = "rest", request_type=compute.AggregatedListBackendServicesRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.aggregated_list(request)


def test_aggregated_list_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendServiceAggregatedList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendServiceAggregatedList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value",)
        mock_args.update(sample_request)
        client.aggregated_list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/aggregated/backendServices"
            % client.transport._host,
            args[1],
        )


def test_aggregated_list_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListBackendServicesRequest(), project="project_value",
        )


def test_aggregated_list_rest_pager(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.BackendServiceAggregatedList(
                items={
                    "a": compute.BackendServicesScopedList(),
                    "b": compute.BackendServicesScopedList(),
                    "c": compute.BackendServicesScopedList(),
                },
                next_page_token="abc",
            ),
            compute.BackendServiceAggregatedList(items={}, next_page_token="def",),
            compute.BackendServiceAggregatedList(
                items={"g": compute.BackendServicesScopedList(),},
                next_page_token="ghi",
            ),
            compute.BackendServiceAggregatedList(
                items={
                    "h": compute.BackendServicesScopedList(),
                    "i": compute.BackendServicesScopedList(),
                },
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.BackendServiceAggregatedList.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.aggregated_list(request=sample_request)

        assert isinstance(pager.get("a"), compute.BackendServicesScopedList)
        assert pager.get("h") is None

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tuple) for i in results)
        for result in results:
            assert isinstance(result, tuple)
            assert tuple(type(t) for t in result) == (
                str,
                compute.BackendServicesScopedList,
            )

        assert pager.get("a") is None
        assert isinstance(pager.get("h"), compute.BackendServicesScopedList)

        pages = list(client.aggregated_list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [compute.DeleteBackendServiceRequest, dict,])
def test_delete_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_unary_rest_required_fields(
    request_type=compute.DeleteBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",)) & set(("backendService", "project",))
    )


def test_delete_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_unary(request)


def test_delete_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", backend_service="backend_service_value",
        )
        mock_args.update(sample_request)
        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
        )


def test_delete_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.DeleteSignedUrlKeyBackendServiceRequest, dict,]
)
def test_delete_signed_url_key_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_signed_url_key_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_signed_url_key_unary_rest_required_fields(
    request_type=compute.DeleteSignedUrlKeyBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["key_name"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped
    assert "keyName" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_signed_url_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "keyName" in jsonified_request
    assert jsonified_request["keyName"] == request_init["key_name"]

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["keyName"] = "key_name_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_signed_url_key._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id", "key_name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "keyName" in jsonified_request
    assert jsonified_request["keyName"] == "key_name_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_signed_url_key_unary(request)

            expected_params = [
                ("keyName", "",),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_signed_url_key_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_signed_url_key._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId", "keyName",)) & set(("backendService", "keyName", "project",))
    )


def test_delete_signed_url_key_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeleteSignedUrlKeyBackendServiceRequest,
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_signed_url_key_unary(request)


def test_delete_signed_url_key_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service="backend_service_value",
            key_name="key_name_value",
        )
        mock_args.update(sample_request)
        client.delete_signed_url_key_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}/deleteSignedUrlKey"
            % client.transport._host,
            args[1],
        )


def test_delete_signed_url_key_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_signed_url_key_unary(
            compute.DeleteSignedUrlKeyBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
            key_name="key_name_value",
        )


def test_delete_signed_url_key_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize("request_type", [compute.GetBackendServiceRequest, dict,])
def test_get_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendService(
            affinity_cookie_ttl_sec=2432,
            creation_timestamp="creation_timestamp_value",
            custom_request_headers=["custom_request_headers_value"],
            custom_response_headers=["custom_response_headers_value"],
            description="description_value",
            enable_c_d_n=True,
            fingerprint="fingerprint_value",
            health_checks=["health_checks_value"],
            id=205,
            kind="kind_value",
            load_balancing_scheme="load_balancing_scheme_value",
            locality_lb_policy="locality_lb_policy_value",
            name="name_value",
            network="network_value",
            port=453,
            port_name="port_name_value",
            protocol="protocol_value",
            region="region_value",
            security_policy="security_policy_value",
            self_link="self_link_value",
            session_affinity="session_affinity_value",
            timeout_sec=1185,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendService.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.BackendService)
    assert response.affinity_cookie_ttl_sec == 2432
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.custom_request_headers == ["custom_request_headers_value"]
    assert response.custom_response_headers == ["custom_response_headers_value"]
    assert response.description == "description_value"
    assert response.enable_c_d_n is True
    assert response.fingerprint == "fingerprint_value"
    assert response.health_checks == ["health_checks_value"]
    assert response.id == 205
    assert response.kind == "kind_value"
    assert response.load_balancing_scheme == "load_balancing_scheme_value"
    assert response.locality_lb_policy == "locality_lb_policy_value"
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.port == 453
    assert response.port_name == "port_name_value"
    assert response.protocol == "protocol_value"
    assert response.region == "region_value"
    assert response.security_policy == "security_policy_value"
    assert response.self_link == "self_link_value"
    assert response.session_affinity == "session_affinity_value"
    assert response.timeout_sec == 1185


def test_get_rest_required_fields(request_type=compute.GetBackendServiceRequest):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.BackendService()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.BackendService.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("backendService", "project",)))


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get(request)


def test_get_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendService()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendService.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", backend_service="backend_service_value",
        )
        mock_args.update(sample_request)
        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
        )


def test_get_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.GetHealthBackendServiceRequest, dict,]
)
def test_get_health_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["resource_group_reference_resource"] = {"group": "group_value"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendServiceGroupHealth(kind="kind_value",)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendServiceGroupHealth.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_health(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.BackendServiceGroupHealth)
    assert response.kind == "kind_value"


def test_get_health_rest_required_fields(
    request_type=compute.GetHealthBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_health._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_health._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.BackendServiceGroupHealth()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.BackendServiceGroupHealth.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_health(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_health_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_health._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(()) & set(("backendService", "project", "resourceGroupReferenceResource",))
    )


def test_get_health_rest_bad_request(
    transport: str = "rest", request_type=compute.GetHealthBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["resource_group_reference_resource"] = {"group": "group_value"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_health(request)


def test_get_health_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendServiceGroupHealth()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendServiceGroupHealth.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service="backend_service_value",
            resource_group_reference_resource=compute.ResourceGroupReference(
                group="group_value"
            ),
        )
        mock_args.update(sample_request)
        client.get_health(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}/getHealth"
            % client.transport._host,
            args[1],
        )


def test_get_health_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_health(
            compute.GetHealthBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
            resource_group_reference_resource=compute.ResourceGroupReference(
                group="group_value"
            ),
        )


def test_get_health_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize("request_type", [compute.InsertBackendServiceRequest, dict,])
def test_insert_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request_init["backend_service_resource"] = {
        "affinity_cookie_ttl_sec": 2432,
        "backends": [
            {
                "balancing_mode": "balancing_mode_value",
                "capacity_scaler": 0.1575,
                "description": "description_value",
                "failover": True,
                "group": "group_value",
                "max_connections": 1608,
                "max_connections_per_endpoint": 2990,
                "max_connections_per_instance": 2978,
                "max_rate": 849,
                "max_rate_per_endpoint": 0.22310000000000002,
                "max_rate_per_instance": 0.22190000000000001,
                "max_utilization": 0.1633,
            }
        ],
        "cdn_policy": {
            "bypass_cache_on_request_headers": [{"header_name": "header_name_value"}],
            "cache_key_policy": {
                "include_host": True,
                "include_protocol": True,
                "include_query_string": True,
                "query_string_blacklist": [
                    "query_string_blacklist_value_1",
                    "query_string_blacklist_value_2",
                ],
                "query_string_whitelist": [
                    "query_string_whitelist_value_1",
                    "query_string_whitelist_value_2",
                ],
            },
            "cache_mode": "cache_mode_value",
            "client_ttl": 1074,
            "default_ttl": 1176,
            "max_ttl": 761,
            "negative_caching": True,
            "negative_caching_policy": [{"code": 411, "ttl": 340}],
            "request_coalescing": True,
            "serve_while_stale": 1813,
            "signed_url_cache_max_age_sec": 2890,
            "signed_url_key_names": [
                "signed_url_key_names_value_1",
                "signed_url_key_names_value_2",
            ],
        },
        "circuit_breakers": {
            "max_connections": 1608,
            "max_pending_requests": 2149,
            "max_requests": 1313,
            "max_requests_per_connection": 2902,
            "max_retries": 1187,
        },
        "connection_draining": {"draining_timeout_sec": 2124},
        "consistent_hash": {
            "http_cookie": {
                "name": "name_value",
                "path": "path_value",
                "ttl": {"nanos": 543, "seconds": 751},
            },
            "http_header_name": "http_header_name_value",
            "minimum_ring_size": 1829,
        },
        "creation_timestamp": "creation_timestamp_value",
        "custom_request_headers": [
            "custom_request_headers_value_1",
            "custom_request_headers_value_2",
        ],
        "custom_response_headers": [
            "custom_response_headers_value_1",
            "custom_response_headers_value_2",
        ],
        "description": "description_value",
        "enable_c_d_n": True,
        "failover_policy": {
            "disable_connection_drain_on_failover": True,
            "drop_traffic_if_unhealthy": True,
            "failover_ratio": 0.1494,
        },
        "fingerprint": "fingerprint_value",
        "health_checks": ["health_checks_value_1", "health_checks_value_2"],
        "iap": {
            "enabled": True,
            "oauth2_client_id": "oauth2_client_id_value",
            "oauth2_client_secret": "oauth2_client_secret_value",
            "oauth2_client_secret_sha256": "oauth2_client_secret_sha256_value",
        },
        "id": 205,
        "kind": "kind_value",
        "load_balancing_scheme": "load_balancing_scheme_value",
        "locality_lb_policy": "locality_lb_policy_value",
        "log_config": {"enable": True, "sample_rate": 0.1165},
        "max_stream_duration": {"nanos": 543, "seconds": 751},
        "name": "name_value",
        "network": "network_value",
        "outlier_detection": {
            "base_ejection_time": {"nanos": 543, "seconds": 751},
            "consecutive_errors": 1956,
            "consecutive_gateway_failure": 2880,
            "enforcing_consecutive_errors": 3006,
            "enforcing_consecutive_gateway_failure": 3930,
            "enforcing_success_rate": 2334,
            "interval": {"nanos": 543, "seconds": 751},
            "max_ejection_percent": 2118,
            "success_rate_minimum_hosts": 2799,
            "success_rate_request_volume": 2915,
            "success_rate_stdev_factor": 2663,
        },
        "port": 453,
        "port_name": "port_name_value",
        "protocol": "protocol_value",
        "region": "region_value",
        "security_policy": "security_policy_value",
        "security_settings": {
            "client_tls_policy": "client_tls_policy_value",
            "subject_alt_names": [
                "subject_alt_names_value_1",
                "subject_alt_names_value_2",
            ],
        },
        "self_link": "self_link_value",
        "session_affinity": "session_affinity_value",
        "subsetting": {"policy": "policy_value"},
        "timeout_sec": 1185,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_insert_unary_rest_required_fields(
    request_type=compute.InsertBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.insert_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_insert_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",)) & set(("backendServiceResource", "project",))
    )


def test_insert_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request_init["backend_service_resource"] = {
        "affinity_cookie_ttl_sec": 2432,
        "backends": [
            {
                "balancing_mode": "balancing_mode_value",
                "capacity_scaler": 0.1575,
                "description": "description_value",
                "failover": True,
                "group": "group_value",
                "max_connections": 1608,
                "max_connections_per_endpoint": 2990,
                "max_connections_per_instance": 2978,
                "max_rate": 849,
                "max_rate_per_endpoint": 0.22310000000000002,
                "max_rate_per_instance": 0.22190000000000001,
                "max_utilization": 0.1633,
            }
        ],
        "cdn_policy": {
            "bypass_cache_on_request_headers": [{"header_name": "header_name_value"}],
            "cache_key_policy": {
                "include_host": True,
                "include_protocol": True,
                "include_query_string": True,
                "query_string_blacklist": [
                    "query_string_blacklist_value_1",
                    "query_string_blacklist_value_2",
                ],
                "query_string_whitelist": [
                    "query_string_whitelist_value_1",
                    "query_string_whitelist_value_2",
                ],
            },
            "cache_mode": "cache_mode_value",
            "client_ttl": 1074,
            "default_ttl": 1176,
            "max_ttl": 761,
            "negative_caching": True,
            "negative_caching_policy": [{"code": 411, "ttl": 340}],
            "request_coalescing": True,
            "serve_while_stale": 1813,
            "signed_url_cache_max_age_sec": 2890,
            "signed_url_key_names": [
                "signed_url_key_names_value_1",
                "signed_url_key_names_value_2",
            ],
        },
        "circuit_breakers": {
            "max_connections": 1608,
            "max_pending_requests": 2149,
            "max_requests": 1313,
            "max_requests_per_connection": 2902,
            "max_retries": 1187,
        },
        "connection_draining": {"draining_timeout_sec": 2124},
        "consistent_hash": {
            "http_cookie": {
                "name": "name_value",
                "path": "path_value",
                "ttl": {"nanos": 543, "seconds": 751},
            },
            "http_header_name": "http_header_name_value",
            "minimum_ring_size": 1829,
        },
        "creation_timestamp": "creation_timestamp_value",
        "custom_request_headers": [
            "custom_request_headers_value_1",
            "custom_request_headers_value_2",
        ],
        "custom_response_headers": [
            "custom_response_headers_value_1",
            "custom_response_headers_value_2",
        ],
        "description": "description_value",
        "enable_c_d_n": True,
        "failover_policy": {
            "disable_connection_drain_on_failover": True,
            "drop_traffic_if_unhealthy": True,
            "failover_ratio": 0.1494,
        },
        "fingerprint": "fingerprint_value",
        "health_checks": ["health_checks_value_1", "health_checks_value_2"],
        "iap": {
            "enabled": True,
            "oauth2_client_id": "oauth2_client_id_value",
            "oauth2_client_secret": "oauth2_client_secret_value",
            "oauth2_client_secret_sha256": "oauth2_client_secret_sha256_value",
        },
        "id": 205,
        "kind": "kind_value",
        "load_balancing_scheme": "load_balancing_scheme_value",
        "locality_lb_policy": "locality_lb_policy_value",
        "log_config": {"enable": True, "sample_rate": 0.1165},
        "max_stream_duration": {"nanos": 543, "seconds": 751},
        "name": "name_value",
        "network": "network_value",
        "outlier_detection": {
            "base_ejection_time": {"nanos": 543, "seconds": 751},
            "consecutive_errors": 1956,
            "consecutive_gateway_failure": 2880,
            "enforcing_consecutive_errors": 3006,
            "enforcing_consecutive_gateway_failure": 3930,
            "enforcing_success_rate": 2334,
            "interval": {"nanos": 543, "seconds": 751},
            "max_ejection_percent": 2118,
            "success_rate_minimum_hosts": 2799,
            "success_rate_request_volume": 2915,
            "success_rate_stdev_factor": 2663,
        },
        "port": 453,
        "port_name": "port_name_value",
        "protocol": "protocol_value",
        "region": "region_value",
        "security_policy": "security_policy_value",
        "security_settings": {
            "client_tls_policy": "client_tls_policy_value",
            "subject_alt_names": [
                "subject_alt_names_value_1",
                "subject_alt_names_value_2",
            ],
        },
        "self_link": "self_link_value",
        "session_affinity": "session_affinity_value",
        "subsetting": {"policy": "policy_value"},
        "timeout_sec": 1185,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert_unary(request)


def test_insert_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service_resource=compute.BackendService(
                affinity_cookie_ttl_sec=2432
            ),
        )
        mock_args.update(sample_request)
        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices"
            % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
            compute.InsertBackendServiceRequest(),
            project="project_value",
            backend_service_resource=compute.BackendService(
                affinity_cookie_ttl_sec=2432
            ),
        )


def test_insert_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize("request_type", [compute.ListBackendServicesRequest, dict,])
def test_list_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendServiceList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendServiceList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


def test_list_rest_required_fields(request_type=compute.ListBackendServicesRequest):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        ("max_results", "filter", "order_by", "page_token", "return_partial_success",)
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.BackendServiceList()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": request_init,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.BackendServiceList.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("maxResults", "filter", "orderBy", "pageToken", "returnPartialSuccess",))
        & set(("project",))
    )


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListBackendServicesRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list(request)


def test_list_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.BackendServiceList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.BackendServiceList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value",)
        mock_args.update(sample_request)
        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices"
            % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListBackendServicesRequest(), project="project_value",
        )


def test_list_rest_pager(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.BackendServiceList(
                items=[
                    compute.BackendService(),
                    compute.BackendService(),
                    compute.BackendService(),
                ],
                next_page_token="abc",
            ),
            compute.BackendServiceList(items=[], next_page_token="def",),
            compute.BackendServiceList(
                items=[compute.BackendService(),], next_page_token="ghi",
            ),
            compute.BackendServiceList(
                items=[compute.BackendService(), compute.BackendService(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.BackendServiceList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.BackendService) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [compute.PatchBackendServiceRequest, dict,])
def test_patch_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["backend_service_resource"] = {
        "affinity_cookie_ttl_sec": 2432,
        "backends": [
            {
                "balancing_mode": "balancing_mode_value",
                "capacity_scaler": 0.1575,
                "description": "description_value",
                "failover": True,
                "group": "group_value",
                "max_connections": 1608,
                "max_connections_per_endpoint": 2990,
                "max_connections_per_instance": 2978,
                "max_rate": 849,
                "max_rate_per_endpoint": 0.22310000000000002,
                "max_rate_per_instance": 0.22190000000000001,
                "max_utilization": 0.1633,
            }
        ],
        "cdn_policy": {
            "bypass_cache_on_request_headers": [{"header_name": "header_name_value"}],
            "cache_key_policy": {
                "include_host": True,
                "include_protocol": True,
                "include_query_string": True,
                "query_string_blacklist": [
                    "query_string_blacklist_value_1",
                    "query_string_blacklist_value_2",
                ],
                "query_string_whitelist": [
                    "query_string_whitelist_value_1",
                    "query_string_whitelist_value_2",
                ],
            },
            "cache_mode": "cache_mode_value",
            "client_ttl": 1074,
            "default_ttl": 1176,
            "max_ttl": 761,
            "negative_caching": True,
            "negative_caching_policy": [{"code": 411, "ttl": 340}],
            "request_coalescing": True,
            "serve_while_stale": 1813,
            "signed_url_cache_max_age_sec": 2890,
            "signed_url_key_names": [
                "signed_url_key_names_value_1",
                "signed_url_key_names_value_2",
            ],
        },
        "circuit_breakers": {
            "max_connections": 1608,
            "max_pending_requests": 2149,
            "max_requests": 1313,
            "max_requests_per_connection": 2902,
            "max_retries": 1187,
        },
        "connection_draining": {"draining_timeout_sec": 2124},
        "consistent_hash": {
            "http_cookie": {
                "name": "name_value",
                "path": "path_value",
                "ttl": {"nanos": 543, "seconds": 751},
            },
            "http_header_name": "http_header_name_value",
            "minimum_ring_size": 1829,
        },
        "creation_timestamp": "creation_timestamp_value",
        "custom_request_headers": [
            "custom_request_headers_value_1",
            "custom_request_headers_value_2",
        ],
        "custom_response_headers": [
            "custom_response_headers_value_1",
            "custom_response_headers_value_2",
        ],
        "description": "description_value",
        "enable_c_d_n": True,
        "failover_policy": {
            "disable_connection_drain_on_failover": True,
            "drop_traffic_if_unhealthy": True,
            "failover_ratio": 0.1494,
        },
        "fingerprint": "fingerprint_value",
        "health_checks": ["health_checks_value_1", "health_checks_value_2"],
        "iap": {
            "enabled": True,
            "oauth2_client_id": "oauth2_client_id_value",
            "oauth2_client_secret": "oauth2_client_secret_value",
            "oauth2_client_secret_sha256": "oauth2_client_secret_sha256_value",
        },
        "id": 205,
        "kind": "kind_value",
        "load_balancing_scheme": "load_balancing_scheme_value",
        "locality_lb_policy": "locality_lb_policy_value",
        "log_config": {"enable": True, "sample_rate": 0.1165},
        "max_stream_duration": {"nanos": 543, "seconds": 751},
        "name": "name_value",
        "network": "network_value",
        "outlier_detection": {
            "base_ejection_time": {"nanos": 543, "seconds": 751},
            "consecutive_errors": 1956,
            "consecutive_gateway_failure": 2880,
            "enforcing_consecutive_errors": 3006,
            "enforcing_consecutive_gateway_failure": 3930,
            "enforcing_success_rate": 2334,
            "interval": {"nanos": 543, "seconds": 751},
            "max_ejection_percent": 2118,
            "success_rate_minimum_hosts": 2799,
            "success_rate_request_volume": 2915,
            "success_rate_stdev_factor": 2663,
        },
        "port": 453,
        "port_name": "port_name_value",
        "protocol": "protocol_value",
        "region": "region_value",
        "security_policy": "security_policy_value",
        "security_settings": {
            "client_tls_policy": "client_tls_policy_value",
            "subject_alt_names": [
                "subject_alt_names_value_1",
                "subject_alt_names_value_2",
            ],
        },
        "self_link": "self_link_value",
        "session_affinity": "session_affinity_value",
        "subsetting": {"policy": "policy_value"},
        "timeout_sec": 1185,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_patch_unary_rest_required_fields(
    request_type=compute.PatchBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.patch_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(("backendService", "backendServiceResource", "project",))
    )


def test_patch_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["backend_service_resource"] = {
        "affinity_cookie_ttl_sec": 2432,
        "backends": [
            {
                "balancing_mode": "balancing_mode_value",
                "capacity_scaler": 0.1575,
                "description": "description_value",
                "failover": True,
                "group": "group_value",
                "max_connections": 1608,
                "max_connections_per_endpoint": 2990,
                "max_connections_per_instance": 2978,
                "max_rate": 849,
                "max_rate_per_endpoint": 0.22310000000000002,
                "max_rate_per_instance": 0.22190000000000001,
                "max_utilization": 0.1633,
            }
        ],
        "cdn_policy": {
            "bypass_cache_on_request_headers": [{"header_name": "header_name_value"}],
            "cache_key_policy": {
                "include_host": True,
                "include_protocol": True,
                "include_query_string": True,
                "query_string_blacklist": [
                    "query_string_blacklist_value_1",
                    "query_string_blacklist_value_2",
                ],
                "query_string_whitelist": [
                    "query_string_whitelist_value_1",
                    "query_string_whitelist_value_2",
                ],
            },
            "cache_mode": "cache_mode_value",
            "client_ttl": 1074,
            "default_ttl": 1176,
            "max_ttl": 761,
            "negative_caching": True,
            "negative_caching_policy": [{"code": 411, "ttl": 340}],
            "request_coalescing": True,
            "serve_while_stale": 1813,
            "signed_url_cache_max_age_sec": 2890,
            "signed_url_key_names": [
                "signed_url_key_names_value_1",
                "signed_url_key_names_value_2",
            ],
        },
        "circuit_breakers": {
            "max_connections": 1608,
            "max_pending_requests": 2149,
            "max_requests": 1313,
            "max_requests_per_connection": 2902,
            "max_retries": 1187,
        },
        "connection_draining": {"draining_timeout_sec": 2124},
        "consistent_hash": {
            "http_cookie": {
                "name": "name_value",
                "path": "path_value",
                "ttl": {"nanos": 543, "seconds": 751},
            },
            "http_header_name": "http_header_name_value",
            "minimum_ring_size": 1829,
        },
        "creation_timestamp": "creation_timestamp_value",
        "custom_request_headers": [
            "custom_request_headers_value_1",
            "custom_request_headers_value_2",
        ],
        "custom_response_headers": [
            "custom_response_headers_value_1",
            "custom_response_headers_value_2",
        ],
        "description": "description_value",
        "enable_c_d_n": True,
        "failover_policy": {
            "disable_connection_drain_on_failover": True,
            "drop_traffic_if_unhealthy": True,
            "failover_ratio": 0.1494,
        },
        "fingerprint": "fingerprint_value",
        "health_checks": ["health_checks_value_1", "health_checks_value_2"],
        "iap": {
            "enabled": True,
            "oauth2_client_id": "oauth2_client_id_value",
            "oauth2_client_secret": "oauth2_client_secret_value",
            "oauth2_client_secret_sha256": "oauth2_client_secret_sha256_value",
        },
        "id": 205,
        "kind": "kind_value",
        "load_balancing_scheme": "load_balancing_scheme_value",
        "locality_lb_policy": "locality_lb_policy_value",
        "log_config": {"enable": True, "sample_rate": 0.1165},
        "max_stream_duration": {"nanos": 543, "seconds": 751},
        "name": "name_value",
        "network": "network_value",
        "outlier_detection": {
            "base_ejection_time": {"nanos": 543, "seconds": 751},
            "consecutive_errors": 1956,
            "consecutive_gateway_failure": 2880,
            "enforcing_consecutive_errors": 3006,
            "enforcing_consecutive_gateway_failure": 3930,
            "enforcing_success_rate": 2334,
            "interval": {"nanos": 543, "seconds": 751},
            "max_ejection_percent": 2118,
            "success_rate_minimum_hosts": 2799,
            "success_rate_request_volume": 2915,
            "success_rate_stdev_factor": 2663,
        },
        "port": 453,
        "port_name": "port_name_value",
        "protocol": "protocol_value",
        "region": "region_value",
        "security_policy": "security_policy_value",
        "security_settings": {
            "client_tls_policy": "client_tls_policy_value",
            "subject_alt_names": [
                "subject_alt_names_value_1",
                "subject_alt_names_value_2",
            ],
        },
        "self_link": "self_link_value",
        "session_affinity": "session_affinity_value",
        "subsetting": {"policy": "policy_value"},
        "timeout_sec": 1185,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.patch_unary(request)


def test_patch_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service="backend_service_value",
            backend_service_resource=compute.BackendService(
                affinity_cookie_ttl_sec=2432
            ),
        )
        mock_args.update(sample_request)
        client.patch_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}"
            % client.transport._host,
            args[1],
        )


def test_patch_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_unary(
            compute.PatchBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
            backend_service_resource=compute.BackendService(
                affinity_cookie_ttl_sec=2432
            ),
        )


def test_patch_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.SetSecurityPolicyBackendServiceRequest, dict,]
)
def test_set_security_policy_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["security_policy_reference_resource"] = {
        "security_policy": "security_policy_value"
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_security_policy_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_security_policy_unary_rest_required_fields(
    request_type=compute.SetSecurityPolicyBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_security_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_security_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_security_policy_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_security_policy_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_security_policy._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(("backendService", "project", "securityPolicyReferenceResource",))
    )


def test_set_security_policy_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.SetSecurityPolicyBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["security_policy_reference_resource"] = {
        "security_policy": "security_policy_value"
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_security_policy_unary(request)


def test_set_security_policy_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service="backend_service_value",
            security_policy_reference_resource=compute.SecurityPolicyReference(
                security_policy="security_policy_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_security_policy_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}/setSecurityPolicy"
            % client.transport._host,
            args[1],
        )


def test_set_security_policy_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_security_policy_unary(
            compute.SetSecurityPolicyBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
            security_policy_reference_resource=compute.SecurityPolicyReference(
                security_policy="security_policy_value"
            ),
        )


def test_set_security_policy_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize("request_type", [compute.UpdateBackendServiceRequest, dict,])
def test_update_unary_rest(request_type):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["backend_service_resource"] = {
        "affinity_cookie_ttl_sec": 2432,
        "backends": [
            {
                "balancing_mode": "balancing_mode_value",
                "capacity_scaler": 0.1575,
                "description": "description_value",
                "failover": True,
                "group": "group_value",
                "max_connections": 1608,
                "max_connections_per_endpoint": 2990,
                "max_connections_per_instance": 2978,
                "max_rate": 849,
                "max_rate_per_endpoint": 0.22310000000000002,
                "max_rate_per_instance": 0.22190000000000001,
                "max_utilization": 0.1633,
            }
        ],
        "cdn_policy": {
            "bypass_cache_on_request_headers": [{"header_name": "header_name_value"}],
            "cache_key_policy": {
                "include_host": True,
                "include_protocol": True,
                "include_query_string": True,
                "query_string_blacklist": [
                    "query_string_blacklist_value_1",
                    "query_string_blacklist_value_2",
                ],
                "query_string_whitelist": [
                    "query_string_whitelist_value_1",
                    "query_string_whitelist_value_2",
                ],
            },
            "cache_mode": "cache_mode_value",
            "client_ttl": 1074,
            "default_ttl": 1176,
            "max_ttl": 761,
            "negative_caching": True,
            "negative_caching_policy": [{"code": 411, "ttl": 340}],
            "request_coalescing": True,
            "serve_while_stale": 1813,
            "signed_url_cache_max_age_sec": 2890,
            "signed_url_key_names": [
                "signed_url_key_names_value_1",
                "signed_url_key_names_value_2",
            ],
        },
        "circuit_breakers": {
            "max_connections": 1608,
            "max_pending_requests": 2149,
            "max_requests": 1313,
            "max_requests_per_connection": 2902,
            "max_retries": 1187,
        },
        "connection_draining": {"draining_timeout_sec": 2124},
        "consistent_hash": {
            "http_cookie": {
                "name": "name_value",
                "path": "path_value",
                "ttl": {"nanos": 543, "seconds": 751},
            },
            "http_header_name": "http_header_name_value",
            "minimum_ring_size": 1829,
        },
        "creation_timestamp": "creation_timestamp_value",
        "custom_request_headers": [
            "custom_request_headers_value_1",
            "custom_request_headers_value_2",
        ],
        "custom_response_headers": [
            "custom_response_headers_value_1",
            "custom_response_headers_value_2",
        ],
        "description": "description_value",
        "enable_c_d_n": True,
        "failover_policy": {
            "disable_connection_drain_on_failover": True,
            "drop_traffic_if_unhealthy": True,
            "failover_ratio": 0.1494,
        },
        "fingerprint": "fingerprint_value",
        "health_checks": ["health_checks_value_1", "health_checks_value_2"],
        "iap": {
            "enabled": True,
            "oauth2_client_id": "oauth2_client_id_value",
            "oauth2_client_secret": "oauth2_client_secret_value",
            "oauth2_client_secret_sha256": "oauth2_client_secret_sha256_value",
        },
        "id": 205,
        "kind": "kind_value",
        "load_balancing_scheme": "load_balancing_scheme_value",
        "locality_lb_policy": "locality_lb_policy_value",
        "log_config": {"enable": True, "sample_rate": 0.1165},
        "max_stream_duration": {"nanos": 543, "seconds": 751},
        "name": "name_value",
        "network": "network_value",
        "outlier_detection": {
            "base_ejection_time": {"nanos": 543, "seconds": 751},
            "consecutive_errors": 1956,
            "consecutive_gateway_failure": 2880,
            "enforcing_consecutive_errors": 3006,
            "enforcing_consecutive_gateway_failure": 3930,
            "enforcing_success_rate": 2334,
            "interval": {"nanos": 543, "seconds": 751},
            "max_ejection_percent": 2118,
            "success_rate_minimum_hosts": 2799,
            "success_rate_request_volume": 2915,
            "success_rate_stdev_factor": 2663,
        },
        "port": 453,
        "port_name": "port_name_value",
        "protocol": "protocol_value",
        "region": "region_value",
        "security_policy": "security_policy_value",
        "security_settings": {
            "client_tls_policy": "client_tls_policy_value",
            "subject_alt_names": [
                "subject_alt_names_value_1",
                "subject_alt_names_value_2",
            ],
        },
        "self_link": "self_link_value",
        "session_affinity": "session_affinity_value",
        "subsetting": {"policy": "policy_value"},
        "timeout_sec": 1185,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_unary(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_unary_rest_required_fields(
    request_type=compute.UpdateBackendServiceRequest,
):
    transport_class = transports.BackendServicesRestTransport

    request_init = {}
    request_init["backend_service"] = ""
    request_init["project"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["backendService"] = "backend_service_value"
    jsonified_request["project"] = "project_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "backendService" in jsonified_request
    assert jsonified_request["backendService"] == "backend_service_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"

    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.Operation()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "put",
                "query_params": request_init,
            }
            transcode_result["body"] = {}
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = compute.Operation.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_unary_rest_unset_required_fields():
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(("backendService", "backendServiceResource", "project",))
    )


def test_update_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.UpdateBackendServiceRequest
):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "backend_service": "sample2"}
    request_init["backend_service_resource"] = {
        "affinity_cookie_ttl_sec": 2432,
        "backends": [
            {
                "balancing_mode": "balancing_mode_value",
                "capacity_scaler": 0.1575,
                "description": "description_value",
                "failover": True,
                "group": "group_value",
                "max_connections": 1608,
                "max_connections_per_endpoint": 2990,
                "max_connections_per_instance": 2978,
                "max_rate": 849,
                "max_rate_per_endpoint": 0.22310000000000002,
                "max_rate_per_instance": 0.22190000000000001,
                "max_utilization": 0.1633,
            }
        ],
        "cdn_policy": {
            "bypass_cache_on_request_headers": [{"header_name": "header_name_value"}],
            "cache_key_policy": {
                "include_host": True,
                "include_protocol": True,
                "include_query_string": True,
                "query_string_blacklist": [
                    "query_string_blacklist_value_1",
                    "query_string_blacklist_value_2",
                ],
                "query_string_whitelist": [
                    "query_string_whitelist_value_1",
                    "query_string_whitelist_value_2",
                ],
            },
            "cache_mode": "cache_mode_value",
            "client_ttl": 1074,
            "default_ttl": 1176,
            "max_ttl": 761,
            "negative_caching": True,
            "negative_caching_policy": [{"code": 411, "ttl": 340}],
            "request_coalescing": True,
            "serve_while_stale": 1813,
            "signed_url_cache_max_age_sec": 2890,
            "signed_url_key_names": [
                "signed_url_key_names_value_1",
                "signed_url_key_names_value_2",
            ],
        },
        "circuit_breakers": {
            "max_connections": 1608,
            "max_pending_requests": 2149,
            "max_requests": 1313,
            "max_requests_per_connection": 2902,
            "max_retries": 1187,
        },
        "connection_draining": {"draining_timeout_sec": 2124},
        "consistent_hash": {
            "http_cookie": {
                "name": "name_value",
                "path": "path_value",
                "ttl": {"nanos": 543, "seconds": 751},
            },
            "http_header_name": "http_header_name_value",
            "minimum_ring_size": 1829,
        },
        "creation_timestamp": "creation_timestamp_value",
        "custom_request_headers": [
            "custom_request_headers_value_1",
            "custom_request_headers_value_2",
        ],
        "custom_response_headers": [
            "custom_response_headers_value_1",
            "custom_response_headers_value_2",
        ],
        "description": "description_value",
        "enable_c_d_n": True,
        "failover_policy": {
            "disable_connection_drain_on_failover": True,
            "drop_traffic_if_unhealthy": True,
            "failover_ratio": 0.1494,
        },
        "fingerprint": "fingerprint_value",
        "health_checks": ["health_checks_value_1", "health_checks_value_2"],
        "iap": {
            "enabled": True,
            "oauth2_client_id": "oauth2_client_id_value",
            "oauth2_client_secret": "oauth2_client_secret_value",
            "oauth2_client_secret_sha256": "oauth2_client_secret_sha256_value",
        },
        "id": 205,
        "kind": "kind_value",
        "load_balancing_scheme": "load_balancing_scheme_value",
        "locality_lb_policy": "locality_lb_policy_value",
        "log_config": {"enable": True, "sample_rate": 0.1165},
        "max_stream_duration": {"nanos": 543, "seconds": 751},
        "name": "name_value",
        "network": "network_value",
        "outlier_detection": {
            "base_ejection_time": {"nanos": 543, "seconds": 751},
            "consecutive_errors": 1956,
            "consecutive_gateway_failure": 2880,
            "enforcing_consecutive_errors": 3006,
            "enforcing_consecutive_gateway_failure": 3930,
            "enforcing_success_rate": 2334,
            "interval": {"nanos": 543, "seconds": 751},
            "max_ejection_percent": 2118,
            "success_rate_minimum_hosts": 2799,
            "success_rate_request_volume": 2915,
            "success_rate_stdev_factor": 2663,
        },
        "port": 453,
        "port_name": "port_name_value",
        "protocol": "protocol_value",
        "region": "region_value",
        "security_policy": "security_policy_value",
        "security_settings": {
            "client_tls_policy": "client_tls_policy_value",
            "subject_alt_names": [
                "subject_alt_names_value_1",
                "subject_alt_names_value_2",
            ],
        },
        "self_link": "self_link_value",
        "session_affinity": "session_affinity_value",
        "subsetting": {"policy": "policy_value"},
        "timeout_sec": 1185,
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_unary(request)


def test_update_unary_rest_flattened():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "backend_service": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            backend_service="backend_service_value",
            backend_service_resource=compute.BackendService(
                affinity_cookie_ttl_sec=2432
            ),
        )
        mock_args.update(sample_request)
        client.update_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/global/backendServices/{backend_service}"
            % client.transport._host,
            args[1],
        )


def test_update_unary_rest_flattened_error(transport: str = "rest"):
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_unary(
            compute.UpdateBackendServiceRequest(),
            project="project_value",
            backend_service="backend_service_value",
            backend_service_resource=compute.BackendService(
                affinity_cookie_ttl_sec=2432
            ),
        )


def test_update_unary_rest_error():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BackendServicesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BackendServicesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BackendServicesClient(client_options=options, transport=transport,)

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BackendServicesClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BackendServicesClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BackendServicesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = BackendServicesClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize("transport_class", [transports.BackendServicesRestTransport,])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_backend_services_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.BackendServicesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_backend_services_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.backend_services.transports.BackendServicesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BackendServicesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "add_signed_url_key",
        "aggregated_list",
        "delete",
        "delete_signed_url_key",
        "get",
        "get_health",
        "insert",
        "list",
        "patch",
        "set_security_policy",
        "update",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_backend_services_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.backend_services.transports.BackendServicesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BackendServicesTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_backend_services_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.backend_services.transports.BackendServicesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BackendServicesTransport()
        adc.assert_called_once()


def test_backend_services_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        BackendServicesClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_backend_services_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.BackendServicesRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_backend_services_host_no_port():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_backend_services_host_with_port():
    client = BackendServicesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:8000"


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BackendServicesClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = BackendServicesClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BackendServicesClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = BackendServicesClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = BackendServicesClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BackendServicesClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = BackendServicesClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = BackendServicesClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BackendServicesClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = BackendServicesClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = BackendServicesClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BackendServicesClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = BackendServicesClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = BackendServicesClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BackendServicesClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BackendServicesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BackendServicesClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BackendServicesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BackendServicesClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = BackendServicesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
    ]
    for transport in transports:
        client = BackendServicesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [(BackendServicesClient, transports.BackendServicesRestTransport),],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )
