__author__ = 'zlu'

from jinja2 import Environment, FileSystemLoader
import os
import webbrowser


class GraphHtmlGenerator(object):
    template_path = ''

    def __init__(self, template_folder, template_name):
        self.template_folder = template_folder
        self.template_name = template_name

    def generate_html_with_json(self, price_json_data, graph_setup_data, export_path):
        # Create the jinja2 environment.
        # Notice the use of trim_blocks, which greatly helps control whitespace.
        env = Environment(loader=FileSystemLoader(self.template_folder), trim_blocks=True)
        template = env.get_template(self.template_name)
        result_html = template.render(PRICE_DATA=price_json_data, GRAPH_SETUP_DATA=graph_setup_data)
        GraphHtmlGenerator._save_html(export_path, result_html)
        # webbrowser.open('file://' + os.path.realpath(export_path))

    def generate_html_with_json(self, price_json_data, graph_setup_data, graph_global_setup, export_path):
        # Create the jinja2 environment.
        # Notice the use of trim_blocks, which greatly helps control whitespace.
        env = Environment(loader=FileSystemLoader(self.template_folder), trim_blocks=True)
        template = env.get_template(self.template_name)
        result_html = template.render(PRICE_DATA=price_json_data, GRAPH_SETUP_DATA=graph_setup_data, GRAPH_GLOBAL_SETUP=graph_global_setup)
        GraphHtmlGenerator._save_html(export_path, result_html)

    @staticmethod
    def _save_html(file_name, result_html):
        with open(file_name, "w") as text_file:
            text_file.write(result_html)
