# Babysitter Agent
School project for learn about intelligent agents theory

## Description
The full project description is located in `doc/proyecto-agentes.pdf`.

## Requierments
This project was developed using `Python >= 3.7.4` and has not any extra dependencies. Then if you need to install python check the oficial [site](https://www.python.org/downloads/)

## Execution
First of all there are three modes of execution. You can see the three of time listed typing:
```bash
python main.py
```
If you want to use the `config` mode, you need a configuration file with the below content:
```
[env]
rows    = 7        # -n or --rows
columns = 8        # -m or --columns
babies  = 6        # -b or --babies
toys    = 20       # -o or --toys
dirty   = 40       # -d or --dirty
time    = 20       # -t or --time
name    = house    # -env or --env
cicles  = 100      # -c or --cicles

[robot]
name = reactive    # -bot or --robot

[log]
level = info       # -lvl or --level
file  = custom.log # -f or --file 

[app]
repetitions = 30   # -rep or --repetitions
```
You can change every value listed above to run different simulations. Also every configuration variable has a relative command line argument in the `cmd` mode. The mentioned relations are also showed in the above file using the inline comments.

> Everything that follow a `#` symbol will be interpreted as comments.

To read about the meaning of each argument, see the `cmd` inline help by typing:
```bash
python main.py cmd -h
```
Once you are ready to run the app type:
```bash
python main.py config -p <your-configuration-file-path>
```
Or in case of use the `cmd` mode:
```bash
python main.py cmd 12 <your-custom-arguments>
```
Optionally if you use the project `config.ini` file you can use:
```bash
make config
```
And for any configuration saved on the `configurations/` folder:
```bash
make load LABEL=<configuration-name>
```

## Customization
You can add custom agents and enviroments by implementing `Agent` and `Enviroment` respectively. To see the content of this classes check the files `src/agent/base_agent.py` and `src/enviroment/base_env.py`.

Once you have your implementation you need to register them in the appropiate module `__init__.py` file. Simply add your robots to the `robots` list in  `src/agent/__init__.py`, and add your enviroments to the `envs` list in  `src/enviroments/__init__.py`. When you are done, check that your implementations are correctly added typing:
```bash
python main.py info
```
or 
```bash
make info
```