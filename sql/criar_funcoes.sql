CREATE OR REPLACE FUNCTION
	contar_tarefas()
RETURNS INTEGER AS $$
	SELECT COUNT(*) FROM tarefas;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION contar_tarefas_atrasadas() RETURNS TABLE (
    id INTEGER,
    titulo VARCHAR,
    descricao VARCHAR,
    data_criacao TIMESTAMP
) AS $$
BEGIN
	-- Vai retornar todas as tarefas criadas há mais de 7 dias e que ainda não foram concluídas
	RETURN QUERY -- Permite retornar os resultados de uma QUERY diretamente
	SELECT tarefas.id, tarefas.titulo, tarefas.descricao, tarefas.data_criacao
	FROM tarefas
	WHERE tarefas.data_criacao < NOW() - INTERVAL '7 days' AND tarefas.status = false
	ORDER BY tarefas.data_criacao;
END;
$$ LANGUAGE plpgsql;
