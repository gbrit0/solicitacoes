select top 8 * from SC1010;


SELECT B1_COD,B1_DESC,B1_UM,B1_LOCPAD FROM SB1010
WHERE D_E_L_E_T_ <> '*'
AND B1_MSBLQL = '2'
AND B1_FILIAL = '01'