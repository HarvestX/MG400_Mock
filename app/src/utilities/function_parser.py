"""Function Parser."""

import re as regex


class FunctionParser:
    """FunctionParser"""
    @staticmethod
    def exec(command_class, command: str):
        """exec"""
        function_name = regex.match(r"\s*[a-zA-Z0-9_]+(?=(\s*\(.*\)))", command)

        if not function_name:
            raise ValueError("Invalid command: " + command)

        function_name_str = function_name.group()

        args_str = (
            command.replace(function_name_str, "").strip().lstrip(
                "(").rstrip(")")
        )
        args = args_str.split(",")

        try:
            function = getattr(command_class, function_name_str)
            res = function(args)

            return res

        except AttributeError as err:
            raise ValueError("Not found a function: " + str(err)) from err
