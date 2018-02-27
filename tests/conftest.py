import os
import py
import pytest
import time

from lektor.project import Project
from lektor.environment import Environment

from lektor_markdown_header_anchors import MarkdownHeaderAnchorsPlugin


def pytest_generate_tests(metafunc):
    if 'project' in metafunc.fixturenames:
        cwd = os.path.dirname(__file__) 
        metafunc.parametrize(
            "project_path", [
                os.path.join(cwd, 'demo-project'),
                os.path.join(cwd, 'demo-project-random'),
            ], indirect=True)


@pytest.fixture(scope='function')
def project_path(request):
    return request.param


@pytest.fixture(scope='function')
def project(project_path):
    return Project.from_path(project_path, 'demo-project')


@pytest.fixture(scope='function')
def env(project):
    return Environment(project)


@pytest.fixture
def plugin(env):
    return MarkdownHeaderAnchorsPlugin(env, "markdown-header-anchors")
