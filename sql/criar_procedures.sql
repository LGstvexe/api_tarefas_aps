CREATE OR REPLACE PROCEDURE adicionar_tarefa(p_titulo VARCHAR, p_descricao VARCHAR)
AS $$
BEGIN
    -- Adiciona a nova tarefa criada para a tabela 'tarefas'
    INSERT INTO tarefas (titulo, descricao, status, data_criacao)
    VALUES (p_titulo, p_descricao, false, NOW());
END;
$$ LANGUAGE plpgsql;

