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
from google.cloud.compute_v1.services.region_instance_group_managers import (
    RegionInstanceGroupManagersClient,
)
from google.cloud.compute_v1.services.region_instance_group_managers import pagers
from google.cloud.compute_v1.services.region_instance_group_managers import transports
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

    assert RegionInstanceGroupManagersClient._get_default_mtls_endpoint(None) is None
    assert (
        RegionInstanceGroupManagersClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegionInstanceGroupManagersClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegionInstanceGroupManagersClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RegionInstanceGroupManagersClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        RegionInstanceGroupManagersClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize("client_class", [RegionInstanceGroupManagersClient,])
def test_region_instance_group_managers_client_from_service_account_info(client_class):
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
    [(transports.RegionInstanceGroupManagersRestTransport, "rest"),],
)
def test_region_instance_group_managers_client_service_account_always_use_jwt(
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


@pytest.mark.parametrize("client_class", [RegionInstanceGroupManagersClient,])
def test_region_instance_group_managers_client_from_service_account_file(client_class):
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


def test_region_instance_group_managers_client_get_transport_class():
    transport = RegionInstanceGroupManagersClient.get_transport_class()
    available_transports = [
        transports.RegionInstanceGroupManagersRestTransport,
    ]
    assert transport in available_transports

    transport = RegionInstanceGroupManagersClient.get_transport_class("rest")
    assert transport == transports.RegionInstanceGroupManagersRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            RegionInstanceGroupManagersClient,
            transports.RegionInstanceGroupManagersRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    RegionInstanceGroupManagersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegionInstanceGroupManagersClient),
)
def test_region_instance_group_managers_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        RegionInstanceGroupManagersClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        RegionInstanceGroupManagersClient, "get_transport_class"
    ) as gtc:
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
            RegionInstanceGroupManagersClient,
            transports.RegionInstanceGroupManagersRestTransport,
            "rest",
            "true",
        ),
        (
            RegionInstanceGroupManagersClient,
            transports.RegionInstanceGroupManagersRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    RegionInstanceGroupManagersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegionInstanceGroupManagersClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_region_instance_group_managers_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [RegionInstanceGroupManagersClient])
@mock.patch.object(
    RegionInstanceGroupManagersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RegionInstanceGroupManagersClient),
)
def test_region_instance_group_managers_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
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
    [
        (
            RegionInstanceGroupManagersClient,
            transports.RegionInstanceGroupManagersRestTransport,
            "rest",
        ),
    ],
)
def test_region_instance_group_managers_client_client_options_scopes(
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
    [
        (
            RegionInstanceGroupManagersClient,
            transports.RegionInstanceGroupManagersRestTransport,
            "rest",
        ),
    ],
)
def test_region_instance_group_managers_client_client_options_credentials_file(
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
    "request_type", [compute.AbandonInstancesRegionInstanceGroupManagerRequest, dict,]
)
def test_abandon_instances_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init[
        "region_instance_group_managers_abandon_instances_request_resource"
    ] = {"instances": ["instances_value_1", "instances_value_2"]}
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
        response = client.abandon_instances_unary(request)

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


def test_abandon_instances_unary_rest_required_fields(
    request_type=compute.AbandonInstancesRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).abandon_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).abandon_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.abandon_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_abandon_instances_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.abandon_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersAbandonInstancesRequestResource",
            )
        )
    )


def test_abandon_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.AbandonInstancesRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init[
        "region_instance_group_managers_abandon_instances_request_resource"
    ] = {"instances": ["instances_value_1", "instances_value_2"]}
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
        client.abandon_instances_unary(request)


def test_abandon_instances_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_abandon_instances_request_resource=compute.RegionInstanceGroupManagersAbandonInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)
        client.abandon_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/abandonInstances"
            % client.transport._host,
            args[1],
        )


def test_abandon_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.abandon_instances_unary(
            compute.AbandonInstancesRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_abandon_instances_request_resource=compute.RegionInstanceGroupManagersAbandonInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_abandon_instances_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest, dict,],
)
def test_apply_updates_to_instances_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_apply_updates_request_resource"] = {
        "all_instances": True,
        "instances": ["instances_value_1", "instances_value_2"],
        "minimal_action": "minimal_action_value",
        "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
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
        response = client.apply_updates_to_instances_unary(request)

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


def test_apply_updates_to_instances_unary_rest_required_fields(
    request_type=compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_updates_to_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_updates_to_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.apply_updates_to_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_apply_updates_to_instances_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.apply_updates_to_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersApplyUpdatesRequestResource",
            )
        )
    )


def test_apply_updates_to_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_apply_updates_request_resource"] = {
        "all_instances": True,
        "instances": ["instances_value_1", "instances_value_2"],
        "minimal_action": "minimal_action_value",
        "most_disruptive_allowed_action": "most_disruptive_allowed_action_value",
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
        client.apply_updates_to_instances_unary(request)


def test_apply_updates_to_instances_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_apply_updates_request_resource=compute.RegionInstanceGroupManagersApplyUpdatesRequest(
                all_instances=True
            ),
        )
        mock_args.update(sample_request)
        client.apply_updates_to_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/applyUpdatesToInstances"
            % client.transport._host,
            args[1],
        )


def test_apply_updates_to_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_updates_to_instances_unary(
            compute.ApplyUpdatesToInstancesRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_apply_updates_request_resource=compute.RegionInstanceGroupManagersApplyUpdatesRequest(
                all_instances=True
            ),
        )


def test_apply_updates_to_instances_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.CreateInstancesRegionInstanceGroupManagerRequest, dict,]
)
def test_create_instances_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_create_instances_request_resource"] = {
        "instances": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
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
        response = client.create_instances_unary(request)

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


def test_create_instances_unary_rest_required_fields(
    request_type=compute.CreateInstancesRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.create_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_instances_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersCreateInstancesRequestResource",
            )
        )
    )


def test_create_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.CreateInstancesRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_create_instances_request_resource"] = {
        "instances": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
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
        client.create_instances_unary(request)


def test_create_instances_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_create_instances_request_resource=compute.RegionInstanceGroupManagersCreateInstancesRequest(
                instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
            ),
        )
        mock_args.update(sample_request)
        client.create_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/createInstances"
            % client.transport._host,
            args[1],
        )


def test_create_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_instances_unary(
            compute.CreateInstancesRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_create_instances_request_resource=compute.RegionInstanceGroupManagersCreateInstancesRequest(
                instances=[compute.PerInstanceConfig(fingerprint="fingerprint_value")]
            ),
        )


def test_create_instances_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.DeleteRegionInstanceGroupManagerRequest, dict,]
)
def test_delete_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
    request_type=compute.DeleteRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
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

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",)) & set(("instanceGroupManager", "project", "region",))
    )


def test_delete_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeleteRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        client.delete_unary(request)


def test_delete_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)
        client.delete_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_delete_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_unary(
            compute.DeleteRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_delete_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.DeleteInstancesRegionInstanceGroupManagerRequest, dict,]
)
def test_delete_instances_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_delete_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"],
        "skip_instances_on_validation_error": True,
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
        response = client.delete_instances_unary(request)

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


def test_delete_instances_unary_rest_required_fields(
    request_type=compute.DeleteInstancesRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.delete_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_instances_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersDeleteInstancesRequestResource",
            )
        )
    )


def test_delete_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeleteInstancesRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_delete_instances_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"],
        "skip_instances_on_validation_error": True,
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
        client.delete_instances_unary(request)


def test_delete_instances_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_delete_instances_request_resource=compute.RegionInstanceGroupManagersDeleteInstancesRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)
        client.delete_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/deleteInstances"
            % client.transport._host,
            args[1],
        )


def test_delete_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_instances_unary(
            compute.DeleteInstancesRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_delete_instances_request_resource=compute.RegionInstanceGroupManagersDeleteInstancesRequest(
                instances=["instances_value"]
            ),
        )


def test_delete_instances_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest, dict,],
)
def test_delete_per_instance_configs_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init[
        "region_instance_group_manager_delete_instance_config_req_resource"
    ] = {"names": ["names_value_1", "names_value_2"]}
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
        response = client.delete_per_instance_configs_unary(request)

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


def test_delete_per_instance_configs_unary_rest_required_fields(
    request_type=compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.delete_per_instance_configs_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_per_instance_configs_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagerDeleteInstanceConfigReqResource",
            )
        )
    )


def test_delete_per_instance_configs_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init[
        "region_instance_group_manager_delete_instance_config_req_resource"
    ] = {"names": ["names_value_1", "names_value_2"]}
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
        client.delete_per_instance_configs_unary(request)


def test_delete_per_instance_configs_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_manager_delete_instance_config_req_resource=compute.RegionInstanceGroupManagerDeleteInstanceConfigReq(
                names=["names_value"]
            ),
        )
        mock_args.update(sample_request)
        client.delete_per_instance_configs_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/deletePerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_delete_per_instance_configs_unary_rest_flattened_error(
    transport: str = "rest",
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_per_instance_configs_unary(
            compute.DeletePerInstanceConfigsRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_manager_delete_instance_config_req_resource=compute.RegionInstanceGroupManagerDeleteInstanceConfigReq(
                names=["names_value"]
            ),
        )


def test_delete_per_instance_configs_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.GetRegionInstanceGroupManagerRequest, dict,]
)
def test_get_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManager(
            base_instance_name="base_instance_name_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            fingerprint="fingerprint_value",
            id=205,
            instance_group="instance_group_value",
            instance_template="instance_template_value",
            kind="kind_value",
            name="name_value",
            region="region_value",
            self_link="self_link_value",
            target_pools=["target_pools_value"],
            target_size=1185,
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManager.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.InstanceGroupManager)
    assert response.base_instance_name == "base_instance_name_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.fingerprint == "fingerprint_value"
    assert response.id == 205
    assert response.instance_group == "instance_group_value"
    assert response.instance_template == "instance_template_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.target_pools == ["target_pools_value"]
    assert response.target_size == 1185
    assert response.zone == "zone_value"


def test_get_rest_required_fields(
    request_type=compute.GetRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
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

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.InstanceGroupManager()
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
            json_return_value = compute.InstanceGroupManager.to_json(return_value)
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(()) & set(("instanceGroupManager", "project", "region",))
    )


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetRegionInstanceGroupManagerRequest
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        client.get(request)


def test_get_rest_flattened():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceGroupManager()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceGroupManager.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)
        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_get_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.InsertRegionInstanceGroupManagerRequest, dict,]
)
def test_insert_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {"calculated": 1042, "fixed": 528, "percent": 753},
            "minimal_action": "minimal_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {"calculated": 1042, "fixed": 528, "percent": 753},
            }
        ],
        "zone": "zone_value",
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
    request_type=compute.InsertRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
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
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).insert._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.insert._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(("instanceGroupManagerResource", "project", "region",))
    )


def test_insert_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.InsertRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {"calculated": 1042, "fixed": 528, "percent": 753},
            "minimal_action": "minimal_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {"calculated": 1042, "fixed": 528, "percent": 753},
            }
        ],
        "zone": "zone_value",
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
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {"project": "sample1", "region": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager_resource=compute.InstanceGroupManager(
                auto_healing_policies=[
                    compute.InstanceGroupManagerAutoHealingPolicy(
                        health_check="health_check_value"
                    )
                ]
            ),
        )
        mock_args.update(sample_request)
        client.insert_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers"
            % client.transport._host,
            args[1],
        )


def test_insert_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert_unary(
            compute.InsertRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager_resource=compute.InstanceGroupManager(
                auto_healing_policies=[
                    compute.InstanceGroupManagerAutoHealingPolicy(
                        health_check="health_check_value"
                    )
                ]
            ),
        )


def test_insert_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.ListRegionInstanceGroupManagersRequest, dict,]
)
def test_list_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagerList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagerList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


def test_list_rest_required_fields(
    request_type=compute.ListRegionInstanceGroupManagersRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["project"] = ""
    request_init["region"] = ""
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
    jsonified_request["region"] = "region_value"

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
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.RegionInstanceGroupManagerList()
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
            json_return_value = compute.RegionInstanceGroupManagerList.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("maxResults", "filter", "orderBy", "pageToken", "returnPartialSuccess",))
        & set(("project", "region",))
    )


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListRegionInstanceGroupManagersRequest
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "region": "sample2"}
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
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagerList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagerList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "region": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value", region="region_value",)
        mock_args.update(sample_request)
        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers"
            % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListRegionInstanceGroupManagersRequest(),
            project="project_value",
            region="region_value",
        )


def test_list_rest_pager(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.RegionInstanceGroupManagerList(
                items=[
                    compute.InstanceGroupManager(),
                    compute.InstanceGroupManager(),
                    compute.InstanceGroupManager(),
                ],
                next_page_token="abc",
            ),
            compute.RegionInstanceGroupManagerList(items=[], next_page_token="def",),
            compute.RegionInstanceGroupManagerList(
                items=[compute.InstanceGroupManager(),], next_page_token="ghi",
            ),
            compute.RegionInstanceGroupManagerList(
                items=[compute.InstanceGroupManager(), compute.InstanceGroupManager(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.RegionInstanceGroupManagerList.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1", "region": "sample2"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.InstanceGroupManager) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type", [compute.ListErrorsRegionInstanceGroupManagersRequest, dict,]
)
def test_list_errors_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagersListErrorsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagersListErrorsResponse.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_errors(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListErrorsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_errors_rest_required_fields(
    request_type=compute.ListErrorsRegionInstanceGroupManagersRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_errors._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_errors._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        ("max_results", "filter", "order_by", "page_token", "return_partial_success",)
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.RegionInstanceGroupManagersListErrorsResponse()
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
            json_return_value = compute.RegionInstanceGroupManagersListErrorsResponse.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_errors(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_errors_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_errors._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("maxResults", "filter", "orderBy", "pageToken", "returnPartialSuccess",))
        & set(("instanceGroupManager", "project", "region",))
    )


def test_list_errors_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ListErrorsRegionInstanceGroupManagersRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        client.list_errors(request)


def test_list_errors_rest_flattened():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagersListErrorsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagersListErrorsResponse.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)
        client.list_errors(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listErrors"
            % client.transport._host,
            args[1],
        )


def test_list_errors_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_errors(
            compute.ListErrorsRegionInstanceGroupManagersRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_list_errors_rest_pager(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.RegionInstanceGroupManagersListErrorsResponse(
                items=[
                    compute.InstanceManagedByIgmError(),
                    compute.InstanceManagedByIgmError(),
                    compute.InstanceManagedByIgmError(),
                ],
                next_page_token="abc",
            ),
            compute.RegionInstanceGroupManagersListErrorsResponse(
                items=[], next_page_token="def",
            ),
            compute.RegionInstanceGroupManagersListErrorsResponse(
                items=[compute.InstanceManagedByIgmError(),], next_page_token="ghi",
            ),
            compute.RegionInstanceGroupManagersListErrorsResponse(
                items=[
                    compute.InstanceManagedByIgmError(),
                    compute.InstanceManagedByIgmError(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.RegionInstanceGroupManagersListErrorsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        pager = client.list_errors(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.InstanceManagedByIgmError) for i in results)

        pages = list(client.list_errors(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [compute.ListManagedInstancesRegionInstanceGroupManagersRequest, dict,],
)
def test_list_managed_instances_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagersListInstancesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagersListInstancesResponse.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_managed_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListManagedInstancesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_managed_instances_rest_required_fields(
    request_type=compute.ListManagedInstancesRegionInstanceGroupManagersRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_managed_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_managed_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        ("max_results", "filter", "order_by", "page_token", "return_partial_success",)
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.RegionInstanceGroupManagersListInstancesResponse()
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
            json_return_value = compute.RegionInstanceGroupManagersListInstancesResponse.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_managed_instances(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_managed_instances_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_managed_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("maxResults", "filter", "orderBy", "pageToken", "returnPartialSuccess",))
        & set(("instanceGroupManager", "project", "region",))
    )


def test_list_managed_instances_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ListManagedInstancesRegionInstanceGroupManagersRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        client.list_managed_instances(request)


def test_list_managed_instances_rest_flattened():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagersListInstancesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagersListInstancesResponse.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)
        client.list_managed_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listManagedInstances"
            % client.transport._host,
            args[1],
        )


def test_list_managed_instances_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_managed_instances(
            compute.ListManagedInstancesRegionInstanceGroupManagersRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_list_managed_instances_rest_pager(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.RegionInstanceGroupManagersListInstancesResponse(
                managed_instances=[
                    compute.ManagedInstance(),
                    compute.ManagedInstance(),
                    compute.ManagedInstance(),
                ],
                next_page_token="abc",
            ),
            compute.RegionInstanceGroupManagersListInstancesResponse(
                managed_instances=[], next_page_token="def",
            ),
            compute.RegionInstanceGroupManagersListInstancesResponse(
                managed_instances=[compute.ManagedInstance(),], next_page_token="ghi",
            ),
            compute.RegionInstanceGroupManagersListInstancesResponse(
                managed_instances=[
                    compute.ManagedInstance(),
                    compute.ManagedInstance(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.RegionInstanceGroupManagersListInstancesResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        pager = client.list_managed_instances(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.ManagedInstance) for i in results)

        pages = list(client.list_managed_instances(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest, dict,],
)
def test_list_per_instance_configs_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagersListInstanceConfigsResp(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagersListInstanceConfigsResp.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_per_instance_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPerInstanceConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_per_instance_configs_rest_required_fields(
    request_type=compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        ("max_results", "filter", "order_by", "page_token", "return_partial_success",)
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )
    request = request_type(request_init)

    # Designate an appropriate value for the returned response.
    return_value = compute.RegionInstanceGroupManagersListInstanceConfigsResp()
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
            json_return_value = compute.RegionInstanceGroupManagersListInstanceConfigsResp.to_json(
                return_value
            )
            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_per_instance_configs(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_per_instance_configs_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("maxResults", "filter", "orderBy", "pageToken", "returnPartialSuccess",))
        & set(("instanceGroupManager", "project", "region",))
    )


def test_list_per_instance_configs_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        client.list_per_instance_configs(request)


def test_list_per_instance_configs_rest_flattened():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.RegionInstanceGroupManagersListInstanceConfigsResp()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.RegionInstanceGroupManagersListInstanceConfigsResp.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )
        mock_args.update(sample_request)
        client.list_per_instance_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/listPerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_list_per_instance_configs_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_per_instance_configs(
            compute.ListPerInstanceConfigsRegionInstanceGroupManagersRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
        )


def test_list_per_instance_configs_rest_pager(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.RegionInstanceGroupManagersListInstanceConfigsResp(
                items=[
                    compute.PerInstanceConfig(),
                    compute.PerInstanceConfig(),
                    compute.PerInstanceConfig(),
                ],
                next_page_token="abc",
            ),
            compute.RegionInstanceGroupManagersListInstanceConfigsResp(
                items=[], next_page_token="def",
            ),
            compute.RegionInstanceGroupManagersListInstanceConfigsResp(
                items=[compute.PerInstanceConfig(),], next_page_token="ghi",
            ),
            compute.RegionInstanceGroupManagersListInstanceConfigsResp(
                items=[compute.PerInstanceConfig(), compute.PerInstanceConfig(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.RegionInstanceGroupManagersListInstanceConfigsResp.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        pager = client.list_per_instance_configs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.PerInstanceConfig) for i in results)

        pages = list(client.list_per_instance_configs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type", [compute.PatchRegionInstanceGroupManagerRequest, dict,]
)
def test_patch_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {"calculated": 1042, "fixed": 528, "percent": 753},
            "minimal_action": "minimal_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {"calculated": 1042, "fixed": 528, "percent": 753},
            }
        ],
        "zone": "zone_value",
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
    request_type=compute.PatchRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
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

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "instanceGroupManagerResource",
                "project",
                "region",
            )
        )
    )


def test_patch_unary_rest_bad_request(
    transport: str = "rest", request_type=compute.PatchRegionInstanceGroupManagerRequest
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["instance_group_manager_resource"] = {
        "auto_healing_policies": [
            {"health_check": "health_check_value", "initial_delay_sec": 1778}
        ],
        "base_instance_name": "base_instance_name_value",
        "creation_timestamp": "creation_timestamp_value",
        "current_actions": {
            "abandoning": 1041,
            "creating": 845,
            "creating_without_retries": 2589,
            "deleting": 844,
            "none": 432,
            "recreating": 1060,
            "refreshing": 1069,
            "restarting": 1091,
            "verifying": 979,
        },
        "description": "description_value",
        "distribution_policy": {
            "target_shape": "target_shape_value",
            "zones": [{"zone": "zone_value"}],
        },
        "fingerprint": "fingerprint_value",
        "id": 205,
        "instance_group": "instance_group_value",
        "instance_template": "instance_template_value",
        "kind": "kind_value",
        "name": "name_value",
        "named_ports": [{"name": "name_value", "port": 453}],
        "region": "region_value",
        "self_link": "self_link_value",
        "stateful_policy": {"preserved_state": {"disks": {}}},
        "status": {
            "autoscaler": "autoscaler_value",
            "is_stable": True,
            "stateful": {
                "has_stateful_config": True,
                "per_instance_configs": {"all_effective": True},
            },
            "version_target": {"is_reached": True},
        },
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
        "target_size": 1185,
        "update_policy": {
            "instance_redistribution_type": "instance_redistribution_type_value",
            "max_surge": {"calculated": 1042, "fixed": 528, "percent": 753},
            "max_unavailable": {"calculated": 1042, "fixed": 528, "percent": 753},
            "minimal_action": "minimal_action_value",
            "replacement_method": "replacement_method_value",
            "type_": "type__value",
        },
        "versions": [
            {
                "instance_template": "instance_template_value",
                "name": "name_value",
                "target_size": {"calculated": 1042, "fixed": 528, "percent": 753},
            }
        ],
        "zone": "zone_value",
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
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_manager_resource=compute.InstanceGroupManager(
                auto_healing_policies=[
                    compute.InstanceGroupManagerAutoHealingPolicy(
                        health_check="health_check_value"
                    )
                ]
            ),
        )
        mock_args.update(sample_request)
        client.patch_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}"
            % client.transport._host,
            args[1],
        )


def test_patch_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_unary(
            compute.PatchRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            instance_group_manager_resource=compute.InstanceGroupManager(
                auto_healing_policies=[
                    compute.InstanceGroupManagerAutoHealingPolicy(
                        health_check="health_check_value"
                    )
                ]
            ),
        )


def test_patch_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest, dict,],
)
def test_patch_per_instance_configs_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_manager_patch_instance_config_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
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
        response = client.patch_per_instance_configs_unary(request)

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


def test_patch_per_instance_configs_unary_rest_required_fields(
    request_type=compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).patch_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.patch_per_instance_configs_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_patch_per_instance_configs_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.patch_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagerPatchInstanceConfigReqResource",
            )
        )
    )


def test_patch_per_instance_configs_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_manager_patch_instance_config_req_resource"] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
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
        client.patch_per_instance_configs_unary(request)


def test_patch_per_instance_configs_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_manager_patch_instance_config_req_resource=compute.RegionInstanceGroupManagerPatchInstanceConfigReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )
        mock_args.update(sample_request)
        client.patch_per_instance_configs_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/patchPerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_patch_per_instance_configs_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch_per_instance_configs_unary(
            compute.PatchPerInstanceConfigsRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_manager_patch_instance_config_req_resource=compute.RegionInstanceGroupManagerPatchInstanceConfigReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )


def test_patch_per_instance_configs_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.RecreateInstancesRegionInstanceGroupManagerRequest, dict,]
)
def test_recreate_instances_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_recreate_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
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
        response = client.recreate_instances_unary(request)

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


def test_recreate_instances_unary_rest_required_fields(
    request_type=compute.RecreateInstancesRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recreate_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).recreate_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.recreate_instances_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_recreate_instances_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.recreate_instances._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersRecreateRequestResource",
            )
        )
    )


def test_recreate_instances_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.RecreateInstancesRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_recreate_request_resource"] = {
        "instances": ["instances_value_1", "instances_value_2"]
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
        client.recreate_instances_unary(request)


def test_recreate_instances_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_recreate_request_resource=compute.RegionInstanceGroupManagersRecreateRequest(
                instances=["instances_value"]
            ),
        )
        mock_args.update(sample_request)
        client.recreate_instances_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/recreateInstances"
            % client.transport._host,
            args[1],
        )


def test_recreate_instances_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.recreate_instances_unary(
            compute.RecreateInstancesRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_recreate_request_resource=compute.RegionInstanceGroupManagersRecreateRequest(
                instances=["instances_value"]
            ),
        )


def test_recreate_instances_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.ResizeRegionInstanceGroupManagerRequest, dict,]
)
def test_resize_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        response = client.resize_unary(request)

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


def test_resize_unary_rest_required_fields(
    request_type=compute.ResizeRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request_init["size"] = 0
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped
    assert "size" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "size" in jsonified_request
    assert jsonified_request["size"] == request_init["size"]

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"
    jsonified_request["size"] = 443

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id", "size",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"
    assert "size" in jsonified_request
    assert jsonified_request["size"] == 443

    client = RegionInstanceGroupManagersClient(
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

            response = client.resize_unary(request)

            expected_params = [
                ("size", 0,),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_resize_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.resize._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId", "size",))
        & set(("instanceGroupManager", "project", "region", "size",))
    )


def test_resize_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.ResizeRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
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
        client.resize_unary(request)


def test_resize_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )
        mock_args.update(sample_request)
        client.resize_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/resize"
            % client.transport._host,
            args[1],
        )


def test_resize_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resize_unary(
            compute.ResizeRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            size=443,
        )


def test_resize_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [compute.SetInstanceTemplateRegionInstanceGroupManagerRequest, dict,],
)
def test_set_instance_template_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_set_template_request_resource"] = {
        "instance_template": "instance_template_value"
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
        response = client.set_instance_template_unary(request)

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


def test_set_instance_template_unary_rest_required_fields(
    request_type=compute.SetInstanceTemplateRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_instance_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_instance_template._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.set_instance_template_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_instance_template_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_instance_template._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersSetTemplateRequestResource",
            )
        )
    )


def test_set_instance_template_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetInstanceTemplateRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_set_template_request_resource"] = {
        "instance_template": "instance_template_value"
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
        client.set_instance_template_unary(request)


def test_set_instance_template_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_set_template_request_resource=compute.RegionInstanceGroupManagersSetTemplateRequest(
                instance_template="instance_template_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_instance_template_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/setInstanceTemplate"
            % client.transport._host,
            args[1],
        )


def test_set_instance_template_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_instance_template_unary(
            compute.SetInstanceTemplateRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_set_template_request_resource=compute.RegionInstanceGroupManagersSetTemplateRequest(
                instance_template="instance_template_value"
            ),
        )


def test_set_instance_template_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type", [compute.SetTargetPoolsRegionInstanceGroupManagerRequest, dict,]
)
def test_set_target_pools_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_set_target_pools_request_resource"] = {
        "fingerprint": "fingerprint_value",
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
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
        response = client.set_target_pools_unary(request)

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


def test_set_target_pools_unary_rest_required_fields(
    request_type=compute.SetTargetPoolsRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_target_pools._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_target_pools._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.set_target_pools_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_target_pools_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_target_pools._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagersSetTargetPoolsRequestResource",
            )
        )
    )


def test_set_target_pools_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetTargetPoolsRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init["region_instance_group_managers_set_target_pools_request_resource"] = {
        "fingerprint": "fingerprint_value",
        "target_pools": ["target_pools_value_1", "target_pools_value_2"],
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
        client.set_target_pools_unary(request)


def test_set_target_pools_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_set_target_pools_request_resource=compute.RegionInstanceGroupManagersSetTargetPoolsRequest(
                fingerprint="fingerprint_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_target_pools_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/setTargetPools"
            % client.transport._host,
            args[1],
        )


def test_set_target_pools_unary_rest_flattened_error(transport: str = "rest"):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_target_pools_unary(
            compute.SetTargetPoolsRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_managers_set_target_pools_request_resource=compute.RegionInstanceGroupManagersSetTargetPoolsRequest(
                fingerprint="fingerprint_value"
            ),
        )


def test_set_target_pools_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest, dict,],
)
def test_update_per_instance_configs_unary_rest(request_type):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init[
        "region_instance_group_manager_update_instance_config_req_resource"
    ] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
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
        response = client.update_per_instance_configs_unary(request)

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


def test_update_per_instance_configs_unary_rest_required_fields(
    request_type=compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
):
    transport_class = transports.RegionInstanceGroupManagersRestTransport

    request_init = {}
    request_init["instance_group_manager"] = ""
    request_init["project"] = ""
    request_init["region"] = ""
    request = request_type(request_init)
    jsonified_request = json.loads(
        request_type.to_json(
            request, including_default_value_fields=False, use_integers_for_enums=False
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_per_instance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instanceGroupManager"] = "instance_group_manager_value"
    jsonified_request["project"] = "project_value"
    jsonified_request["region"] = "region_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_per_instance_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instanceGroupManager" in jsonified_request
    assert jsonified_request["instanceGroupManager"] == "instance_group_manager_value"
    assert "project" in jsonified_request
    assert jsonified_request["project"] == "project_value"
    assert "region" in jsonified_request
    assert jsonified_request["region"] == "region_value"

    client = RegionInstanceGroupManagersClient(
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

            response = client.update_per_instance_configs_unary(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_per_instance_configs_unary_rest_unset_required_fields():
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_per_instance_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "instanceGroupManager",
                "project",
                "region",
                "regionInstanceGroupManagerUpdateInstanceConfigReqResource",
            )
        )
    )


def test_update_per_instance_configs_unary_rest_bad_request(
    transport: str = "rest",
    request_type=compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest,
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "project": "sample1",
        "region": "sample2",
        "instance_group_manager": "sample3",
    }
    request_init[
        "region_instance_group_manager_update_instance_config_req_resource"
    ] = {
        "per_instance_configs": [
            {
                "fingerprint": "fingerprint_value",
                "name": "name_value",
                "preserved_state": {"disks": {}, "metadata": {}},
                "status": "status_value",
            }
        ]
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
        client.update_per_instance_configs_unary(request)


def test_update_per_instance_configs_unary_rest_flattened():
    client = RegionInstanceGroupManagersClient(
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
        sample_request = {
            "project": "sample1",
            "region": "sample2",
            "instance_group_manager": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_manager_update_instance_config_req_resource=compute.RegionInstanceGroupManagerUpdateInstanceConfigReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )
        mock_args.update(sample_request)
        client.update_per_instance_configs_unary(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/regions/{region}/instanceGroupManagers/{instance_group_manager}/updatePerInstanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_update_per_instance_configs_unary_rest_flattened_error(
    transport: str = "rest",
):
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_per_instance_configs_unary(
            compute.UpdatePerInstanceConfigsRegionInstanceGroupManagerRequest(),
            project="project_value",
            region="region_value",
            instance_group_manager="instance_group_manager_value",
            region_instance_group_manager_update_instance_config_req_resource=compute.RegionInstanceGroupManagerUpdateInstanceConfigReq(
                per_instance_configs=[
                    compute.PerInstanceConfig(fingerprint="fingerprint_value")
                ]
            ),
        )


def test_update_per_instance_configs_unary_rest_error():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RegionInstanceGroupManagersClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RegionInstanceGroupManagersClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RegionInstanceGroupManagersClient(
            client_options=options, transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RegionInstanceGroupManagersClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RegionInstanceGroupManagersClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RegionInstanceGroupManagersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = RegionInstanceGroupManagersClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class", [transports.RegionInstanceGroupManagersRestTransport,]
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_region_instance_group_managers_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RegionInstanceGroupManagersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_region_instance_group_managers_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.region_instance_group_managers.transports.RegionInstanceGroupManagersTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RegionInstanceGroupManagersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "abandon_instances",
        "apply_updates_to_instances",
        "create_instances",
        "delete",
        "delete_instances",
        "delete_per_instance_configs",
        "get",
        "insert",
        "list",
        "list_errors",
        "list_managed_instances",
        "list_per_instance_configs",
        "patch",
        "patch_per_instance_configs",
        "recreate_instances",
        "resize",
        "set_instance_template",
        "set_target_pools",
        "update_per_instance_configs",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_region_instance_group_managers_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.region_instance_group_managers.transports.RegionInstanceGroupManagersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RegionInstanceGroupManagersTransport(
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


def test_region_instance_group_managers_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.region_instance_group_managers.transports.RegionInstanceGroupManagersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RegionInstanceGroupManagersTransport()
        adc.assert_called_once()


def test_region_instance_group_managers_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RegionInstanceGroupManagersClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_region_instance_group_managers_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.RegionInstanceGroupManagersRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_region_instance_group_managers_host_no_port():
    client = RegionInstanceGroupManagersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_region_instance_group_managers_host_with_port():
    client = RegionInstanceGroupManagersClient(
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
    actual = RegionInstanceGroupManagersClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = RegionInstanceGroupManagersClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionInstanceGroupManagersClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = RegionInstanceGroupManagersClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = RegionInstanceGroupManagersClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionInstanceGroupManagersClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = RegionInstanceGroupManagersClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = RegionInstanceGroupManagersClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionInstanceGroupManagersClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = RegionInstanceGroupManagersClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = RegionInstanceGroupManagersClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionInstanceGroupManagersClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = RegionInstanceGroupManagersClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = RegionInstanceGroupManagersClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RegionInstanceGroupManagersClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RegionInstanceGroupManagersTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RegionInstanceGroupManagersClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RegionInstanceGroupManagersTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RegionInstanceGroupManagersClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = RegionInstanceGroupManagersClient(
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
        client = RegionInstanceGroupManagersClient(
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
    [
        (
            RegionInstanceGroupManagersClient,
            transports.RegionInstanceGroupManagersRestTransport,
        ),
    ],
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
