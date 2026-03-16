class CredentialGuard:
    def allow(self, action: str) -> bool:
        return False if action == "dump_credentials" else True
