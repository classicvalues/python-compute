from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import path_template
from google.api_core import gapic_v1
from requests import __version__ as requests_version
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

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

from google.cloud.compute_v1.types import compute

from .base import SubnetworksTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SubnetworksRestTransport(SubnetworksTransport):
    """REST backend transport for Subnetworks.

    The Subnetworks API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    __aggregated_list_required_fields_default_values = {
        "project": "",
    }

    @staticmethod
    def _aggregated_list_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__aggregated_list_required_fields_default_values.items()
            if k not in message_dict
        }

    def _aggregated_list(
        self,
        request: compute.AggregatedListSubnetworksRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SubnetworkAggregatedList:
        r"""Call the aggregated list method over HTTP.

        Args:
            request (~.compute.AggregatedListSubnetworksRequest):
                The request object. A request message for
                Subnetworks.AggregatedList. See the
                method description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.SubnetworkAggregatedList:

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/aggregated/subnetworks",
            },
        ]

        request_kwargs = compute.AggregatedListSubnetworksRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.AggregatedListSubnetworksRequest.to_json(
                compute.AggregatedListSubnetworksRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(
            self._aggregated_list_get_unset_required_fields(query_params)
        )

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.SubnetworkAggregatedList.from_json(
            response.content, ignore_unknown_fields=True
        )

    __delete_required_fields_default_values = {
        "project": "",
        "region": "",
        "subnetwork": "",
    }

    @staticmethod
    def _delete_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__delete_required_fields_default_values.items()
            if k not in message_dict
        }

    def _delete(
        self,
        request: compute.DeleteSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteSubnetworkRequest):
                The request object. A request message for
                Subnetworks.Delete. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "delete",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{subnetwork}",
            },
        ]

        request_kwargs = compute.DeleteSubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.DeleteSubnetworkRequest.to_json(
                compute.DeleteSubnetworkRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(self._delete_get_unset_required_fields(query_params))

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    __expand_ip_cidr_range_required_fields_default_values = {
        "project": "",
        "region": "",
        "subnetwork": "",
    }

    @staticmethod
    def _expand_ip_cidr_range_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__expand_ip_cidr_range_required_fields_default_values.items()
            if k not in message_dict
        }

    def _expand_ip_cidr_range(
        self,
        request: compute.ExpandIpCidrRangeSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the expand ip cidr range method over HTTP.

        Args:
            request (~.compute.ExpandIpCidrRangeSubnetworkRequest):
                The request object. A request message for
                Subnetworks.ExpandIpCidrRange. See the
                method description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{subnetwork}/expandIpCidrRange",
                "body": "subnetworks_expand_ip_cidr_range_request_resource",
            },
        ]

        request_kwargs = compute.ExpandIpCidrRangeSubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.SubnetworksExpandIpCidrRangeRequest.to_json(
            compute.SubnetworksExpandIpCidrRangeRequest(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.ExpandIpCidrRangeSubnetworkRequest.to_json(
                compute.ExpandIpCidrRangeSubnetworkRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(
            self._expand_ip_cidr_range_get_unset_required_fields(query_params)
        )

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    __get_required_fields_default_values = {
        "project": "",
        "region": "",
        "subnetwork": "",
    }

    @staticmethod
    def _get_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__get_required_fields_default_values.items()
            if k not in message_dict
        }

    def _get(
        self,
        request: compute.GetSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Subnetwork:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetSubnetworkRequest):
                The request object. A request message for
                Subnetworks.Get. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Subnetwork:
                Represents a Subnetwork resource. A
                subnetwork (also known as a subnet) is a
                logical partition of a Virtual Private
                Cloud network with one primary IP range
                and zero or more secondary IP ranges.
                For more information, read Virtual
                Private Cloud (VPC) Network.

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{subnetwork}",
            },
        ]

        request_kwargs = compute.GetSubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.GetSubnetworkRequest.to_json(
                compute.GetSubnetworkRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(self._get_get_unset_required_fields(query_params))

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Subnetwork.from_json(
            response.content, ignore_unknown_fields=True
        )

    __get_iam_policy_required_fields_default_values = {
        "project": "",
        "region": "",
        "resource": "",
    }

    @staticmethod
    def _get_iam_policy_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__get_iam_policy_required_fields_default_values.items()
            if k not in message_dict
        }

    def _get_iam_policy(
        self,
        request: compute.GetIamPolicySubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Call the get iam policy method over HTTP.

        Args:
            request (~.compute.GetIamPolicySubnetworkRequest):
                The request object. A request message for
                Subnetworks.GetIamPolicy. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions; each ``role``
                can be an IAM predefined role or a user-created custom
                role. For some types of Google Cloud resources, a
                ``binding`` can also specify a ``condition``, which is a
                logical expression that allows access to a resource only
                if the expression evaluates to ``true``. A condition can
                add constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:** { "bindings": [ { "role":
                "roles/resourcemanager.organizationAdmin", "members": [
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                ] }, { "role":
                "roles/resourcemanager.organizationViewer", "members": [
                "user:eve@example.com" ], "condition": { "title":
                "expirable access", "description": "Does not grant
                access after Sep 2020", "expression": "request.time <
                timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag":
                "BwWWja0YfJA=", "version": 3 } **YAML example:**
                bindings: - members: - user:mike@example.com -
                group:admins@example.com - domain:google.com -
                serviceAccount:my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA=
                version: 3 For a description of IAM and its features,
                see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{resource}/getIamPolicy",
            },
        ]

        request_kwargs = compute.GetIamPolicySubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.GetIamPolicySubnetworkRequest.to_json(
                compute.GetIamPolicySubnetworkRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(
            self._get_iam_policy_get_unset_required_fields(query_params)
        )

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Policy.from_json(response.content, ignore_unknown_fields=True)

    __insert_required_fields_default_values = {
        "project": "",
        "region": "",
    }

    @staticmethod
    def _insert_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__insert_required_fields_default_values.items()
            if k not in message_dict
        }

    def _insert(
        self,
        request: compute.InsertSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertSubnetworkRequest):
                The request object. A request message for
                Subnetworks.Insert. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks",
                "body": "subnetwork_resource",
            },
        ]

        request_kwargs = compute.InsertSubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.Subnetwork.to_json(
            compute.Subnetwork(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.InsertSubnetworkRequest.to_json(
                compute.InsertSubnetworkRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(self._insert_get_unset_required_fields(query_params))

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    __list_required_fields_default_values = {
        "project": "",
        "region": "",
    }

    @staticmethod
    def _list_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__list_required_fields_default_values.items()
            if k not in message_dict
        }

    def _list(
        self,
        request: compute.ListSubnetworksRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SubnetworkList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListSubnetworksRequest):
                The request object. A request message for
                Subnetworks.List. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.SubnetworkList:
                Contains a list of Subnetwork
                resources.

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks",
            },
        ]

        request_kwargs = compute.ListSubnetworksRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.ListSubnetworksRequest.to_json(
                compute.ListSubnetworksRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(self._list_get_unset_required_fields(query_params))

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.SubnetworkList.from_json(
            response.content, ignore_unknown_fields=True
        )

    __list_usable_required_fields_default_values = {
        "project": "",
    }

    @staticmethod
    def _list_usable_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__list_usable_required_fields_default_values.items()
            if k not in message_dict
        }

    def _list_usable(
        self,
        request: compute.ListUsableSubnetworksRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.UsableSubnetworksAggregatedList:
        r"""Call the list usable method over HTTP.

        Args:
            request (~.compute.ListUsableSubnetworksRequest):
                The request object. A request message for
                Subnetworks.ListUsable. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.UsableSubnetworksAggregatedList:

        """

        http_options = [
            {
                "method": "get",
                "uri": "/compute/v1/projects/{project}/aggregated/subnetworks/listUsable",
            },
        ]

        request_kwargs = compute.ListUsableSubnetworksRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.ListUsableSubnetworksRequest.to_json(
                compute.ListUsableSubnetworksRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(self._list_usable_get_unset_required_fields(query_params))

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.UsableSubnetworksAggregatedList.from_json(
            response.content, ignore_unknown_fields=True
        )

    __patch_required_fields_default_values = {
        "project": "",
        "region": "",
        "subnetwork": "",
    }

    @staticmethod
    def _patch_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__patch_required_fields_default_values.items()
            if k not in message_dict
        }

    def _patch(
        self,
        request: compute.PatchSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the patch method over HTTP.

        Args:
            request (~.compute.PatchSubnetworkRequest):
                The request object. A request message for
                Subnetworks.Patch. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "patch",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{subnetwork}",
                "body": "subnetwork_resource",
            },
        ]

        request_kwargs = compute.PatchSubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.Subnetwork.to_json(
            compute.Subnetwork(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.PatchSubnetworkRequest.to_json(
                compute.PatchSubnetworkRequest(transcoded_request["query_params"]),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(self._patch_get_unset_required_fields(query_params))

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    __set_iam_policy_required_fields_default_values = {
        "project": "",
        "region": "",
        "resource": "",
    }

    @staticmethod
    def _set_iam_policy_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__set_iam_policy_required_fields_default_values.items()
            if k not in message_dict
        }

    def _set_iam_policy(
        self,
        request: compute.SetIamPolicySubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Policy:
        r"""Call the set iam policy method over HTTP.

        Args:
            request (~.compute.SetIamPolicySubnetworkRequest):
                The request object. A request message for
                Subnetworks.SetIamPolicy. See the method
                description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Policy:
                An Identity and Access Management (IAM) policy, which
                specifies access controls for Google Cloud resources. A
                ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions; each ``role``
                can be an IAM predefined role or a user-created custom
                role. For some types of Google Cloud resources, a
                ``binding`` can also specify a ``condition``, which is a
                logical expression that allows access to a resource only
                if the expression evaluates to ``true``. A condition can
                add constraints based on attributes of the request, the
                resource, or both. To learn which resources support
                conditions in their IAM policies, see the `IAM
                documentation <https://cloud.google.com/iam/help/conditions/resource-policies>`__.
                **JSON example:** { "bindings": [ { "role":
                "roles/resourcemanager.organizationAdmin", "members": [
                "user:mike@example.com", "group:admins@example.com",
                "domain:google.com",
                "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                ] }, { "role":
                "roles/resourcemanager.organizationViewer", "members": [
                "user:eve@example.com" ], "condition": { "title":
                "expirable access", "description": "Does not grant
                access after Sep 2020", "expression": "request.time <
                timestamp('2020-10-01T00:00:00.000Z')", } } ], "etag":
                "BwWWja0YfJA=", "version": 3 } **YAML example:**
                bindings: - members: - user:mike@example.com -
                group:admins@example.com - domain:google.com -
                serviceAccount:my-project-id@appspot.gserviceaccount.com
                role: roles/resourcemanager.organizationAdmin - members:
                - user:eve@example.com role:
                roles/resourcemanager.organizationViewer condition:
                title: expirable access description: Does not grant
                access after Sep 2020 expression: request.time <
                timestamp('2020-10-01T00:00:00.000Z') etag: BwWWja0YfJA=
                version: 3 For a description of IAM and its features,
                see the `IAM
                documentation <https://cloud.google.com/iam/docs/>`__.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{resource}/setIamPolicy",
                "body": "region_set_policy_request_resource",
            },
        ]

        request_kwargs = compute.SetIamPolicySubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.RegionSetPolicyRequest.to_json(
            compute.RegionSetPolicyRequest(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.SetIamPolicySubnetworkRequest.to_json(
                compute.SetIamPolicySubnetworkRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(
            self._set_iam_policy_get_unset_required_fields(query_params)
        )

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Policy.from_json(response.content, ignore_unknown_fields=True)

    __set_private_ip_google_access_required_fields_default_values = {
        "project": "",
        "region": "",
        "subnetwork": "",
    }

    @staticmethod
    def _set_private_ip_google_access_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__set_private_ip_google_access_required_fields_default_values.items()
            if k not in message_dict
        }

    def _set_private_ip_google_access(
        self,
        request: compute.SetPrivateIpGoogleAccessSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the set private ip google
        access method over HTTP.

        Args:
            request (~.compute.SetPrivateIpGoogleAccessSubnetworkRequest):
                The request object. A request message for
                Subnetworks.SetPrivateIpGoogleAccess.
                See the method description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/v1/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/v1/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/v1/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zonalOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{subnetwork}/setPrivateIpGoogleAccess",
                "body": "subnetworks_set_private_ip_google_access_request_resource",
            },
        ]

        request_kwargs = compute.SetPrivateIpGoogleAccessSubnetworkRequest.to_dict(
            request
        )
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.SubnetworksSetPrivateIpGoogleAccessRequest.to_json(
            compute.SubnetworksSetPrivateIpGoogleAccessRequest(
                transcoded_request["body"]
            ),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.SetPrivateIpGoogleAccessSubnetworkRequest.to_json(
                compute.SetPrivateIpGoogleAccessSubnetworkRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(
            self._set_private_ip_google_access_get_unset_required_fields(query_params)
        )

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    __test_iam_permissions_required_fields_default_values = {
        "project": "",
        "region": "",
        "resource": "",
    }

    @staticmethod
    def _test_iam_permissions_get_unset_required_fields(message_dict):
        return {
            k: v
            for k, v in SubnetworksRestTransport.__test_iam_permissions_required_fields_default_values.items()
            if k not in message_dict
        }

    def _test_iam_permissions(
        self,
        request: compute.TestIamPermissionsSubnetworkRequest,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.TestPermissionsResponse:
        r"""Call the test iam permissions method over HTTP.

        Args:
            request (~.compute.TestIamPermissionsSubnetworkRequest):
                The request object. A request message for
                Subnetworks.TestIamPermissions. See the
                method description for details.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.TestPermissionsResponse:

        """

        http_options = [
            {
                "method": "post",
                "uri": "/compute/v1/projects/{project}/regions/{region}/subnetworks/{resource}/testIamPermissions",
                "body": "test_permissions_request_resource",
            },
        ]

        request_kwargs = compute.TestIamPermissionsSubnetworkRequest.to_dict(request)
        transcoded_request = path_template.transcode(http_options, **request_kwargs)

        # Jsonify the request body
        body = compute.TestPermissionsRequest.to_json(
            compute.TestPermissionsRequest(transcoded_request["body"]),
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
        uri = transcoded_request["uri"]
        method = transcoded_request["method"]

        # Jsonify the query params
        query_params = json.loads(
            compute.TestIamPermissionsSubnetworkRequest.to_json(
                compute.TestIamPermissionsSubnetworkRequest(
                    transcoded_request["query_params"]
                ),
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
        )

        query_params.update(
            self._test_iam_permissions_get_unset_required_fields(query_params)
        )

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = getattr(self._session, method)(
            # Replace with proper schema configuration (http/https) logic
            "https://{host}{uri}".format(host=self._host, uri=uri),
            timeout=timeout,
            headers=headers,
            params=rest_helpers.flatten_query_params(query_params),
            data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.TestPermissionsResponse.from_json(
            response.content, ignore_unknown_fields=True
        )

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListSubnetworksRequest], compute.SubnetworkAggregatedList
    ]:
        return self._aggregated_list

    @property
    def delete(self) -> Callable[[compute.DeleteSubnetworkRequest], compute.Operation]:
        return self._delete

    @property
    def expand_ip_cidr_range(
        self,
    ) -> Callable[[compute.ExpandIpCidrRangeSubnetworkRequest], compute.Operation]:
        return self._expand_ip_cidr_range

    @property
    def get(self) -> Callable[[compute.GetSubnetworkRequest], compute.Subnetwork]:
        return self._get

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[compute.GetIamPolicySubnetworkRequest], compute.Policy]:
        return self._get_iam_policy

    @property
    def insert(self) -> Callable[[compute.InsertSubnetworkRequest], compute.Operation]:
        return self._insert

    @property
    def list(
        self,
    ) -> Callable[[compute.ListSubnetworksRequest], compute.SubnetworkList]:
        return self._list

    @property
    def list_usable(
        self,
    ) -> Callable[
        [compute.ListUsableSubnetworksRequest], compute.UsableSubnetworksAggregatedList
    ]:
        return self._list_usable

    @property
    def patch(self) -> Callable[[compute.PatchSubnetworkRequest], compute.Operation]:
        return self._patch

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[compute.SetIamPolicySubnetworkRequest], compute.Policy]:
        return self._set_iam_policy

    @property
    def set_private_ip_google_access(
        self,
    ) -> Callable[
        [compute.SetPrivateIpGoogleAccessSubnetworkRequest], compute.Operation
    ]:
        return self._set_private_ip_google_access

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsSubnetworkRequest], compute.TestPermissionsResponse
    ]:
        return self._test_iam_permissions

    def close(self):
        self._session.close()


__all__ = ("SubnetworksRestTransport",)
