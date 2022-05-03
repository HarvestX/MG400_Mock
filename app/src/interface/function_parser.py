import re as regex

class FunctionParesr:

    @staticmethod
    def exec(command_class, command: str):
        function_name = regex.match(r'\s*[a-zA-Z]+(?=(\s*\(.*\)))', command)

        if not function_name:
            raise ValueError('Invalid command: ' + command)

        function_name_str = function_name.group()

        args_str = command.replace(function_name_str, '').strip().lstrip('(').rstrip(')')
        args = args_str.split(',')

        try:
            function = getattr(command_class, function_name_str)

            function(args)
        except AttributeError as err:
            raise ValueError('Not found a function: ' + err)
