# LEI



## Install

```sh
mkdir $nome_projeto
cd $nome_projeto
mkdir src local  filestore logs
git clone -b 14.0 --single-branch --depth 1 https://github.com/odoo/odoo.git src/odoo
env/bin/pip3 install -r src/odoo/requirements.txt
git clone https://github.com/Joao-Parente/LEI.git 

```

## Run

### First time:
```sh
src/odoo/odoo-bin -d odoov2  --db-filter=odoov2$ --stop-after-init --save -c ./config.cfg --addons-path=src/odoo/odoo/addons,src/odoo/addons,local --data-dir filestore
```
### After:
```sh
src/odoo/odoo-bin -c config.cfg
```

Nota: Substituir odoov2 pela db desejada.



