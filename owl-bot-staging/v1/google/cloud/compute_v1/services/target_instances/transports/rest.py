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
import dataclasses
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.compute_v1.types import compute

from .base import TargetInstancesTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)

@dataclasses.dataclass
class TargetInstancesRestStub:
    _session: AuthorizedSession
    _host: str

class TargetInstancesRestTransport(TargetInstancesTransport):
    """REST backend transport for TargetInstances.

    The TargetInstances API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """
    _STUBS: Dict[str, TargetInstancesRestStub] = {}

    def __init__(self, *,
            host: str = 'compute.googleapis.com',
            credentials: ga_credentials.Credentials=None,
            credentials_file: str=None,
            scopes: Sequence[str]=None,
            client_cert_source_for_mtls: Callable[[
                ], Tuple[bytes, bytes]]=None,
            quota_project_id: Optional[str]=None,
            client_info: gapic_v1.client_info.ClientInfo=DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool]=False,
            url_scheme: str='https',
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
                Generally, you only need to set this if you are developing
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
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    class _AggregatedList(TargetInstancesRestStub):
        def __hash__(self):
            return hash("AggregatedList")

        __REQUIRED_FIELDS_DEFAULT_VALUES =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.AggregatedListTargetInstancesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.TargetInstanceAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListTargetInstancesRequest):
                    The request object. A request message for
                TargetInstances.AggregatedList. See the
                method description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetInstanceAggregatedList:

            """

            http_options = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/aggregated/targetInstances',
            },
            ]

            request_kwargs = compute.AggregatedListTargetInstancesRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.AggregatedListTargetInstancesRequest.to_json(
                compute.AggregatedListTargetInstancesRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            return compute.TargetInstanceAggregatedList.from_json(
                response.content,
                ignore_unknown_fields=True
            )

    class _Delete(TargetInstancesRestStub):
        def __hash__(self):
            return hash("Delete")

        __REQUIRED_FIELDS_DEFAULT_VALUES =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.DeleteTargetInstanceRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteTargetInstanceRequest):
                    The request object. A request message for
                TargetInstances.Delete. See the method
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

            http_options = [{
                'method': 'delete',
                'uri': '/compute/v1/projects/{project}/zones/{zone}/targetInstances/{target_instance}',
            },
            ]

            request_kwargs = compute.DeleteTargetInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.DeleteTargetInstanceRequest.to_json(
                compute.DeleteTargetInstanceRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            return compute.Operation.from_json(
                response.content,
                ignore_unknown_fields=True
            )

    class _Get(TargetInstancesRestStub):
        def __hash__(self):
            return hash("Get")

        __REQUIRED_FIELDS_DEFAULT_VALUES =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.GetTargetInstanceRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.TargetInstance:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetTargetInstanceRequest):
                    The request object. A request message for
                TargetInstances.Get. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetInstance:
                    Represents a Target Instance
                resource. You can use a target instance
                to handle traffic for one or more
                forwarding rules, which is ideal for
                forwarding protocol traffic that is
                managed by a single source. For example,
                ESP, AH, TCP, or UDP. For more
                information, read Target instances.

            """

            http_options = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/zones/{zone}/targetInstances/{target_instance}',
            },
            ]

            request_kwargs = compute.GetTargetInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.GetTargetInstanceRequest.to_json(
                compute.GetTargetInstanceRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            return compute.TargetInstance.from_json(
                response.content,
                ignore_unknown_fields=True
            )

    class _Insert(TargetInstancesRestStub):
        def __hash__(self):
            return hash("Insert")

        __REQUIRED_FIELDS_DEFAULT_VALUES =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.InsertTargetInstanceRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertTargetInstanceRequest):
                    The request object. A request message for
                TargetInstances.Insert. See the method
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

            http_options = [{
                'method': 'post',
                'uri': '/compute/v1/projects/{project}/zones/{zone}/targetInstances',
                'body': 'target_instance_resource',
            },
            ]

            request_kwargs = compute.InsertTargetInstanceRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            # Jsonify the request body
            body = compute.TargetInstance.to_json(
                compute.TargetInstance(transcoded_request['body']),                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.InsertTargetInstanceRequest.to_json(
                compute.InsertTargetInstanceRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            return compute.Operation.from_json(
                response.content,
                ignore_unknown_fields=True
            )

    class _List(TargetInstancesRestStub):
        def __hash__(self):
            return hash("List")

        __REQUIRED_FIELDS_DEFAULT_VALUES =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: compute.ListTargetInstancesRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: float=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> compute.TargetInstanceList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListTargetInstancesRequest):
                    The request object. A request message for
                TargetInstances.List. See the method
                description for details.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.compute.TargetInstanceList:
                    Contains a list of TargetInstance
                resources.

            """

            http_options = [{
                'method': 'get',
                'uri': '/compute/v1/projects/{project}/zones/{zone}/targetInstances',
            },
            ]

            request_kwargs = compute.ListTargetInstancesRequest.to_dict(request)
            transcoded_request = path_template.transcode(
                http_options, **request_kwargs)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(compute.ListTargetInstancesRequest.to_json(
                compute.ListTargetInstancesRequest(transcoded_request['query_params']),
                including_default_value_fields=False,
                use_integers_for_enums=False
            ))

            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
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
            return compute.TargetInstanceList.from_json(
                response.content,
                ignore_unknown_fields=True
            )

    @property
    def aggregated_list(self) -> Callable[
            [compute.AggregatedListTargetInstancesRequest],
            compute.TargetInstanceAggregatedList]:
        stub = self._STUBS.get("aggregated_list")
        if not stub:
            stub = self._STUBS["aggregated_list"] = self._AggregatedList(self._session, self._host)

        return stub

    @property
    def delete(self) -> Callable[
            [compute.DeleteTargetInstanceRequest],
            compute.Operation]:
        stub = self._STUBS.get("delete")
        if not stub:
            stub = self._STUBS["delete"] = self._Delete(self._session, self._host)

        return stub

    @property
    def get(self) -> Callable[
            [compute.GetTargetInstanceRequest],
            compute.TargetInstance]:
        stub = self._STUBS.get("get")
        if not stub:
            stub = self._STUBS["get"] = self._Get(self._session, self._host)

        return stub

    @property
    def insert(self) -> Callable[
            [compute.InsertTargetInstanceRequest],
            compute.Operation]:
        stub = self._STUBS.get("insert")
        if not stub:
            stub = self._STUBS["insert"] = self._Insert(self._session, self._host)

        return stub

    @property
    def list(self) -> Callable[
            [compute.ListTargetInstancesRequest],
            compute.TargetInstanceList]:
        stub = self._STUBS.get("list")
        if not stub:
            stub = self._STUBS["list"] = self._List(self._session, self._host)

        return stub

    def close(self):
        self._session.close()


__all__=(
    'TargetInstancesRestTransport',
)
