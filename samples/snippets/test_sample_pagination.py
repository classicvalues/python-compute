# Copyright 2021 Google LLC
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
import typing

from sample_pagination import print_images_list, print_images_list_by_page

PROJECT = "windows-sql-cloud"


def test_pagination(capsys: typing.Any) -> None:
    print_images_list(PROJECT)
    out, _ = capsys.readouterr()
    assert len(out.splitlines()) > 2


def test_pagination_page(capsys: typing.Any) -> None:
    print_images_list_by_page(PROJECT, 2)
    out, _ = capsys.readouterr()
    assert "Page 2" in out
