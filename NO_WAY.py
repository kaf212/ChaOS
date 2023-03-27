def echo(cmd):
    print(cmd[1])


def print_loop(cmd):
    for i in range(int(cmd[2])):
        print(cmd[1])


cmd = input('cmd > ')
cmd = cmd.split()

if cmd[0] == 'echo':
    echo(cmd)
elif cmd[0] == 'print_loop':
    print_loop(cmd)

cmd_map = {'echo': echo,
           'pr_lp': lambda pr_lp: pr_lp(cmd) if 2 == 2 else print('acces not granted. ')
           }

cmd_map[cmd[0]](cmd)



