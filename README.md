# Challenge Data Science da Alura

## Desafio

Você foi contratado(a) como pessoa cientista de dados para trabalhar em um banco digital internacional chamado Alura Cash. Na primeira reunião do seu novo trabalho, a diretoria financeira informa que, recorrentemente, estão surgindo pessoas inadimplentes após a liberação de créditos. Portanto, é solicitada uma solução para que seja possível diminuir as perdas financeiras por conta de pessoas mutuarias que não quitam suas dívidas.

Como cientista de dados, você sugere um estudo das informações financeiras e de solicitação de empréstimo para encontrar padrões que possam indicar uma possível inadimplência.

Desse modo, você solicita um conjunto de dados que contenha as informações de clientes, da solicitação de empréstimo, do histórico de crédito, bem como se a pessoa mutuaria é inadimplente ou não. Com esses dados, você sabe que consegue modelar um classificador capaz de encontrar potenciais clientes inadimplentes e solucionar o problema do Alura Cash.

## Semana 01 - Tratamento de dados: entendendo como tratar dados com SQL

  A Alura Cash disponibilizou um Dump SQL para poder fazer a carga dos dados, então, utilizando a ferramenta MySQL Workbench, criei um banco de dados com o nome analise_risco e utilizei o Data Import/Restore do Workbench para importar os dados.
  
  Logo após, li o dicionário disponibilizado, vi os tipos de variáveis e comecei a fazer o tratamento dos dados. Observei que tinham algumas colunas contendo valores em branco e nulos, inclusive no campo Id. Eu atualizei os valores brancos para nulos e mantive todas as linhas, deletando somente as linhas que estavam com o id nulo, além disso, na tabela id, a tipagem estava diferente dos ids das outras tabelas, então alterei para ficar igual às tabelas relacionadas (de text para varchar(16)). E então criei chaves primárias e estrangeiras para fazer o relacionamento das tabelas e fiz a tradução dos dados para o português, o script está disponibilizado no arquivo **ETL.sql**.
  
  Com os dados tratados e traduzidos, eu fiz um inner join da tabela id com as outras tabelas e então exportei para o arquivo **dados_unicos_por_id.csv** utilizando a ferramenta de exportação do Workbench.
  
  **OBS**: Como ainda não sei o que exatamente será feito com os dados eu optei por manter campos nulos, pois as outras informações contidas nas outras colunas podem ser úteis para futuras análises, e posso tratar os campos nulos de outras formas sem ser deletando, posso preencher com a média ou moda, por exemplo.
  
  **OBS2**: Na tabela dados_mutuarios, nas colunas de idade e de tempo trabalhado, existem idades superiores a 100 anos, o que é uma inconsistência, no entanto, como não tive uma orientação da Alura Cash a respeito, optei por manter as linhas sem apagar.
  
  ## Semana 02 
  
  O desafio desta semana foi focado em utilizar o arquivo .csv gerado na primeira semana para poder fazer modelos de Machine Learning para poder fazer predições sobre quais clientes podem ou não ser inadimplentes quando solicitam crédito para empréstimo.
  
  Utilizei o Google Collab para fazer todo o processo. Para o tratamento dos dados, removi todos os dados nulos a pedido da Alura Cash. Depois tive que aplicar encoding nas variáveis categóricas e fiz a padronização e normalização das variáveis quantitativas para lidar com os outliers e poder ter melhor performance e precisão nos modelos.
  
  Para aplicar meus conhecimentos de machine learning, utilizei a Regressão Linear, o Random Forest e K-Nearest Neighbors para poder fazer as predições. Como sabia que a variável alvo da base de dados estava desbalanceada (variável status_emprestimo), analisei métricas como a precisão, recall e curva ROC para poder avaliar o modelo.
  
  Após os modelos estarem criados, refiz o processo utilizando o banco de dados balanceados desta vez. Fiz um random oversampling da biblioteca imbaleced_learn, e apliquei os modelos novamentes. Foi notável a melhora dos modelos, provando que o balanceamento ajuda muito.
  
  Por fim, exportei os modelos para arquivos no formato .pkl, para poder utilizar nas outras semanas.

  ## Semana 03 e 04

  O desafio desta semana é focado em fornecer os modelos criados na semana 2 através de uma API para o Power BI e poder fazer predições em um cliente ainda não avaliado pelo modelo e poder decidir se o banco irá fazer a concessão de crédito ou não.
