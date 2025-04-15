# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # gravitino settings
    uri: str

    # one of basic auth or jwt token should be provided
    username: Optional[str] = None
    password: Optional[str] = None
    jwt_token: Optional[str] = None

    # mcp settings
    active_tools: Optional[str] = "*"  # comma separated tools to mount

    model_config = SettingsConfigDict(env_prefix="GRAVITINO_")

    @model_validator(mode="after")
    def validate_auth(self):
        if self.username and self.password:
            return self
        if self.jwt_token:
            return self
        raise ValueError("one of basic auth or jwt token should be provided")

    @property
    def authorization(self) -> dict:
        if self.username and self.password:
            return {"Authorization": f"Basic {self.username}:{self.password}"}
        if self.jwt_token:
            return {"Authorization": f"Bearer {self.jwt_token}"}
        raise ValueError("one of basic auth or jwt token should be provided")
