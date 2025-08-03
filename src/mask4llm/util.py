import json

from mask4llm.widgets.copy_on_enter_log import CopyOnEnterLog


def pipe_str(input: str) -> str:
    input_list = input.split(",")
    return "|".join(list(map(str.strip, input_list)))


def display_dict_in_json_format(
    log_widget: CopyOnEnterLog, data: dict[str, str]
) -> None:
    json_str = json.dumps(data, indent=2)
    for line in json_str.splitlines():
        _ = log_widget.write_line(line)
