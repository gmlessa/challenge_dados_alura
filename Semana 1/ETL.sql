##Criando banco de dados
CREATE DATABASE IF NOT EXISTS analise_risco;
USE analise_risco;

##Visualizando os dados

SELECT * FROM dados_mutuarios;
SELECT * FROM emprestimos;
SELECT * FROM historicos_banco;
SELECT * FROM id;

##Vendo o número de linhas de cada tabela

SELECT COUNT(*) from dados_mutuarios;
SELECT count(*) from emprestimos;
select count(*) from historicos_banco;
select count(*) from id;

##Vendo o número de linhas de cada tabela lado a lado

SELECT (
	SELECT COUNT(*) FROM dados_mutuarios) as dados_mutuarios,(
    SELECT COUNT(*) FROM emprestimos) as emprestimos,(
    SELECT COUNT(*) FROM historicos_banco) as historicos_banco,(
    SELECT COUNT(*) FROM id) as id
FROM DUAL;

##Verificando inconsistência de dados da tabela dados_mutuariios

select distinct person_home_ownership from dados_mutuarios;
select * from dados_mutuarios
where person_emp_length > 100;

select count(*) from id a inner join dados_mutuarios b
on a.person_id = b.person_id
where person_home_ownership = "";

select * from dados_mutuarios
where person_id = "";

select * from dados mutuarios
where person_age <0;

select * from dados_mutuarios
where person_age > 100;

select * from id a inner join dados_mutuarios b
on a.person_id = b.person_id;

SELECT *, REPLACE(person_home_ownership, "Rent", "Aluguel"), REPLACE(person_home_ownership, "Own", "Propria")
from dados_mutuarios;

SELECT sum(person_age is null), sum(person_home_ownership = "") FROM dados_mutuarios;

##Tratando inconsistência e traduzindo dados da tabela dados_mutuários

Start transaction;

update dados_mutuarios
	set person_home_ownership = replace(person_home_ownership, "Rent", "Aluguel"),
		person_home_ownership = replace(person_home_ownership, "Own", "Própria"),
		person_home_ownership = replace(person_home_ownership, "Mortgage", "Hipoteca"),
		person_home_ownership = replace(person_home_ownership, "Other", "Outro"),
		person_home_ownership = if(person_home_ownership = "", NULL, person_home_ownership);
    
alter table dados_mutuarios
	rename column person_id to id_pessoa,
	rename column person_age to idade_pessoa,
	rename column person_income to salario_pessoa,
	rename column person_home_ownership to situacao_propriedade_pessoa,
	rename column person_emp_length to tempo_trabalhado_pessoa;

update dados_mutuarios
	set id_pessoa = if(id_pessoa = "", Null, id_pessoa);
    
commit;

##Verificando inconsistência dos dados da tabela emprestimos

select * from emprestimos;

select * from emprestimos
where loan_id = "";

select * from emprestimos
where loan_intent = "";

select * from emprestimos
where loan_grade = "";

select * from emprestimos
where loan_amnt < 0;

select * from emprestimos
where loan_int_rate < 0;

select distinct loan_status from emprestimos;

select * from emprestimos
where loan_percent_income > 1;

##Tratando inconscistências e traduzindo dados da tabela emprestimos

start transaction;

alter table emprestimos
	rename column loan_id to id_emprestimo,
	rename column loan_intent to motivo_emprestimo,
	rename column loan_grade to pontuacao_emprestimo,
	rename column loan_amnt to valor_emprestimo,
	rename column loan_int_rate to taxa_juros_emprestimo,
	rename column loan_status to status_emprestimo,
	rename column loan_percent_income to porcentagem_salario_emprestimo;

update emprestimos
set motivo_emprestimo = if(motivo_emprestimo = "", NULL, motivo_emprestimo),
	motivo_emprestimo = replace(motivo_emprestimo, "Homeimprovement", "Melhora do lar"),
    motivo_emprestimo = replace(motivo_emprestimo, "Venture", "Empreendimento"),
    motivo_emprestimo = replace(motivo_emprestimo, "Education", "Educativo"),
    motivo_emprestimo = replace(motivo_emprestimo, "Medical", "Médico"),
    motivo_emprestimo = replace(motivo_emprestimo, "Debtconsolidation", "Pagamento de débitos");
    
update emprestimos
	set pontuacao_emprestimo = if(pontuacao_emprestimo = "", NULL, pontuacao_emprestimo);


commit;

##Verificando inconsistências da tabela historicos_banco

select * from historicos_banco
where cb_id = "";

select distinct cb_person_default_on_file from historicos_banco;

select * from historicos_banco
where cb_person_cred_hist_length <0;

select * from historicos_banco
where cb_person_cred_hist_length > 100;

##Tratando inconsistências e traduzindo dados da tabela historicos_banco

start transaction;

alter table historicos_banco
	rename column cb_id to id_cb,
    rename column cb_person_default_on_file to foi_inadimplente_cb,
    rename column cb_person_cred_hist_length to tempo_primeira_solicitacao_credito_cb;

update historicos_banco
	set foi_inadimplente_cb = if(foi_inadimplente_cb="", NULL, foi_inadimplente_cb),
    foi_inadimplente_cb = replace(foi_inadimplente_cb, "Y", "S");
    
commit;

##Verificando inconsistências da tabela id

select * from id
where person_id = "";

select * from id
where loan_id = "";

select * from id
where cb_id = "";

##Traduzindo os dados da tabela id

start transaction;

alter table id
	rename column person_id to id_pessoa,
    rename column loan_id to id_emprestimo,
    rename column cb_id to id_cb;

select * from id;

commit;


    




