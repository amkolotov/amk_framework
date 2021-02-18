from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
import os


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: имя папки с шаблонами
    :param kwargs: аргументы
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
