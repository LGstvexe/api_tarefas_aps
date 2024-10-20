CREATE OR REPLACE VIEW view_tarefas_concluidas AS
SELECT id, titulo, descricao, data_criacao, data_movimentacao
FROM tarefas_concluidas_log
WHERE status = true;
