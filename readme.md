Olá, aqui vai umas dicas para que usufrua da aplicação sem erros :D

- Primeiramente, certifique de ter instalado em sua máquina o oracle database express 11g ou superior, para o correto funcionamento da conexão com o python nesta 
aplicação e também instalado o cx_oracle, uma biblioteca para a comunicação com o banco, pode ser instalado com o seguinte comando no terminal: pip install cx_Oracle.

- Depois deste primeiro passo, você precisa instalar o Oracle Instant Client, através deste link: https://www.oracle.com/br/database/technologies/instant-client.html

- Logo após ter instalado, ao extrair o código para sua máquina, na linha 13 e 14 irá ter o seguinte comando:

os.chdir("C:")
os.chdir("C:\\Users\\carlo\\Downloads\\instantclient-basic-windows.x64-19.6.0.0.0dbru\\instantclient_19_6")

=====> NESTE MOMENTO É IMPORTANTE QUE VOCê SUBSTITUA O CÓDIGO ACIMA COM O CAMINHO QUE ESTÁ INSTALADO  O SEU INSTANT CLIENTE, APENAS MODIFICAR COM O CAMINHO
DA ONDE VOCÊ EXTRAIU O INSTANT CLIENT, UTILIZANDO DUAS BARRAS PARA QUE O INTERPRETADOR ENTENDA QUE É UM DIRETÓRIO!.

- Depois disso basta inserir seu usuário do oracle database, que geralmente é system, e depois sua senha que escolheu na instalação. 

ESPERO QUE GOSTEM <3
