#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pprint
from collections import defaultdict
from functools import reduce


# <INGREDIENT test_ingredient1>
def some_function(a: int, b: str) -> defaultdict:
    """
    Do something with a and b that will give a defaultdict.
    """
    out = defaultdict(int)
    for letter in b:
        out[letter] += a * ord(letter) + reduce(lambda x, y: x+ord(y), b, 0)
    pprint.pprint(out)
    return out
# </INGREDIENT>\
