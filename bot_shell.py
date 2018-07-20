import bot_shell_builtins

class bot_shell:

    """Attributes: 
        commands - Dict of command objects
    """
    def __init__(self,custom_commands):
        self.commands={}
        self.env={} #env for command use
        self.env['commands']=self.commands
        built=bot_shell_builtins.getbuiltins()
        for cmd in built:
            self.commands[cmd.name]=cmd
        for cmd in custom_commands:
            #Overwriting builtins permitted
            self.commands[cmd.name]=cmd

    def process(self,command):
        args=command[0].split()
        if args[0] in self.commands:
            print("Executing command: "+args[0])
            return self.commands[ args[0] ].function(args,self.env)
        else:
            return (("shell: "+args[0]+": command not found"),0)
