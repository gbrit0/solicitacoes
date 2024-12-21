SELECT TOP 5
   C1_FILIAL                -- Filial do Sistema (varchar(4), não nulo)
   , C1_NUM                 -- Número da Solicitação de Compra (MAX(SC1)) (varchar(6), não nulo)
   , C1_ITEM                -- Item da Solicitação (varchar(4), não nulo)
   , B1_DESC                -- Descricao do Produto (varchar(30), não nulo)
   , C1_DESCRI
   , CTT_CUSTO              -- Centro de Custo (varchar(16), não nulo)
   , C1_CC
   , C1_PRODUTO              -- Descricao do Produto	(varchar(30), não nulo)
   , C1_LOCAL               -- Armazem (varchar(2), não nulo)
   , C1_QUANT               -- Quantidade da SC (float, não nulo)
   , C1_EMISSAO             -- Data de Emissao da SC (varchar(8), não nulo)
   , C1_DATPRF              -- Data prev. da Necessidade	 (varchar(8), não nulo)
   , C1_SOLICIT             -- Nome do Solicitante (varchar(25), não nulo)
   , SC1010.R_E_C_N_O_      -- (pk, bigint, não nulo)  
-- Identificador único de todas as tabelas.
FROM SC1010
   LEFT JOIN SB1010 ON B1_COD = C1_PRODUTO
   LEFT JOIN CTT010 ON CTT_CUSTO = C1_CC

WHERE C1_CC <> '         '

SELECT 
   MAX(COALESCE(CONVERT(INT, TRIM(C1_NUM)),0))
FROM SC1010
WHERE TRIM(C1_NUM) NOT LIKE '%G%' AND TRIM(C1_NUM) NOT LIKE ""
ORDER BY C1_NUM DESC

select max(R_E_C_N_O_)
FROM SC1010
;
SELECT MAX(R_E_C_N_O_) +1
                              FROM SC1010
select top 8 * from SB1010
SELECT
   M0_CODFIL AS Filial,
   -- SUBSTRING(M0_CODFIL, 1,2) AS Filial2,
   M0_FILIAL AS NomeFilial

FROM
   SYS_COMPANY

WHERE
   SYS_COMPANY.D_E_L_E_T_ = ''
   AND M0_NOME = 'BRG Geradores';

SELECT
   B1_COD AS cod_produto,
   B1_DESC AS produto
FROM SB1010
WHERE B1_FILIAL = '01'


SELECT TOP 5 * FROM SB1010
-- B1_COD (varchar(15), não nulo)
-- B1_DESC (varchar(50), não nulo)
-- B1_UM (varchar(2), não nulo)
-- B1_LOCPAD (varchar(2), não nulo)


SELECT CTT_FILIAL, CTT_CUSTO, CTT_DESC01 FROM CTT010 
WHERE D_E_L_E_T_ <> '*'
AND CTT_BLOQ = '2'
AND CTT_FILIAL = '0101'
AND CTT_CLASSE = '2'