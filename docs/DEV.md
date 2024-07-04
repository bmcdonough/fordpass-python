# development
## my notes
## requirements
### virtualenv
```shell
pip3 install --user --upgrade pip setuptools virtualenv
git clone https://github.com/bmcdonough/fordpass-python.git --branch=dev
cd fordpass-python
virtualenv venv
source venv/bin/activate
pip3 install -r docs/dev-requirements.txt
```
### environment
```shell
cat env-example >>~/.env
vi ~/.env
```