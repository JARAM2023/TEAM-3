from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseSettings, Field


class AppSettings(BaseSettings):
    LOGGING_DEBUG_LEVEL: bool = Field(
        default=True,
        description="True: DEBUG mode, False:: INFO mode",
    )

    DEBUG_ALLOW_CORS_ALL_ORIGIN: bool = Field(
        default=True,
        description="If True, allow origins for CORS requests.",
    )
    DEBUG_ALLOW_NON_CERTIFICATED_USER_GET_TOKEN: bool = Field(
        default=True,
        description="If True, allow non-cerficiated users to get ESP token.",
    )

    THREAD_POOL_SIZE: Optional[int] = Field(
        default=10,
        description="Change the server's thread pool size to handle non-async function",
    )

    SECRET_KEY: str = Field(
        default="example_secret_key_WoW",
        description="Secret key to be used for issuing HMAC tokens.",
    )

    DATABASE_URI: AnyUrl = Field(
        default="postgresql+psycopg2://team3:devpassword@127.0.0.1:35000/team3",
        description="PosstgreSQL connection URI.",
    )
    DATABASE_OPTIONS: Dict[str, Any] = Field(
        default={
            "connect_args": {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 15,
            },
            "pool_pre_ping": True,
            "pool_recycle": 15 * 60,
            "pool_size": 50,
            "max_overflow": 50,
            "pool_use_lifo": True,
        },
        description="PosstgreSQL option to create a connection.",
    )

    class Config:
        env_file = ".env"
        env_prefix = "app_"


app_settings: AppSettings = AppSettings()
