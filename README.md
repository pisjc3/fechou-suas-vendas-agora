# Projeto Integrador III

Projeto Integrador III - Grupo 012 - UNIVESP

Tema: Desenvolver um software com framework web ou aplicativo que utilize banco de dados, inclua script web (Javascript), nuvem, acessibilidade, controle de versão, integração contínua e testes. Incluir um dos seguintes requisitos: uso e fornecimento de API, análises de dados e IoT.

## Participantes

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/ocarlosmonteiro.png" width="100px;" alt="Foto de Carlos Monteiro"/><br />
      <a href="https://github.com/ocarlosmonteiro"><sub><b>Carlos Monteiro</b></sub></a>
    </td>
    <td align="center">
      <img src="https://github.com/obZenBR.png" width="100px;" alt="Foto de Elder Xavier"/><br />
      <a href="https://github.com/obZenBR"><sub><b>Elder Xavier</b></sub></a>
    </td>
    <td align="center">
      <img src="" width="100px;" alt=""/><br />
      <a href=""><sub><b>Elton Miranda</b></sub></a>
    </td>
    <td align="center">
      <img src="https://github.com/OliveiraGmo.png" width="100px;" alt="Foto de Gabriel Monteiro"/><br />
      <a href="https://github.com/OliveiraGmo"><sub><b>Gabriel Monteiro</b></sub></a>
    </td>
    <td align="center">
      <img src="https://github.com/jobemcamera.png" width="100px;" alt="Foto de Jobe Camera"/><br />
      <a href="https://github.com/jobemcamera"><sub><b>Jobe Camera</b></sub></a>
    </td>
    <td align="center">
      <img src="https://github.com/julianagomeshioki.png" width="100px;" alt="Foto de Juliana Hioki"/><br />
      <a href="https://github.com/julianagomeshioki"><sub><b>Juliana Hioki</b></sub></a>
    </td>
    <td align="center">
      <img src="" width="100px;" alt=""/><br />
      <a href=""><sub><b>Marcos Rendohl</b></sub></a>
    </td>
    <td align="center">
      <img src="" width="100px;" alt=""/><br />
      <a href=""><sub><b>Otávio Augusto</b></sub></a>
    </td>
  </tr>
</table>


## Índice

<!--ts-->
  * [Requisitos iniciais](#Requisitos-iniciais)
  * [Ambiente de desenvolvimento](#Ambiente-de-desenvolvimento)
<!--te-->

### Requisitos iniciais

- Baixe o VS Code: https://code.visualstudio.com/download
- Baixe o git: https://git-scm.com/downloads
- Baixe o Python: https://www.python.org/downloads/


### Ambiente de desenvolvimento

Faça o clone deste repositório via https ou ssh. Abra o terminal em qualquer pasta que queira manter o projeto e digite: 
- ```git clone https://github.com/pisjc3/fechou-suas-vendas-agora.git``` para clone via https
- ```git clone git@github.com:pisjc3/fechou-suas-vendas-agora.git``` para clone via ssh

Com o projeto em sua máquina, crie um ambiente virtual na raiz
```
python -m venv venv
```

Ative o ambiente virtual no Windows
```
venv/Scrpits/activate
```

Ative o ambiente virtual no Linux ou macOS
```
source venv/bin/activate
```

Caso o ambiente virtual não seja iniciado no Windows, abra o PowerShell como administrador e execute o comando
```
Set-ExecutionPolicy AllSigned -Force
```

Instale todas as dependências do arquivo ```requirements.txt```
```
pip install -r requirements.txt
```

Faça as migrações necessárias para a base de dados do Django
```
python manage.py makemigrations
python manage.py migrate
```

Crie o superuser do Django
```
python manage.py createsuperuser
```

Rode o servidor do Django
```
python manage.py runserver 
```

Acesse a URL ```http://localhost:8000/admin/``` e faça o login com seu superuser
