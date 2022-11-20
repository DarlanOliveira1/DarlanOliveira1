import sqlite3

banco = sqlite3.connect("pdv2.db")
cursor = banco.cursor()

#cria a tabela de cliente
cursor.execute("CREATE TABLE clientes (cd_cliente integer primary key autoincrement, nm_cliente text, tel_cliente integer, cpf_cliente integer, end_cliente text)")

#Cria a tabela de fornecedores
cursor.execute("CREATE TABLE fornecedores (cd_forne integer primary key autoincrement, nm_forne text, tel_forne text, cnpj_forne integer, end_forne text)")

#Cria a tabela de produtos
cursor.execute("CREATE TABLE produtos (cd_prod integer primary key autoincrement, dsc_prod text,vlr_unit decimal(8,2), cd_forne integer, nm_forne text)")

#Cria a tabela de saldo estoque
cursor.execute("CREATE TABLE saldos (cod_mov integer primary key autoincrement, cd_prod integer, dsc_prod text, qtd_prod decimal(8,2))")

#Cria a tabela de vendas
cursor.execute("CREATE TABLE vendas (cd_venda integer primary key autoincrement, cd_prod integer, dsc_prod text, cd_cliente integer, nm_cliente text, qtd_venda decimal(8,2), vlr_unitario decimal(8,2),vlr_venda decimal(8,2))")

banco.commit()