-- ==============================================================
-- CONSULTAS ANALÍTICAS (DML) - TRABALHO IBD
-- ==============================================================
-- ATENÇÃO!!!!!  Substitua os "nomes" nas consultas  por algum nome de cliente válido com o "SELECT * FROM CLIENTE;" 
-- --------------------------------------------------------------
-- 1. Disponibilidade Regional
-- O que faz: Lista os títulos distintos de todos os filmes que estão 
-- disponíveis em catálogos associados a regiões cujo país é o "Brasil".
-- --------------------------------------------------------------
SELECT DISTINCT f.titulo
FROM Filme f
JOIN Disponibilidade_Filme df ON f.ID_filme = df.ID_filme
JOIN Catalogo c ON df.ID_Catalogo = c.ID_Catalogo
JOIN Catalogo_Regional cr ON c.ID_Catalogo = cr.ID_Catalogo
JOIN Regiao r ON cr.ID_regiao = r.ID_regiao
WHERE r.Pais = 'Brasil';


-- --------------------------------------------------------------
-- 2. Favoritos do Cliente
-- O que faz: Recupera o título e a data de interação dos filmes que 
-- o cliente "Fulano de Tal" marcou como favoritos, ordenados do mais 
-- recente para o mais antigo.
-- --------------------------------------------------------------
SELECT f.titulo, pc.data_interacao
FROM Filme f
JOIN Preferencia_Cliente pc ON f.ID_filme = pc.ID_filme
JOIN Cliente c ON pc.CPF_cliente = c.CPF
WHERE c.nome_completo = 'Noah Bains'
  AND pc.favorito_bool = TRUE
ORDER BY pc.data_interacao DESC;


-- --------------------------------------------------------------
-- 3. Melhores Comédias
-- O que faz: Lista os títulos e a nota média dos filmes do gênero 
-- "Comédia" que possuem uma avaliação média igual ou superior a 4.
-- --------------------------------------------------------------
SELECT f.titulo, AVG(pc.avaliacao) as media_nota
FROM Filme f
JOIN Preferencia_Cliente pc ON f.ID_filme = pc.ID_filme
WHERE f.genero = 'Comédia'
GROUP BY f.ID_filme, f.titulo
HAVING AVG(pc.avaliacao) >= 4;


-- --------------------------------------------------------------
-- 4. Filmes sem Visualização (Diferença)
-- O que faz: Encontra os títulos dos filmes que não tiveram nenhuma 
-- sessão de visualização registrada no período de 01/08/2025 a 31/08/2025.
-- --------------------------------------------------------------
SELECT f.titulo
FROM Filme f
WHERE NOT EXISTS (
    SELECT 1
    FROM Sessao_Visualizacao s
    WHERE s.ID_filme = f.ID_filme
      AND s.data_hora_inicio BETWEEN '2025-08-01' AND '2025-08-31'
);


-- --------------------------------------------------------------
-- 5. Relatório de Consumo por Filme (Brasil)
-- O que faz: Apresenta o título, a contagem total de visualizações e a 
-- soma de minutos assistidos para filmes disponíveis no Brasil durante 
-- Novembro de 2025.
-- --------------------------------------------------------------
SELECT 
    f.titulo,
    COUNT(s.data_hora_inicio) AS total_visualizacoes,
    COALESCE(SUM(s.duracao_sessao), 0) AS total_minutos_assistidos
FROM Filme f
JOIN (
    SELECT DISTINCT df.ID_filme
    FROM Disponibilidade_Filme df
    JOIN Catalogo_Regional cr ON df.ID_Catalogo = cr.ID_Catalogo
    JOIN Regiao r ON cr.ID_regiao = r.ID_regiao
    WHERE r.Pais = 'Brasil'
) filmes_brasil ON f.ID_filme = filmes_brasil.ID_filme
LEFT JOIN Sessao_Visualizacao s 
    ON f.ID_filme = s.ID_filme 
    -- AJUSTE AQUI: Mudado para pegar DEZEMBRO ou o ano todo
    AND s.data_hora_inicio >= '2025-12-01 00:00:00' 
    AND s.data_hora_inicio <= '2025-12-31 23:59:59'
GROUP BY f.ID_filme, f.titulo
ORDER BY total_visualizacoes DESC;

-- --------------------------------------------------------------
-- 6. Consumo por Gênero
-- O que faz: Calcular o total de horas que o cliente "Fulano de Tal" 
-- passou assistindo conteúdo em 2025, agrupado por gênero.
-- --------------------------------------------------------------

SELECT 
    f.genero,
    -- Soma os minutos e divide por 60 para obter horas, arredondando para 2 casas decimais
    ROUND(SUM(s.duracao_sessao) / 60, 2) AS total_horas_assistidas
FROM Sessao_Visualizacao s
JOIN Filme f ON s.ID_filme = f.ID_filme
JOIN Cliente c ON s.CPF_cliente = c.CPF
WHERE c.nome_completo = 'Noah Bains' -- Substitua pelo nome do cliente "X"
  AND s.data_hora_inicio BETWEEN '2025-01-01 00:00:00' AND '2025-12-31 23:59:59' -- Período informado
GROUP BY f.genero
ORDER BY total_horas_assistidas DESC;


-- --------------------------------------------------------------
-- 7. Métricas de Planos
-- O que faz: Listar os nomes dos planos oferecidos, a quantidade total 
-- de clientes atualmente ativos (aqueles cuja data de término na 
-- assinatura é nula) e a média do número máximo de dispositivos permitidos.
-- --------------------------------------------------------------
SELECT 
    p.nome_plano,
    COUNT(ah.CPF_cliente) AS qtd_clientes_ativos,
    AVG(p.n_dispositivos) AS media_dispositivos_max
FROM Plano p
JOIN Assina_Historico ah ON p.ID_plano = ah.ID_plano
WHERE ah.data_termino IS NULL
GROUP BY p.ID_plano, p.nome_plano;


-- --------------------------------------------------------------
-- 8. Ranking de Popularidade (Brasil)
-- O que faz: Identificar os 5 filmes com maior tempo total de exibição 
-- (soma da duração das sessões) assistidos por clientes que residem no 
-- Brasil, considerando apenas o último mês.
-- --------------------------------------------------------------
SELECT 
    f.titulo,
    SUM(s.duracao_sessao) AS total_minutos_assistidos,
    COUNT(*) AS total_sessoes
FROM Sessao_Visualizacao s
JOIN Filme f ON s.ID_filme = f.ID_filme
JOIN Cliente c ON s.CPF_cliente = c.CPF
JOIN Regiao_residencia rr ON c.CPF = rr.CPF
JOIN Regiao r ON rr.ID_regiao = r.ID_regiao
WHERE r.Pais = 'Brasil'
  AND s.data_hora_inicio >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
GROUP BY f.ID_filme, f.titulo
ORDER BY total_minutos_assistidos DESC, total_sessoes DESC
LIMIT 5;


-- --------------------------------------------------------------
-- 9. Análise de Qualidade de Streaming
-- O que faz: Calcular a distribuição (contagem e percentual) das 
-- diferentes qualidades de reprodução (como '4K', 'HD') utilizadas nas 
-- sessões de visualização do cliente "Fulano de Tal".
-- --------------------------------------------------------------
SELECT 
    s.qualidade_reproducao,
    COUNT(*) AS qtd_sessoes,
    (COUNT(*) * 100.0 / (
        SELECT COUNT(*) 
        FROM Sessao_Visualizacao s2 
        JOIN Cliente c2 ON s2.CPF_cliente = c2.CPF 
        WHERE c2.nome_completo = 'Noah Bains'
    )) AS percentual
FROM Sessao_Visualizacao s
JOIN Cliente c ON s.CPF_cliente = c.CPF
WHERE c.nome_completo = 'Noah Bains'
GROUP BY s.qualidade_reproducao;


-- --------------------------------------------------------------
-- 10. Migração de Planos (Churn/Upgrade)
-- O que faz: Listar os clientes que alteraram seu plano de assinatura nos 
-- últimos 3 meses, exibindo o nome do cliente, o plano anterior, o plano 
-- novo e as datas relevantes para análise de migração.
-- --------------------------------------------------------------
SELECT 
    c.nome_completo,
    p_antigo.nome_plano AS plano_anterior,
    p_novo.nome_plano AS plano_novo,
    antigo.data_inicio AS inicio_anterior,
    antigo.data_termino AS termino_anterior,
    novo.data_inicio AS inicio_novo
FROM Assina_Historico antigo
JOIN Assina_Historico novo 
    ON antigo.CPF_cliente = novo.CPF_cliente 
    AND antigo.data_termino = novo.data_inicio 
JOIN Cliente c ON antigo.CPF_cliente = c.CPF
JOIN Plano p_antigo ON antigo.ID_plano = p_antigo.ID_plano
JOIN Plano p_novo ON novo.ID_plano = p_novo.ID_plano
WHERE antigo.data_termino >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
  AND p_antigo.ID_plano <> p_novo.ID_plano;
