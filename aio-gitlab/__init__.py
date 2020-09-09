import gitlab
from .aio_gitlab import AioGitlab


class Gitlab(gitlab.Gitlab):
    def __init__(
            self,
            url,
            private_token,
            oauth_token=None,
            ssl_verify=True,
            http_username=None,
            http_password=None,
            timeout=None,
            api_version="4",
            session=None,
            per_page=None,
    ):
        self.aio = AioGitlab(gl=self, gitlab_url=url, gitlab_token=private_token)
        super(Gitlab, self).__init__(
            url=url,
            private_token=private_token,
            oauth_token=oauth_token,
            ssl_verify=ssl_verify,
            http_username=http_username,
            http_password=http_password,
            timeout=timeout,
            api_version=api_version,
            session=session,
            per_page=per_page,
        )
