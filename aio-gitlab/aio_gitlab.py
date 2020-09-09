import io
import json
import asyncio
import gitlab.v4.objects as gl_objects
import urllib.parse
from aiohttp import ClientSession


class AioGitlab(object):
    def __init__(self, gl, gitlab_url, gitlab_token):
        self._gitlab_url = gitlab_url
        self._gitlab_token = gitlab_token
        self._gl = gl

    def get_project_jobs(self, project, **kwargs):
        resources = {"projects": True, "project_id": project.id, "jobs": True}
        objects = get_gl_objects(self._gl, gl_objects.ProjectJob, gl_objects.ProjectJobManager, self._gitlab_url,
                                 self._gitlab_token, resources, project, **kwargs)
        return objects

    def get_project_commits(self, project, **kwargs):
        resources = {"projects": True, "project_id": project.id, "commits": True}
        objects = get_gl_objects(self._gl, gl_objects.ProjectCommit, gl_objects.ProjectCommitManager, self._gitlab_url,
                                 self._gitlab_token, resources, project, **kwargs)
        return objects

    def get_groups(self, **kwargs):
        resources = {"groups": True}
        objects = get_gl_objects(self._gl, gl_objects.Group, gl_objects.GroupManager, self._gitlab_url,
                                 self._gitlab_token, resources, **kwargs)
        return objects

    def get_issues(self, **kwargs):
        resources = {"issues": True}
        objects = get_gl_objects(self._gl, gl_objects.Issue, gl_objects.IssueManager, self._gitlab_url,
                                 self._gitlab_token, resources, **kwargs)
        return objects

    def get_project_issues(self, project, **kwargs):
        resources = {"projects": True, "project_id": project.id, "issues": True}
        objects = get_gl_objects(self._gl, gl_objects.ProjectIssue, gl_objects.ProjectIssueManager, self._gitlab_url,
                                 self._gitlab_token, resources, project, **kwargs)
        return objects

    def get_project_pipelines(self, project, **kwargs):
        resources = {"projects": True, "project_id": project.id, "pipelines": True}
        objects = get_gl_objects(self._gl, gl_objects.ProjectPipeline, gl_objects.ProjectPipelineManager,
                                 self._gitlab_url,
                                 self._gitlab_token, resources, project, **kwargs)
        return objects


def build_url(gitlab_url, resources, **kwargs):
    projects = "/projects" if resources.get("projects") else ""
    project_id = f"/{resources.get('project_id')}" if resources.get("project_id") else ""
    jobs = "/jobs" if resources.get("jobs") else ""
    job_id = f"/{resources.get('job_id')}" if resources.get("job_id") else ""
    commits = "/repository/commits" if resources.get("commits") else ""
    branches = "/repository/branches" if resources.get("branches") else ""
    issues = "/issues" if resources.get("issues") else ""
    groups = "/groups" if resources.get("groups") else ""
    group_id = f"/{resources.get('group_id')}" if resources.get("group_id") else ""
    pipelines = "/pipelines" if resources.get("pipelines") else ""
    url = f"{gitlab_url}/api/v4" \
          f"{groups}" \
          f"{group_id}" \
          f"{projects}" \
          f"{project_id}" \
          f"{issues}" \
          f"{branches}" \
          f"{commits}" \
          f"{pipelines}" \
          f"{jobs}" \
          f"{job_id}"

    parameters = f"{urllib.parse.urlencode(kwargs)}"

    return f"{url}?{parameters}" if parameters else url


async def send_req(url, headers, session):
    async with session.get(url, headers=headers) as response:
        return await response.read()


async def reqs_batch(gitlab_url, gitlab_token, current_page, objects, resources, reqs_per_run=10, **kwargs):
    async with ClientSession() as session:
        futures = []
        for i in range(current_page, current_page + reqs_per_run):
            url = build_url(gitlab_url, resources, page=i, per_page=100, **kwargs)
            headers = {"PRIVATE-TOKEN": gitlab_token}
            future = asyncio.ensure_future(send_req(url=url, session=session, headers=headers))
            futures.append(future)
        responses = await asyncio.gather(*futures)
        for response in responses:
            resp_objects = json.load(io.BytesIO(response))
            for _object in resp_objects:
                objects.append(_object)


def fetch(gitlab_url, gitlab_token, resources, reqs_per_run=10, **kwargs):
    objects = []
    more_objs_to_fetch = True
    current_page = 1
    while more_objs_to_fetch:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(
            reqs_batch(gitlab_url, gitlab_token, current_page, objects, resources, reqs_per_run, **kwargs))
        loop.run_until_complete(future)

        if len(objects) == ((current_page + reqs_per_run - 1) * 100):
            current_page += reqs_per_run
        else:
            more_objs_to_fetch = False

    return objects


def get_gl_objects(gl, gl_obj_class, gl_obj_mgr_class, gitlab_url, gitlab_token, resources, gl_obj_mgr_parent=None,
                   reqs_per_run=10, **kwargs):
    objects = []
    resp_objects = fetch(gitlab_url, gitlab_token, resources, reqs_per_run, **kwargs)
    manager = gl_obj_mgr_class(gl=gl, parent=gl_obj_mgr_parent)
    for _object in resp_objects:
        objects.append(gl_obj_class(manager=manager, attrs=_object))

    return objects
