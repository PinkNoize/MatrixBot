# MatrixBot
### Execute user-defined functions remotely over the [Matrix](https://www.matrix.org) network
### Basically C2 over [Matrix](https://www.matrix.org)
### Use setup.py to set up bot config (homeserver in form https://matrix.org)
## Adding Custom Commands
### Either add commands to builtins or define them in bot.py and add it to 'commands' in __init__()
#### Ex.
####
```python
def foo(args,env):
	#do stuff
commands.append(command.command("keyword","Help Message\n",foo))
```

### No longer maintained/developed, may someday be rewritten in Rust
