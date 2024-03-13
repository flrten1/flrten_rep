<?php
// Подключение к базе данных
$db = new PDO('sqlite:links.db');

// Получение данных о статистике
$stmt = $db->prepare('SELECT short_url, COUNT(*) as count FROM clicks GROUP BY short_url');
$stmt->execute();
$statistics = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Вывод статистики в формате JSON
header('Content-Type: application/json');
echo json_encode($statistics);
?>
