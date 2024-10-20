CREATE OR REPLACE FUNCTION mover_tarefa_para_log() RETURNS trigger AS $$
BEGIN
    -- Move a tarefa para o log quando o status é alterado para concluído
    IF NEW.status = true THEN
        INSERT INTO tarefas_concluidas_log (titulo, descricao, status, data_criacao, data_movimentacao)
        VALUES (NEW.titulo, NEW.descricao, NEW.status, NEW.data_criacao, NOW());

    -- Remove a tarefa da tabela original
        DELETE FROM tarefas WHERE id = NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_mover_tarefas_concluidas
AFTER UPDATE ON tarefas
FOR EACH ROW
WHEN (NEW.status = true)
EXECUTE FUNCTION mover_tarefa_para_log();