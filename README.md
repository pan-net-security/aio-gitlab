aio-gitlab
===============

`aio-gitlab` is Python package which allows for faster fetching of resources from Gitlab API utilizing asyncio.

## Why?

`python-gitlab` package provides access to Gitlab API and allows for working with its resources in Python.

One of the shortcomings of `python-gitlab` package is that when fetching resources, it's doing so by only sending requests sequentially and waiting for response before sending the next request. This starts to become a problem when fetching larger amounts of resources, as as it can take significant amount of time just to get even rudimentary information about them.

Another problem that this package is trying to solve is dropped connections after 100 pages of paginated content. This may or may not be a problem when using different versions of `python-gitlab` package.

`aio-gitlab` allows users to fetch resources faster by making requests to Gitlab API asynchronous. This can significantly improve performance when working with large amounts of Gitlab resources.

## Installation

```sh
pip install aio-gitlab
```
or
```sh
pip install git+github.com/pan-net-security/aio-gitlab
```

## Usage

`aio-gitlab` package contains `Gitlab` class, which extends `gitlab.Gitlab` class from `python-gitlab` package. Its `aio` attribute contains methods that return resources in form of corresponding objects from `gitlab.v4.objects` module.

Currently supported resources:
- Project Jobs
- Project Commits
- Project Pipelines
- Project Issues
- Groups
- Issues

As of now, `aio-gitlab` only supports authentication via Gitlab access token, username & password auth will not work!

### Example

```python
# Get all jobs from a certain project
import aio_gitlab
import os

# instead of
# gl = gitlab.Gitlab("https://gitlab.com", os.getenv("GITLAB_TOKEN")
gl = aio_gitlab.Gitlab("https://gitlab.com", os.getenv("GITLAB_TOKEN"))
project = gl.projects.get(os.getenv("PROJECT_ID"))

# instead of
# jobs = project.jobs.list(all=True)
project_jobs = gl.aio.get_project_jobs(project)
```
Other attributes for resources that are currently supported by [Gitlab API](https://docs.gitlab.om/ee/api/README.html) are possible to pass via `**kwargs` to the function calls.
