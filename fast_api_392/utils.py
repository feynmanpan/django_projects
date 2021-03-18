from os import path
import config


def static_makeornot(fn_static: str, fn_temp: str, context: dict):
    html_path_relative = path.join(config.static_html, fn_static)
    html_path_absolute = path.join(config.templates, html_path_relative)
    #
    if not path.exists(html_path_absolute):
        print(f'不存在，重造靜態檔: {html_path_absolute}')
        response = config.jinja_templates.TemplateResponse(fn_temp, context)
        with open(html_path_absolute, 'w') as f:
            f.write(response.body.decode('utf-8'))
    else:
        print(f'存在，直接回應靜態檔: {html_path_absolute}')
        response = config.jinja_templates.TemplateResponse(html_path_relative, context)
    #
    return response


class MSG:
    count = 0

    @classmethod
    def printmsg(cls, msg):
        cls.count += 1
        print(f'{cls.count}. {msg}')

    @classmethod
    def prt_msgs(cls, msgs: list):
        for msg in msgs:
            cls.printmsg(msg)
