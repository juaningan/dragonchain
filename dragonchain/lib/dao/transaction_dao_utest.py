# Copyright 2020 Dragonchain, Inc.
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#      6. Trademarks. This License does not grant permission to use the trade
#         names, trademarks, service marks, or product names of the Licensor
#         and its affiliates, except as required to comply with Section 4(c) of
#         the License and to reproduce the content of the NOTICE file.
# You may obtain a copy of the Apache License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.

import unittest
from unittest.mock import patch, MagicMock, call

from dragonchain import test_env  # noqa: F401
from dragonchain.lib.dao import transaction_dao


class TestStoreFullTxns(unittest.TestCase):
    @patch("dragonchain.lib.interfaces.storage.put")
    @patch("dragonchain.lib.database.redisearch.put_many_documents")
    def test_store_full_txns_calls_redis_a_lot(self, mock_index_many, mock_put):
        mock_block = MagicMock(block_id="banana", transactions=[MagicMock(txn_id="apple", block_id="banana", txn_type="fruity")])
        transaction_dao.store_full_txns(mock_block)
        mock_index_many.assert_has_calls(
            [
                call("tx", {"txn-apple": {"block_id": "banana"}}, upsert=True),
                call("fruity", {"apple": mock_block.transactions[0].export_as_search_index.return_value}, upsert=True),
            ]
        )
