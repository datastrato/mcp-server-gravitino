# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
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
