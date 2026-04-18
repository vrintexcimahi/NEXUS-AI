<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

try {
    $dbFile = __DIR__ . '/nexus_gpt.db';
    $db = new PDO("sqlite:$dbFile");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Check storage table for history entries
    $stmt = $db->query("SELECT username, key_name, LENGTH(value_data) as data_length FROM storage WHERE key_name LIKE 'nexus_history_%' ORDER BY username, key_name");
    $historyRows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Check all users
    $userStmt = $db->query("SELECT username, role, email, phone FROM users ORDER BY username");
    $users = $userStmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Sample history data (first user)
    $sampleHistory = null;
    if (!empty($historyRows)) {
        $firstUser = $historyRows[0]['username'];
        $sampleStmt = $db->prepare("SELECT value_data FROM storage WHERE username = ? AND key_name = ?");
        $sampleStmt->execute([$firstUser, 'nexus_history_' . $firstUser]);
        $sampleData = $sampleStmt->fetchColumn();
        $sampleHistory = json_decode($sampleData, true);
    }
    
    echo json_encode([
        'success' => true,
        'db_exists' => file_exists($dbFile),
        'db_size' => file_exists($dbFile) ? filesize($dbFile) : 0,
        'history_entries' => count($historyRows),
        'history_rows' => $historyRows,
        'users' => $users,
        'sample_history_sessions' => $sampleHistory ? array_keys($sampleHistory) : [],
        'sample_session_count' => $sampleHistory ? count($sampleHistory) : 0
    ], JSON_PRETTY_PRINT);
    
} catch (Exception $e) {
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
?>
