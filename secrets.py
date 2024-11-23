import secrets
import os

secrec_key = os.getenv(secrets.token_hex(16))

banco_projetest = "postgresql://banco_projetest_user:rnOtFlEYSJcFvCRqswUGGdsL1hsEtQOh@dpg-ct0aba5umphs73f34s3g-a.oregon-postgres.render.com/banco_projetest"