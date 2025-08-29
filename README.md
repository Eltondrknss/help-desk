# **Sistema Helpdesk**

## 1. Visão Geral do Projeto

Este projeto consiste em um sistema de chamados técnicos desenvolvido em Python. A aplicação é executada via terminal (CLI - Command-Line Interface) e permite a criação de usuários com diferentes níveis de permissão (Usuário, Técnico, Admin), a abertura de novos chamados, a atribuição e a atualização do status desses chamados.

O principal objetivo do projeto foi não apenas criar as funcionalidades, mas sim implementá-las sobre uma arquitetura de software robusta, escalável e de fácil manutenção, aplicando POO, princípios de design como **SOLID**, **Arquitetura limpa** e **Injeção de Dependência**.

## 2. Arquitetura e Princípios de Design

A arquitetura do sistema é o seu diferencial e foi projetada para ser altamente desacoplada, seguindo os preceitos da **Clean Architecture**. Ela é dividida em três camadas principais:

### **a) `Core`**

- **Responsabilidade:** Contém a lógica de negócio pura e as regras mais importantes do sistema. É o coração da aplicação.
- **Características:** Esta camada é totalmente independente de detalhes externos. Ela não sabe qual banco de dados está sendo usado, nem qual é o tipo de interface com o usuário. Isso a torna estável, reutilizável e fácil de testar.
- **Componentes:**
    - **Entidades (`Entities`):** Os objetos de negócio (ex: `User`, `Ticket`).
    - **Casos de Uso (`Use Cases`):** Orquestradores para cada ação do sistema (ex: `CreateUser`, `UpdateTicketStatus`).
    - **Contratos/Interfaces (`Repositories`, `Security`):** Classes Abstratas que definem as regras de como o `Core` deve interagir com o mundo exterior.

### **b) `Infrastructure`**

- **Responsabilidade:** Implementa os detalhes técnicos e as "ferramentas" que o `Core` precisa para funcionar. É a ponte entre a lógica de negócio e as tecnologias externas.
- **Características:** Esta camada depende das abstrações definidas no `Core`, aplicando o **Princípio da Inversão de Dependência (o 'D' do SOLID)**. Se precisarmos trocar o banco de dados de MySQL para PostgreSQL, por exemplo, apenas esta camada seria modificada.
- **Componentes:**
    - **Banco de Dados (`database`):** Implementações concretas dos repositórios (ex: `MySQLUserRepository`) e gerenciadores de conexão.
    - **Segurança (`security`):** Implementação concreta do serviço de hash de senhas (ex: `BcryptPasswordHasher`).

### **c) `Presentation`**

- **Responsabilidade:** Interagir com o usuário final.
- **Características:** Esta camada é a mais externa e volátil. Ela não contém regras de negócio; seu trabalho é apenas coletar dados do usuário, chamar os Casos de Uso apropriados no `Core` e exibir os resultados.
- **Componentes:**
    - **Interface de Linha de Comando (`cli`):** Classes que gerenciam os menus e fluxos de interação no terminal.

### **Injeção de Dependência (DI)**

O princípio que conecta todas as camadas. Em vez de uma classe criar suas próprias dependências (ex: um Caso de Uso instanciando um Repositório), ela as recebe prontas em seu construtor. Isso garante o baixo acoplamento e torna o sistema extremamente testável.

## 3. Estrutura de Pastas

A organização dos arquivos reflete a arquitetura descrita acima:

src/
├── core/
│    ├── entities/        # Classes de dados puras (User, Ticket)
│    ├── repositories/    # Contratos dos repositórios (ITicketRepository)
│    ├── security/        # Contrato do hasher de senha (IPasswordHasher)
│    └── use_cases/       # Classes com a lógica de negócio (CreateUser)
│
├── infrastructure/
│    ├── database/        # Implementação para MySQL dos repositórios
│    └── security/        # Implementação com Bcrypt do hasher
│
├── presentation/
│    └── cli/             # Classes da interface de linha de comando
│
├── config.py             # Classe para gerenciar configurações do .env
└── main.py               # Ponto de entrada: monta e executa a aplicação`

## 4. Funcionalidades Implementadas

O sistema atualmente suporta as seguintes funcionalidades:

### **Gerais (Visitante):**

- **Login de Usuário:** Autenticação segura com verificação de email e senha hasheada.
- **Criação de Novo Usuário:** Cadastro de novos usuários com cargos definidos (admin, técnico, usuário).

### **Usuário Logado (Qualquer cargo):**

- **Abrir Novo Chamado:** Um usuário pode criar um novo chamado técnico com título e descrição.
- **Listar "Meus Chamados":** Um usuário pode ver uma lista de todos os chamados que ele mesmo abriu.
- **Logout:** Encerrar a sessão.

### **Técnico & Admin:**

- **Visualizar Fila de Trabalho:** Ver uma lista de todos os chamados que não estão fechados.
- **Atribuir e Atualizar Chamado:** Um técnico ou admin pode se atribuir a um chamado e alterar seu status para "Em Andamento" ou "Fechado".

### **Administrador:**

- **Listar Todos os Usuários:** Um admin tem acesso a uma lista de todos os usuários cadastrados no sistema.

## 5. Configuração e Instalação

Para executar o projeto, siga os passos abaixo:

### **Pré-requisitos:**

- Python 3.8 ou superior
- Um servidor de banco de dados MySQL em execução

### **Passos:**

1. **Clone o repositório** ou descompacte os arquivos do projeto em uma pasta local.
2. **Crie e ative um ambiente virtual**
    
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    
3. **Instale as dependências**
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Configure o Banco de Dados:**
    - Crie um novo banco de dados no seu servidor MySQL:SQL
        
        ```sql
        CREATE DATABASE sistema_chamados CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ```
        
5. **Crie as Tabelas:**
    - Execute os seguintes comandos SQL no banco de dados recém-criado
        
        ```sql
        - Tabela de Usuários
        CREATE TABLE users (
        			id INT AUTO_INCREMENT PRIMARY KEY,
        			name VARCHAR(255) NOT NULL,
        			email VARCHAR(255) NOT NULL UNIQUE,
        			password_hash VARCHAR(255) NOT NULL,
        			role ENUM('admin', 'technician', 'user') NOT NULL
        );
        
        -- Tabela de Chamados
        CREATE TABLE tickets (
        			id INT AUTO_INCREMENT PRIMARY KEY,
        			title VARCHAR(255) NOT NULL,
        			description TEXT,
        			status ENUM('open', 'in_progress', 'closed') NOT NULL DEFAULT 'open',
        			user_id INT NOT NULL,
        			technician_id INT,
        			created_at DATETIME NOT NULL,
        			updated_at DATETIME NOT NULL,
        			CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
        			CONSTRAINT fk_technician FOREIGN KEY (technician_id) REFERENCES users(id)
        );
        ```
        
6. **Configure as Variáveis de Ambiente:**
    - Renomeie o arquivo `.env.example` para `.env` (ou crie um novo arquivo `.env` na raiz do projeto).
    - Edite o arquivo `.env` com suas credenciais do MySQL
        
        ```toml
        DB_HOST=localhost
        DB_PORT=3306
        DB_USER=seu_usuario_mysql
        DB_PASSWORD=sua_senha_mysql
        DB_NAME=sistema_chamados
        ```
        

## 6. Como Executar o Sistema

Com o ambiente virtual ativado e o arquivo `.env` configurado, execute o seguinte comando a partir da pasta raiz do projeto:

```bash
python -m src.main
```

O sistema será iniciado e o menu principal aparecerá no terminal.

## 7. Detalhes Técnicos e Bibliotecas

- **Linguagem:** Python 3
- **Banco de Dados:** MySQL
- **Bibliotecas Principais:**
    - `mysql-connector-python`: Driver oficial para conexão com o MySQL.
    - `bcrypt`: Para hashing seguro de senhas.
    - `python-dotenv`: Para gerenciamento de variáveis de ambiente.

## 8. Próximos Passos e Melhorias Futuras

O sistema possui uma fundação sólida que permite diversas expansões, como:

- **Testes Unitários:** Implementar `pytest` para testar os Casos de Uso e garantir a qualidade do código.
- **Migrações de Banco de Dados:** Adotar uma ferramenta como `Alembic` para gerenciar o versionamento do schema do banco de dados.
- **Expandir Funcionalidades:** Adicionar a possibilidade de um usuário ver detalhes de um chamado, adicionar comentários, e para um admin poder atribuir um chamado a um técnico específico.
- **Interface Web/API:** A camada `core` está pronta para ser consumida por uma API REST (usando Flask ou FastAPI) ou uma aplicação web (usando Django/Flask), bastando criar uma nova camada de `presentation`.
