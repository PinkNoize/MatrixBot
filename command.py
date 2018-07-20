class command:
    
    """Attributes:
            name - string
            help_message - string
            function - function(args,...)
    """
    def __init__(self,name,help_message,function):
        self.name=name
        self.help_message=help_message
        self.function=function

    def help(self):
        return help_message


