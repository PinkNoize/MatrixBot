import command

def getbuiltins():
    builtins=[]

    def help(args,env):
        if(len(args)>1):
            if(args[1] in env['commands']):
                return (env['commands'][args[1]].help_message , 0)
            else:
                return ("command "+args[1]+" not found",0)
        else:
            helpmessage=""
            for name,cmd in env['commands'].items():
                helpmessage+=name+'\n'
                helpmessage+=cmd.help_message+'\n'
            return (helpmessage,0)
                

    builtins.append(command.command("help",
        ("Usage: help [command]\n"
        "Displays the specified command's help message.\n"),
        help))

    def killbot(args,env):
        return ("Exiting...",1)

    builtins.append(command.command("killbot",
        ("Usage: killbot\n"
        "Kills the bot\n"),
        killbot))

    return builtins
