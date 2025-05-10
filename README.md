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
 * [O Projeto](#O-Projeto)
    * [Resumo](#Resumo) 
  * [Ambiente de desenvolvimento](#Ambiente-de-desenvolvimento)
    * [Requisitos iniciais](#Requisitos-iniciais)
    * [Primeiro acesso](#Primeiro-acesso)
    * [Desenvolvimento](#Desenvolvimento)
    * [Testes](#Teste)
    * [Integração Contínua](#Integração Contínua)
<!--te-->



### O projeto


#### Resumo

Este projeto visa desenvolver uma aplicação web para gestão de estoque e controle de clientes, focada em pequenos empreendedores. A necessidade surgiu devido ao uso de métodos antiquados, como cadernetas e planilhas, que dificultam a organização e a precisão dos dados. O grupo está seguindo a metodologia do “Design Thinking” , onde vem realizando desde o início do projeto reuniões on-line para definir funcionalidades essenciais, como por exemplo; funções de autenticação de login, armazenamento seguro, geração de relatórios e uma interface intuitiva. A aplicação facilita o registro e a consulta de estoque e dados dos clientes. Em conclusão, a aplicação melhora a gestão de estoque e clientes, contribuindo para a competitividade e o crescimento de pequenos negócios.



### Ambiente de desenvolvimento


Requisitos iniciais 


- Baixe o VS Code: https://code.visualstudio.com/download 🔗
- Baixe o git: https://git-scm.com/downloads 🔗
- Baixe o Python: https://www.python.org/downloads/ 🔗


#### Primeiro acesso

Faça o clone deste repositório via https ou ssh. Abra o terminal em qualquer pasta que queira manter o projeto e digite: 
- ```git clone https://github.com/pisjc3/fechou-suas-vendas-agora.git``` para clone via https
- ```git clone git@github.com:pisjc3/fechou-suas-vendas-agora.git``` para clone via ssh

Com o projeto em sua máquina, crie um ambiente virtual na raiz
``` powershell
python -m venv venv
```

Ative o ambiente virtual no Windows
``` powershell
venv/Scrpits/activate
```

Ative o ambiente virtual no Linux ou macOS
``` bash
source venv/bin/activate
```

Caso o ambiente virtual não seja iniciado no Windows, abra o PowerShell como administrador e execute o comando
``` powershell
Set-ExecutionPolicy AllSigned -Force
```

Instale todas as dependências do arquivo ```requirements.txt``` 📦
``` powershell
pip install -r requirements.txt
```

Crie o arquivo ```.env``` na raiz do projeto, fazendo uma cópia do arquivo ```.env.example```, onde todas as variáveis de ambientes deverão ser preenchidas.

Faça as migrações necessárias para a base do banco de dados 🗃️
``` powershell
python manage.py migrate
```

Crie o superuser do Django 🔐
``` powershell
python manage.py createsuperuser
```

Rode o servidor do Django 🚀
``` powershell
python manage.py runserver 
```

Acesse a URL ```http://localhost:8000/admin/``` e faça o login com seu superuser

#### Desenvolvimento

Durante o desenvolvimento, alguns passos do Primeiro acesso devem ser repetidos:

- Ativar o ambiente virtual
- Rodar o servidor do Django

Ao fazer alterações no modelos do Django, através dos arquivos ```models.py```, rode o comando para gerar as migrações

``` powershell
python manage.py makemigrations
```

E logo após, faça as migrações para a base do banco de dados
``` powershell
python manage.py migrate
```

#### Testes

Os scripts de testes devem ser escritos dentro de cada módulo da entidade. Ex: `crm_apps/crm/cliente/tests/<test_models.py>`

Para executar os testes, rode o script exemplo
```powershell
python manage.py test crm_apps.crm.cliente.tests
```

#### Integração Contínua

Em `.github/workflows` existem os arquivos que fazem a automação de processos junto ao GitHub Actions. Ex: `tests.yml`, onde a cada `push` para a `branch main`, todos os testes da aplicação serão executados para fim de controle do cógido inserido no repositório do projeto.

