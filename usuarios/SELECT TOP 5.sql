SELECT DISTINCT TOP 50
   C1_FILIAL                -- Filial do Sistema (varchar(4), não nulo)
   , C1_NUM                 -- Número da Solicitação de Compra (MAX(SC1)) (varchar(6), não nulo)
   , C1_ITEM               -- Descricao do Produto (varchar(30), não nulo)
   , C1_DESCRI            -- Centro de Custo (varchar(16), não nulo)
   , C1_CC
   , C1_PRODUTO              -- Descricao do Produto	(varchar(30), não nulo)
   , C1_LOCAL               -- Armazem (varchar(2), não nulo)
   , C1_QUANT               -- Quantidade da SC (float, não nulo)
   , C1_EMISSAO             -- Data de Emissao da SC (varchar(8), não nulo)
   , C1_DATPRF              -- Data prev. da Necessidade	 (varchar(8), não nulo)
   , C1_SOLICIT             -- Nome do Solicitante (varchar(25), não nulo)
   , C1_OBS
   , SC1010.R_E_C_N_O_      -- (pk, bigint, não nulo)  
-- Identificador único de todas as tabelas.
FROM SC1010
ORDER BY R_E_C_N_O_ DESC


